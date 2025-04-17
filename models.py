from typing import List
from pydantic import BaseModel, Field


class FactsSheet(BaseModel):

    facts: List[str] = Field(
        description="List of Key Valuation Points about the company. Minimum 5, Maximum 10"
    )

class ScalingStrategy(BaseModel):
    scaling_strategy: str = Field(
        description="A section about the scaling potential of the business. Almost 1 page"
    )
    scaling_opportunities: List[str] = Field(
        description="List of 5-7 key scaling opportunities for the business"
    )

class FireCrawlSchema(BaseModel):
    about_us: str
    website_content: str
    # get it in str
    def __str__(self):
        return f"About Us: {self.about_us}\nWebsite Content: {self.website_content}"

class ReviewsSchema(BaseModel):
    five_star_reviews: List[str] = Field(
        description="List of five-star reviews scraped from various platforms",
        default=[]
    )
    total_count: int = Field(
        description="Total count of five-star reviews found",
        default=0
    )
    
    def __str__(self):
        return f"Five Star Reviews: {len(self.five_star_reviews)}\nTotal Count: {self.total_count}"

