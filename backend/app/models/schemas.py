# Pydantic response/request models (MatchResponse, etc.)
from pydantic import BaseModel, Field


class ExperienceSchema(BaseModel):
    company: str = Field(..., description="Name of the company")
    role: str = Field(..., description="Role or position held")
    start_date: str = Field(..., description="Start date of the experience")
    end_date: str = Field(..., description="End date of the experience")
    description: str = Field(
        ..., description="Description of responsibilities and achievements"
    )


class EducationSchema(BaseModel):
    institution: str = Field(..., description="Name of the educational institution")
    degree: str = Field(..., description="Degree or qualification obtained")
    start_date: str = Field(..., description="Start date of the education")
    end_date: str = Field(..., description="End date of the education")
    field_of_study: str = Field(..., description="Field of study or major")


class ResumeSchema(BaseModel):
    name: str = Field(..., description="Full name of the candidate")
    email: str = Field(..., description="Email address of the candidate")
    phone_number: str = Field(..., description="Phone number of the candidate")
    hard_skills: list[str] = Field(..., description="List of hard skills")
    soft_skills: list[str] = Field(..., description="List of soft skills")
    experience: list[ExperienceSchema] = Field(
        ..., description="List of work experiences"
    )
    education: list[EducationSchema] = Field(
        ..., description="List of educational qualifications"
    )
