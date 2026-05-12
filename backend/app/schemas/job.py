import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

class JobExtractedData(BaseModel):
    title: str = Field(..., min_length=2, description="The title of the job")
    company: Optional[str] = Field(None, description="The company offering the job")
    min_salary: Optional[int] = Field(None, description="The minimum salary for the job")
    max_salary: Optional[int] = Field(None, description="The maximum salary for the job")
    currency: Optional[str] = Field(None, description="The currency of the salary")
    years_of_experience: Optional[int] = Field(None, description="The years of experience required for the job")
    english_level: Optional[str] = Field(None, description="The English level required for the job")
    modality: Optional[str] = Field(None, description="The modality of the job")
    technologies: List[str] = Field(default_factory=list, min_length=1, description="The technologies required for the job")


class JobCreateRequest(BaseModel):
    text: str
    original_url: Optional[str] = None


class TechnologyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    company: Optional[str]
    min_salary: Optional[int]
    max_salary: Optional[int]
    currency: Optional[str]
    years_of_experience: Optional[int]
    english_level: Optional[str]
    modality: Optional[str]
    original_url: Optional[str]
    created_at: datetime.datetime
    technologies: List[TechnologyResponse]

class JobScrapeRequest(BaseModel):
    url: str