from typing import Dict, Any, TypedDict, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from prompts import about_us_prompt_template
from state import GraphState



def about_us_node(state: GraphState) -> GraphState:
    """Node implementation for generating an OM section"""
    company_context = state.get("company_context", "")
    current_section = "about_us"
    
    section_title = ' '.join(word.capitalize() for word in current_section.split('_'))
    
    print(f"Generating {section_title}...")


    
    # Create the prompt
    about_us_prompt = PromptTemplate(
        input_variables=[],
        partial_variables={"context": company_context},
        template=about_us_prompt_template,
    )

    
    # Generate the section content
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    chain = about_us_prompt | llm | StrOutputParser()
    
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

