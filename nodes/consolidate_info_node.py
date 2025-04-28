# consolidate info node. This node will take the interview data and the website data and consolidate it into a single data structure using an LLM

from langchain_openai import ChatOpenAI
from state import GraphState
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from models import PortfolioData


def consolidate_info_node(state: GraphState) -> GraphState:
    """Consolidate interview data and website data into a single data structure using an LLM"""
    interview_data = state.get("interview_data")
    portfolio_data = state.get("portfolio_data", PortfolioData())
    is_portfolio = state.get("is_portfolio", False)
    main_company_name = state.get("main_company_name", "Main Company")
    
    # Initialize the OM sections if they don't exist
    om_sections = state.get("om_sections", {})
    
    # Prepare portfolio data for the prompt
    formatted_portfolio_data = ""
    for business_name, website_data in portfolio_data.business_websites.items():
        formatted_portfolio_data += f"\n## {business_name} Website Data:\n"
        formatted_portfolio_data += f"About Us: {website_data.about_us}\n"
        formatted_portfolio_data += f"Website Content: {website_data.website_content}\n\n"

    special_instructions = ""
    if is_portfolio:
        special_instructions = """
        Special Instructions: The data contains information about multiple brands/businesses. Make sure to organize the information by brand/business clearly.
        """
    print(is_portfolio, special_instructions)
    consolidate_data_prompt_template = """
    You are an expert business analyst and writer. Given the following sources of data about the business, merge them into a single source of information. Keep as much information as possible from all sources.
    The business name is {main_company_name}.

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
            "special_instructions": special_instructions,
            "main_company_name": main_company_name
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
