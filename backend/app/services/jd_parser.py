# Split JD into required / nice-to-have items
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from backend.app.models.schemas import JobDescriptionSchema


class JobDescriptionParser:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.output_parser = PydanticOutputParser(pydantic_object=JobDescriptionSchema)
        self.prompt = PromptTemplate(
            template="""You are an expert job description parser. Extract the following information from the job description text provided. Provide the output in JSON format matching the JobDescriptionSchema. Job description text: {jd_text}.\n{format_instructions}""",
            input_variables=["jd_text"],
            partial_variables={
                "format_instructions": self.output_parser.get_format_instructions()
            },
        )

    def parse(self, jd_text: str) -> JobDescriptionSchema:
        prompt = self.prompt
        llm = self.llm
        output_parser = self.output_parser
        chain = prompt | llm | output_parser
        result = chain.invoke({"jd_text": jd_text})
        return result
