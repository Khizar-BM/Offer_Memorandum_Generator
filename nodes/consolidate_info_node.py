# consolidate info node. This node will take the interview data and the website data and consolidate it into a single data structure using an LLM

from langchain_openai import ChatOpenAI
from state import GraphState
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from models import PortfolioData


def process_reviews(reviews):
    """Process 5-star reviews and format them for inclusion in the OM"""
    if not reviews or len(reviews) < 5:
        return None
    
    # Limit to max 10 reviews to keep it concise
    selected_reviews = reviews[:10]
    
    # Format the reviews as a nicely formatted section with header and formatted content
    reviews_formatted = "### Customer Testimonials\n\n"
    
    for review in selected_reviews:
        reviews_formatted += f"- \"{review}\"\n"
    
    return reviews_formatted


def consolidate_info_node(state: GraphState) -> GraphState:
    """Consolidate interview data and website data into a single data structure using an LLM"""
    interview_data = state.get("interview_data")
    portfolio_data = state.get("portfolio_data", PortfolioData())
    is_portfolio = state.get("is_portfolio", False)
    
    # Initialize the OM sections if they don't exist
    om_sections = state.get("om_sections", {})
    
    # Process reviews from portfolio data and add to OM sections
    for business_name, review_data in portfolio_data.business_reviews.items():
        if review_data and review_data.five_star_reviews and len(review_data.five_star_reviews) >= 5:
            # Process reviews for inclusion in the OM
            business_customer_reviews = process_reviews(review_data.five_star_reviews)
            
            # Add customer reviews to the OM sections with business name if in portfolio mode
            # or without business name if not in portfolio mode
            if business_customer_reviews:
                if is_portfolio:
                    review_key = f"customer_reviews_{business_name}"
                    om_sections[review_key] = f"## {business_name} Customer Reviews\n\n{business_customer_reviews}"
                else:
                    om_sections["customer_reviews"] = business_customer_reviews
    
    # Prepare portfolio data for the prompt
    formatted_portfolio_data = ""
    for business_name, website_data in portfolio_data.business_websites.items():
        formatted_portfolio_data += f"\n## {business_name} Website Data:\n"
        formatted_portfolio_data += f"About Us: {website_data.about_us}\n"
        formatted_portfolio_data += f"Website Content: {website_data.website_content}\n\n"
        
        # Add reviews for this business if available
        if business_name in portfolio_data.business_reviews:
            review_data = portfolio_data.business_reviews[business_name]
            if review_data and review_data.five_star_reviews:
                formatted_portfolio_data += f"Customer Reviews:\n"
                for i, review in enumerate(review_data.five_star_reviews[:10]):  # Limit to 10 reviews
                    formatted_portfolio_data += f"- \"{review}\"\n"
                formatted_portfolio_data += "\n"

    special_instructions = ""
    if is_portfolio:
        special_instructions = """
        Special Instructions: The data contains information about multiple brands/businesses. Make sure to organize the information by brand/business clearly.
        """
    print(is_portfolio, special_instructions)
    consolidate_data_prompt_template = """
    You are an expert business analyst and writer. Given the following sources of data about a business, merge them into a single source of information. Keep as much information as possible from all sources.
    Also clearly identify the name of the business they are trying to sell.
    {special_instructions}
    Seller Interview Data:
    {interview_data}

    Additional Data:
    {portfolio_data}

    """

    # Create the prompt
    consolidate_data_prompt = PromptTemplate(
        input_variables=[],
        partial_variables={
            "interview_data": interview_data, 
            "portfolio_data": formatted_portfolio_data,
            "special_instructions": special_instructions
        },
        template=consolidate_data_prompt_template,
    )

    print("Consolidating data...")
    # Generate the section content
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    chain = consolidate_data_prompt | llm | StrOutputParser()
    
    consolidated_data = chain.invoke({})
    
    return {
        "company_context": consolidated_data,
        "om_sections": om_sections
    }
