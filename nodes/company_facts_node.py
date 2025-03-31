from typing import Dict, Any, TypedDict, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from examples import company_facts_example
from models import FactsSheet
from prompts import facts_sheet_prompt_template
from state import GraphState



def company_facts_node(state: GraphState) -> GraphState:
    """Node implementation for generating an OM section"""
    company_context = state.get("company_context", "")
    current_section = "facts_sheet"
    
    section_title = ' '.join(word.capitalize() for word in current_section.split('_'))
    
    print(f"Generating {section_title}...")

    example  =  company_facts_example
    # Combine context
    

    
    # Create the prompt
    facts_sheet_prompt = PromptTemplate(
        input_variables=[],
        partial_variables={"example": example,"context": company_context, "section_title": section_title},
        template=facts_sheet_prompt_template,
    )

    
    # Generate the section content
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7).with_structured_output(FactsSheet)
    chain = facts_sheet_prompt | llm
    
    section_content : FactsSheet = chain.invoke({})
    
    # Determine the next section
    
      # Update the state with the generated content
    om_sections = {**state.get("om_sections", {})}
    om_sections[current_section] = "| ".join(section_content.facts)
    
    return {
        **state,
        "om_sections": om_sections,
        "next_section": "xyz",
        "error": None
    }


