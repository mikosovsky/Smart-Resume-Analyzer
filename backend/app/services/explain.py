# Evidence snippets for matched skills
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from backend.app.models.schemas import (
    JobDescriptionSchema,
    ResumeSchema,
    MatchResponseSchema,
)


class ExplanationService:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.output_parser = PydanticOutputParser(pydantic_object=MatchResponseSchema)
        self.prompt = PromptTemplate(
            template="""You are an expert recruiter at explaining matches between resumes and job descriptions. Given the resume details and job description details, provide a match score (0-10) and a detailed explanation for the score based on skills, experience, and education.\nResume Details:\n{resume_details}\nJob Description Details:\n{jd_details}\nProvide the output in JSON format matching the MatchResponseSchema.\n{format_instructions}""",
            input_variables=["resume_details", "jd_details"],
            partial_variables={
                "format_instructions": self.output_parser.get_format_instructions()
            },
        )

    def explain_match(
        self, resume: ResumeSchema, jd: JobDescriptionSchema
    ) -> MatchResponseSchema:
        prompt = self.prompt
        llm = self.llm
        output_parser = self.output_parser

        chain = prompt | llm | output_parser
        result = chain.invoke({"resume_details": resume, "jd_details": jd})
        return result
