from pydantic import BaseModel, Field


class ResearchResponse(BaseModel):
    """Structured response from the research assistant."""

    answer: str = Field(description="The answer to the question")
    confidence: str = Field(description="high, medium, or low based on source quality")
    sources: list[str] = Field(description="list of source documents used")
    key_quotes: list[str] = Field(
        description="Relevant quotes from sources", default=[]
    )
    follow_up_questions: list[str] = Field(description="Suggested follow-up questions")
