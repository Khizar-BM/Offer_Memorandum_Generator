from typing import Dict, List, Any, TypedDict, Optional, Annotated

from models import  PortfolioData
# Define our state
class GraphState(TypedDict):
    """
    Represents the state of our OM generation graph
    """
    interview_data: str  # Seller interview data
    
    # URLs mapping for businesses
    portfolio_website_urls: Dict[str, List[str]]  # Business name -> URLs mapping for websites
    portfolio_data: PortfolioData  # Consolidated business data
    
    company_context: str  # Consolidated company context
    om_sections: Dict[str, str]  # Generated OM sections
    current_section: str  # Current section being processed
    is_portfolio: bool  # Whether the OM is for multiple businesses
    selected_broker: str  # The selected broker (Website Closers or SellerForce)
    main_company_name: str  # The name of the main/parent company
    error: Optional[str]  # Any error messages
  