# 1) Product spec (v1 → v1.5 → v2)

**v1 (MVP, 1–2 weeks)**

* Upload PDF/DOCX resume(s) + paste Job Description (JD).
* Parse → extract entities (skills, titles, dates) → compute embedding similarity to JD.
* Output: overall match score, top strengths, gaps, and highlight overlay on resume text.

**v1.5 (2–3 weeks)**

* Multi-resume ranking for one JD.
* Explainability pane: per-section score breakdown, matched/unmatched skills.
* Basic admin: save jobs, candidates, comparisons.

**v2 (4–6 weeks)**

* Multi-JD support; role taxonomy (e.g., “Data Scientist”, “SWE Backend”).
* Experience recency weighting + seniority inference.
* Export: PDF report + JSON.
* Team workspace (auth, shareable links), rate-limit, audit logs.

# 2) System architecture (suggested stack)

* **Frontend**: Next.js + Tailwind (file upload, results dashboard).
* **Backend API**: FastAPI (Python) with Celery for async parsing.
* **NLP/ML**:

  * OCR & parsing: `pdfminer`/`pdfplumber`, `python-docx`, fallback `tesseract` for scanned PDFs.
  * NER & skill extraction: spaCy + curated skills dictionary; optional LLM pass for robustness.
  * Embeddings: `text-embedding` model (e.g., OpenAI or local `bge-small-en` for cost control).
* **Vector store**: SQLite + `faiss` (local) → can swap to Postgres+pgvector or Pinecone later.
* **DB**: Postgres (users, jobs, candidates, scores, audit).
* **Storage**: S3-compatible (MinIO locally) for uploads & reports.
* **Auth**: NextAuth (email magic link/OAuth), JWT → FastAPI.
* **Infra**: Docker compose (web, api, worker, db, vector, storage), GitHub Actions CI.

# 3) Data model (minimal tables)

**users**(id, email, name, org_id, created_at)
**jobs**(id, user_id, title, jd_text, created_at)
**candidates**(id, user_id, name, source, resume_path, created_at)
**resume_chunks**(id, candidate_id, chunk_text, section, start_idx, end_idx, embedding_vector)
**skills**(id, name, canonical, aliases[])
**matches**(id, job_id, candidate_id, overall_score, strengths[], gaps[], scores_json, created_at)
**audit_logs**(id, user_id, action, entity, payload_json, created_at)

# 4) Core pipeline (MVP)

1. **Ingestion**

   * Detect file type; extract raw text.
   * Segment into sections: Header, Summary, Experience (bullets), Education, Skills.
   * Chunking: ~200–400 tokens with overlap; tag section per chunk.

2. **Skill extraction**

   * Dictionary match (fast): case-insensitive, lemmatized.
   * spaCy NER to capture organizations, titles, dates (for seniority/recency).
   * Optional LLM “skill normalization” to canonical labels.

3. **Job understanding**

   * Parse JD → required vs. nice-to-have skills, seniority hints, domain (e.g., fintech).

4. **Scoring (explainable)**

   * **Embedding score**: mean cosine across top-k resume chunks vs JD embedding.
   * **Keyword/skill coverage**: weighted coverage of required skills (binary + tf-idf lift).
   * **Recency weight**: experience dated within last N years gets multiplier.
   * **Seniority alignment**: inferred from titles + years (IC vs lead).
   * Final score = `0.45*embed + 0.35*skills + 0.15*recency + 0.05*seniority` (tunable).
   * Store per-component scores for the explainability pane.

5. **Explainability**

   * For each required skill, show: evidence snippet(s) + section + timestamp if present.
   * Highlight unmatched JD requirements as gaps.
   * Heatmap across resume sections (Experience/Skills/Education).

# 5) API design (FastAPI)

```
POST /api/upload-resume           -> {candidate_id}
POST /api/create-job              -> {job_id}
POST /api/match                   -> {job_id, candidate_ids[]} -> {matches[]}
GET  /api/match/{job_id}          -> {ranked_candidates, breakdown}
GET  /api/candidate/{id}/highlights
POST /api/export/report           -> returns PDF
```

# 6) Frontend UX (Next.js)

* **Home**: “Upload resumes” + “Paste JD”.
* **Results list**: table with Candidate, Overall Score, Skills Coverage, Last Updated; sort & filter.
* **Details drawer**:

  * Left: resume text with inline highlights.
  * Right: gauges for component scores; chips for strengths/gaps; timeline of roles.
