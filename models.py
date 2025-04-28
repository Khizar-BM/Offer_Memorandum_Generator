from typing import List, Dict, Optional
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
    about_us: str = Field(description="About us section from website")
    website_content: str = Field(description="General content from the website")

class BusinessWebsiteData(BaseModel):
    """Website data for a single business"""
    business_name: str = Field(description="Name of the business")
    about_us: str = Field(description="About us section from website")
    website_content: str = Field(description="General content from the website")

class PortfolioData(BaseModel):
    """Data structure for portfolio with multiple businesses"""
    business_websites: Dict[str, BusinessWebsiteData] = Field(
        default_factory=dict,
        description="Website data for each business in the portfolio"
    )

