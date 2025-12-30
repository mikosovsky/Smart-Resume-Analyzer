# Smart Resume Analyzer 🎯

An AI-powered resume analysis and matching system that helps recruiters and hiring managers efficiently match resumes to job descriptions using advanced natural language processing and machine learning techniques.

## 📋 Overview

Smart Resume Analyzer is a FastAPI-based backend service that leverages OpenAI's GPT-4 models to intelligently parse resumes and job descriptions, then provides detailed matching scores and explanations. The system extracts structured information from unstructured documents and evaluates candidates based on skills, experience, education, and other relevant criteria.

## ✨ Features

- **Resume Parsing**: Automatically extract structured information from PDF resumes including:
  - Personal information (name, email, phone)
  - Work experience with company names, roles, dates, and descriptions
  - Educational background
  - Technical and soft skills

- **Job Description Parsing**: Extract and categorize job requirements:
  - Required vs. nice-to-have skills
  - Experience level requirements
  - Educational qualifications
  - Job responsibilities

- **Intelligent Matching**: Get detailed match scores (0-10) across multiple dimensions:
  - Hard skills alignment
  - Soft skills compatibility
  - Experience level matching
  - Educational background fit
  - Additional criteria evaluation

- **Explainable Results**: Each match includes detailed explanations for scoring decisions

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.11+**: Core programming language
- **Pydantic**: Data validation and settings management
- **LangChain**: Framework for developing LLM-powered applications
- **OpenAI GPT-4**: Advanced language model for parsing and analysis

### Document Processing
- **PyMuPDF (fitz)**: PDF text extraction
- **python-multipart**: File upload handling

### Authentication & Security
- **Authlib**: OAuth and authentication library
- **python-dotenv**: Environment variable management

### Testing & Quality
- **pytest**: Testing framework
- **pytest-asyncio**: Async testing support
- **ruff**: Fast Python linter and formatter
- **pre-commit**: Git hooks for code quality

### Development
- **uvicorn**: ASGI server
- **httpx**: HTTP client for testing

## 🏗️ Architecture

The application follows a clean architecture pattern with clear separation of concerns:

```
backend/
├── app/
│   ├── api/              # API routes and endpoints
│   ├── models/           # Pydantic schemas and data models
│   ├── services/         # Business logic services
│   │   ├── extract.py    # Document text extraction
│   │   ├── resume_parser.py    # Resume parsing with LLM
│   │   ├── jd_parser.py        # Job description parsing
│   │   └── explain.py          # Match explanation service
│   ├── core/             # Core functionality (scoring algorithms)
│   ├── workers/          # Background task workers (Celery ready)
│   ├── tests/            # Unit and integration tests
│   └── main.py           # Application entry point
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- OpenAI API key (for LLM-powered parsing)
- pip or uv for package management

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mikosovsky/Smart-Resume-Analyzer.git
cd Smart-Resume-Analyzer
```

2. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your configuration:
```env
AUTH0_CLIENT_ID=your_client_id
AUTH0_CLIENT_SECRET=your_client_secret
AUTH0_DOMAIN=your_domain
APP_SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
```

4. Run the application:
```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoints

#### Health Check
```http
GET /health
```
Returns the health status of the API.

#### Upload Resume
```http
POST /resume/upload
```
Upload a PDF resume and get structured parsed data.

**Request**: Multipart form data with PDF file

**Response**: ResumeSchema with extracted information

#### Upload Job Description
```http
POST /job-description/upload
```
Upload a text job description and get structured parsed data.

**Request**: Multipart form data with TXT file

**Response**: JobDescriptionSchema with extracted requirements

#### Match Resume to Job
```http
POST /match
```
Upload both a resume and job description to get detailed matching analysis.

**Request**: Multipart form data with both PDF resume and TXT job description

**Response**: MatchResponseSchema with scores and explanations

## 📊 Data Models

### ResumeSchema
Contains structured resume information including:
- Personal details (name, email, phone)
- Skills (hard and soft)
- Experience entries (company, role, dates, description)
- Education entries (institution, degree, dates, field of study)

### JobDescriptionSchema
Contains structured job information including:
- Job title and company
- Required education and experience
- Required skills and nice-to-have skills
- Responsibilities

### MatchResponseSchema
Contains matching analysis with:
- Candidate name and job title
- Hard skills match (score 0-10 + explanation)
- Soft skills match (score 0-10 + explanation)
- Experience match (score 0-10 + explanation)
- Education match (score 0-10 + explanation)
- Additional criteria match (score 0-10 + explanation)

## 🧪 Testing

The project uses pytest for testing. Tests are organized by component:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest backend/app/tests/services/test_extract.py

# Run tests with coverage
pytest --cov=backend/app
```

Test configuration is in `pytest.ini`.

## 🔧 Development

### Code Quality

The project uses Ruff for linting and formatting:

```bash
# Check code style
ruff check .

# Format code
ruff format .

# Check formatting without changes
ruff format --check --diff
```

### Pre-commit Hooks

Pre-commit hooks are configured to maintain code quality:

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### CI/CD

GitHub Actions workflow (`.github/workflows/python-ci.yml`) runs on every push and pull request:
- Python 3.11, 3.12, and 3.13 compatibility testing
- Linting with Ruff
- Format checking
- Automated tests

## 📁 Sample Data

The `data/samples/` directory contains example files for testing:
- `resume_frontend_engineer.txt`
- `resume_backend_engineer.txt`
- `resume_ml_engineer.txt`
- `jd_frontend_engineer.txt`
- `jd_backend_engineer.txt`
- `jd_ml_engineer.txt`

Use these for development and testing without needing your own data.

## 🗺️ Roadmap

The project roadmap is detailed in `GOALS.md` and includes:

### v1 (MVP) - Current Phase
- ✅ Resume and job description parsing
- ✅ Basic matching with explanations
- ✅ PDF and text file support
- ✅ RESTful API

### v1.5 (Planned)
- Multi-resume ranking for one job description
- Enhanced explainability with per-section breakdowns
- Admin panel for managing jobs and candidates
- Persistent storage with database

### v2 (Future)
- Multi-job description support
- Role taxonomy and categorization
- Experience recency weighting
- Seniority inference
- PDF report generation
- Team workspace with authentication
- Rate limiting and audit logs

### Stretch Features
- LLM-backed cover letter suggestions
- Bias detection and blind scoring
- LinkedIn profile parsing
- Automated candidate notifications

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Use type hints for all functions
- Write tests for new features
- Update documentation as needed
- Use Ruff for linting and formatting

## 🔒 Security & Privacy

- Sensitive configuration via environment variables
- OpenAI API calls are server-side only
- No resume data is stored permanently (stateless MVP)
- Future versions will include:
  - Encrypted at-rest storage
  - PII stripping for logs
  - Signed URLs for downloads
  - Row-level security per organization

## 📝 License

This project is currently unlicensed. Please contact the repository owner for usage permissions.

## 👤 Author

**Mikosovsky**
- GitHub: [@mikosovsky](https://github.com/mikosovsky)

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- FastAPI framework team
- LangChain community
- All contributors and testers

## 📞 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Contact via repository discussions
- Review the API documentation at `/docs`

---

**Note**: This is an active project under development. Features and APIs may change. Check the `GOALS.md` file for the detailed product specification and implementation plan.