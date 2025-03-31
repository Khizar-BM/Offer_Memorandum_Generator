

from typing import Dict, Any, TypedDict, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from examples import scaling_strategy_example
from models import ScalingStrategy
from prompts import scaling_strategy_prompt_template
from state import GraphState



def scaling_strategy_node(state: GraphState) -> GraphState:
    """Node implementation for generating an OM section"""
    company_context = state.get("company_context", "")

    current_section = "scaling_strategy"
    
    section_title = ' '.join(word.capitalize() for word in current_section.split('_'))
    
    print(f"Generating {section_title}...")

    example  =  scaling_strategy_example
    # Combine context
    
    
    # Create the prompt
    facts_sheet_prompt = PromptTemplate(
        input_variables=[],
        partial_variables={"example": example,"context": company_context, "section_title": section_title},
        template=scaling_strategy_prompt_template,
    )

    
    # Generate the section content
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7).with_structured_output(ScalingStrategy)
    chain = facts_sheet_prompt | llm
    
    section_content : ScalingStrategy = chain.invoke({})
    
    # Determine the next section
    
      # Update the state with the generated content
    om_sections = {**state.get("om_sections", {})}
    om_sections[current_section] = section_content.scaling_strategy
    om_sections["scaling_opportunities"] = "\n> ".join(section_content.scaling_opportunities)
    
    return {
        **state,
        "om_sections": om_sections,
        "next_section": "xyz",
        "error": None
    }


