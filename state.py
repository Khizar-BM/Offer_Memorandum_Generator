from typing import Dict, List, Any, TypedDict, Optional, Annotated

from models import FireCrawlSchema
# Define our state
class GraphState(TypedDict):
    """
    Represents the state of our OM generation graph
    """
    interview_data: str  # Seller interview data
    website_url: str  # URL to scrape
    website_data: FireCrawlSchema  # Formatted website data
    company_context: str  # Consolidated company context
    om_sections: Dict[str, str]  # Generated OM sections
    current_section: str  # Current section being processed
    error: Optional[str]  # Any error messages
