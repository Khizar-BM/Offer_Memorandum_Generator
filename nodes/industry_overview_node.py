from typing import Dict, Any, TypedDict, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from examples import industry_overview_example
from prompts import industry_overview_prompt_template
from state import GraphState



def industry_overview_node(state: GraphState) -> GraphState:
    """Node implementation for generating an OM section"""

    company_context = state.get("company_context", "")
    current_section = "industry_overview"
    
    section_title = ' '.join(word.capitalize() for word in current_section.split('_'))
    
    print(f"Generating {section_title}...")

    example  =  industry_overview_example
    # Combine context
    instructions = """
Make sure to include the company's name in the introduction.
Also ensure that there is not exact duplication of information from the Company Overview section, as duplication hurts SEO.
"""

    
    
    # Create the prompt
    industry_overview_prompt = PromptTemplate(
        input_variables=[],
        partial_variables={"example": example, "instructions": instructions, "context": company_context, "section_title": section_title},
        template=industry_overview_prompt_template,
    )

    
    # Generate the section content
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    chain = industry_overview_prompt | llm | StrOutputParser()
    
    section_content = chain.invoke({})
    
    # Determine the next section
    
      # Update the state with the generated content
    om_sections = {**state.get("om_sections", {})}
    om_sections[current_section] = section_content
    
    return {
        **state,
        "om_sections": om_sections,
        "error": None
    }


