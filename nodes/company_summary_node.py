from typing import Dict, Any, TypedDict, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from examples import company_summary_example
from prompts import company_summary_prompt_template
from state import GraphState



def company_summary_node(state: GraphState) -> GraphState:
    """Node implementation for generating an OM section"""

    company_context = state.get("company_context", "")
    om_sections = {**state.get("om_sections", {})}
    company_overview = om_sections.get("company_overview", "")
    current_section = "company_summary"
    
    section_title = ' '.join(word.capitalize() for word in current_section.split('_'))
    
    print(f"Generating {section_title}...")

    example  =  company_summary_example
    # Combine context
    instructions = """
Ensure that there is not any information about the company's actual name or anything else that can identify it in the Company Summary.
Also ensure that there is not exact duplication of information from the Company Overview section, as duplication hurts SEO. It should be focused on other things not already included, like scale opportunities, employees and third party contractors and other things either outlined in the context provided --- and of course --- other things it things are prudent to include in a business like this. Keep the summary brief; 3 medium sized paragraphs is ideal.
"""

    
    company_context += f"\n\nCompany Overview:\n{company_overview}"
    
    # Create the prompt
    company_summary_prompt = PromptTemplate(
        input_variables=[],
        partial_variables={"example": example, "instructions": instructions, "context": company_context, "section_title": section_title},
        template=company_summary_prompt_template,
    )

    
    # Generate the section content
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    chain = company_summary_prompt | llm | StrOutputParser()
    
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


