# consolidate info node. This node will take the interview data and the website data and consolidate it into a single data structure using an LLM

from langchain_openai import ChatOpenAI
from state import GraphState
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate


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
    fireCrawlData = state.get("website_data")
    reviewData = state.get("review_data", None)
    
    website_data = f"""
    About Us: {fireCrawlData.about_us}
    Website Content: {fireCrawlData.website_content}
"""

    # Prepare reviews section if we have enough 5-star reviews
    reviews_section = ""
    customer_reviews = None
    
    if reviewData and reviewData.total_count >= 5:
        reviews_list = "\n".join([f"- \"{review}\"" for review in reviewData.five_star_reviews])
        reviews_section = f"""
    Customer Reviews:
    {reviews_list}
"""
        # Process reviews for inclusion in the OM
        customer_reviews = process_reviews(reviewData.five_star_reviews)

    consolidate_data_prompt_template = """
    You are an expert business analyst and writer. Given the following sources of data about a business, merge them into a single source of information. Keep as much information as possible from all sources.

    Seller Interview Data:
    {interview_data}

    Website Data:
    {website_data}
    
    {reviews_section}
    """

    # Create the prompt
    consolidate_data_prompt = PromptTemplate(
        input_variables=[],
        partial_variables={
            "interview_data": interview_data, 
            "website_data": website_data,
            "reviews_section": reviews_section
        },
        template=consolidate_data_prompt_template,
    )

    print("Consolidating data...")
    # Generate the section content
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    chain = consolidate_data_prompt | llm | StrOutputParser()
    
    consolidated_data = chain.invoke({})
    
    # Initialize the OM sections if they don't exist
    om_sections = state.get("om_sections", {})
    
    # Add customer reviews to the OM sections if available
    if customer_reviews:
        om_sections["customer_reviews"] = customer_reviews
    
    return {
        "company_context": consolidated_data,
        "om_sections": om_sections
    }
