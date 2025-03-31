# consolidate info node. This node will take the interview data and the website data and consolidate it into a single data structure using an LLM

from langchain_openai import ChatOpenAI
from state import GraphState
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate



def consolidate_info_node(state: GraphState) -> GraphState:
    """Consolidate interview data and website data into a single data structure using an LLM"""
    interview_data = state.get("interview_data")
    fireCrawlData = state.get("website_data")
    website_data = f"""
    About Us: {fireCrawlData.about_us}
    Website Content: {fireCrawlData.website_content}
"""

    consolidate_data_prompt_template = """
    You are an expert business analyst and writer. Given the following 2 sources of data about a business, merge them into a single source of information. Keep as much information as possible from both sources.

    Seller Interview Data:
    {interview_data}

    Website Data:
    {website_data}
    """

  # Create the prompt
    consolidate_data_prompt = PromptTemplate(
        input_variables=[],
        partial_variables={"interview_data": interview_data, "website_data": website_data},
        template=consolidate_data_prompt_template,
    )

    print("Consolidating data...")
        # Generate the section content
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    chain = consolidate_data_prompt | llm | StrOutputParser()
    
    consolidated_data = chain.invoke({})
    return {"company_context": consolidated_data}
