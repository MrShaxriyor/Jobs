from pydantic import BaseModel

class Job(BaseModel):
    title: str
    company: str
    salary: float
    description: str