* **Export** button -> PDF; **Share** -> link with token.

# 7) Evaluation plan (what to show interviewers)

* **Datasets**: scrape/curate ~50–100 public resumes + 10–20 JDs (mask PII).
* **Ground truth**: manually label top-5 candidates per JD.
* **Metrics**:

  * Ranking: NDCG@5, MRR, Precision@k.
  * Component ablations: show lift when adding recency/seniority.
* **Benchmarks**: “keyword-only baseline” vs. “our hybrid scoring”.
* **Error analysis**: a few failure cases with “why” and planned fixes.

# 8) Security & privacy

* Strip PII for logs; encrypt at rest (S3 SSE / pgcrypto).
* Signed URLs for downloads; per-org row-level scoping.
* Document data retention; delete original files option.
* Rate limiting + content scanning (block executables in uploads).

# 9) Deployment

* **Local dev**: Docker Compose (api, worker, next, pg, faiss, minio, redis).
* **Prod**: Render/Fly.io/Heroku for quick demo or GCP/AWS.
* **CI/CD**: lint, type check (mypy), unit tests, build, integration tests on a small sample; push image.

# 10) Cost control (critical for a public demo)

* Cache embeddings per chunk hash.
* Use local open-source embeddings (e.g., `bge-small-en`) by default; toggle to API for quality.
* Batch embedding calls; truncate long resumes smartly (experience > skills > education).

# 11) Stretch features (nice interview talking points)

* **LLM-backed cover letter suggestions**: from JD+resume (with editable draft).
* **Bias checks**: redact name/graduation year for “blind” scoring; fairness report.
* **LinkedIn profile parse**: URL → resume-like profile ingestion.
* **Calendarized review**: email summary of top candidates per JD.

# 12) Sample scoring pseudo-code

```python
def final_score(jd_vec, resume_chunks, skill_hits, recency_years, seniority_gap):
    # Embedding similarity
    sims = [cosine(jd_vec, c.vec) for c in resume_chunks]
    embed = mean(sorted(sims, reverse=True)[:5])

    # Skill coverage
    required = skill_hits['required']   # list of (skill, found: bool, snippet)
    nice     = skill_hits['nice']
    req_cov  = sum(int(f) for _, f, _ in required)/max(1,len(required))
    nice_cov = sum(int(f) for _, f, _ in nice)/max(1,len(nice))
    skills   = 0.8*req_cov + 0.2*nice_cov

    # Recency
    recency = min(1.0, sum(1/(1+y) for y in recency_years)/len(recency_years))

    # Seniority (0..1, 1=perfect)
    seniority = 1.0 - min(1.0, abs(seniority_gap)/3.0)

    return 0.45*embed + 0.35*skills + 0.15*recency + 0.05*seniority
```

# 13) README structure (make recruiters happy)

* **One-liner** + GIF demo at top.
* **Why it exists** (pain point).
* **How it works** (diagram + bullet pipeline).
* **Tech stack** + “Run locally in 2 commands”.
* **Screenshots** (upload, ranking, explainability).
* **Privacy** note.
* **Roadmap** + “Contributing”.

# 14) Testing checklist

* Unit: parsing, chunking, skill matcher, embedding wrapper, scorers.
* Integration: end-to-end for 3 sample resumes/JDs.
* Regression: saved fixtures for stable scores.
* Load: batch 100 resumes, ensure <X sec per resume on your machine.

# 15) Demo script (3 minutes)

1. Upload 5 resumes, paste JD → “Analyze”.
2. Show ranked list; click top candidate.
3. Walk through explainability (matched skills + evidence).
4. Export a one-page PDF report.
5. Mention metrics (NDCG@5) and fairness guardrails.

---

## Quick task breakdown (tickets you can open today)

* [ ] FastAPI skeleton + `/healthz`
* [ ] Resume extractors (pdf/docx/ocr) + tests
* [ ] Sectioner + chunker
* [ ] Embedding service (cache + batch)
* [ ] Skill dictionary + normalizer
* [ ] JD parser (required/nice-to-have)
* [ ] Scoring module (pluggable weights)
* [ ] Explainability: snippet finder + highlighter
* [ ] Vector store (faiss) CRUD
* [ ] Next.js upload + results table UI
* [ ] Candidate detail drawer + highlight view
* [ ] Exporter (WeasyPrint/ReportLab)
* [ ] Auth + org scoping
* [ ] Docker compose & CI