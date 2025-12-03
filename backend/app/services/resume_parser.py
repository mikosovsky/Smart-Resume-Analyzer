# Skill detection (fuzzy + dictionary)
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.models.schemas import ResumeSchema


class ResumeParser:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.output_parser = PydanticOutputParser(pydantic_object=ResumeSchema)
        self.prompt = PromptTemplate(
            template="""You are an expert resume parser. Extract the following information from the resume text provided. Provide the output in JSON format matching the ResumeSchema. Resume text: {resume_text}.\n{format_instructions}""",
            input_variables=["resume_text"],
            partial_variables={
                "format_instructions": self.output_parser.get_format_instructions()
            },
        )

    def parse(self, resume_text: str) -> ResumeSchema:
        prompt = self.prompt
        llm = self.llm
        output_parser = self.output_parser
        chain = prompt | llm | output_parser
        result = chain.invoke({"resume_text": resume_text})
        return result
