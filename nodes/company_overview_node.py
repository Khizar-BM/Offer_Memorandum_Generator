from typing import Dict, Any, TypedDict, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from examples import company_overview_example
from prompts import section_generator_prompt_template
from state import GraphState



def company_overview_node(state: GraphState) -> GraphState:
    """Node implementation for generating an OM section"""
    company_context = state.get("company_context", "")

    current_section = "company_overview"
    
    section_title = ' '.join(word.capitalize() for word in current_section.split('_'))
    
    print(f"Generating {section_title}...")

    example  =  company_overview_example
    # Combine context
    instructions = """
Mention the high level attributes of the company - outlining what the company does and interesting facts about it. Do not mention the company's actual name or anything else that can identify it in the Company Overview because this is also the information that is placed on the website and in email blasts. A buyer cannot see the OM until they have signed a non-disclosure agreement (NDA) .. so everything in the OM is protected until that NDA is signed.
You also have to ALWAYS mention the Business Broker Takeaways  like in the example, which is where we outline the 3 most important things about this company.
"""
    
    
    # Create the prompt
    section_generator_prompt = PromptTemplate(
        input_variables=[],
        partial_variables={"example": example, "instructions": instructions, "context": company_context, "section_title": section_title},
        template=section_generator_prompt_template,
    )

    
    # Generate the section content
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    chain = section_generator_prompt | llm | StrOutputParser()
    
    section_content = chain.invoke({})
    
    # Determine the next section
    
      # Update the state with the generated content
    om_sections = {**state.get("om_sections", {})}
    om_sections[current_section] = section_content
    
    return {
        **state,
        "om_sections": om_sections,
        "next_section": "xyz",
        "error": None
    }


