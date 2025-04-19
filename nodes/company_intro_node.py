from typing import Dict, Any, TypedDict, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from examples import company_intro_example
from prompts import company_intro_prompt_template
from state import GraphState



def company_intro_node(state: GraphState) -> GraphState:
    """Node implementation for generating an OM section"""

    company_context = state.get("company_context", "")
    om_sections = {**state.get("om_sections", {})}
    company_overview = om_sections.get("company_overview", "")
    current_section = "company_intro"
    is_portfolio = state.get("is_portfolio", False)
    
    section_title = ' '.join(word.capitalize() for word in current_section.split('_'))
    
    print(f"Generating {section_title}...")

    example  =  company_intro_example
    # Combine context
    instructions = """
"""

    if is_portfolio:
        instructions += """
        Special Instructions: The data contains information about multiple brands/businesses. Make sure to write accordingly, by taking inspiration from the following example:
        Example:
        This rapidly growing enterprise holds a collection of lucrative eCommerce Brands, with each featuring a flagship product sold only by that brand. Among them are a powerful waist-slimming hosiery brand, four undergarment outlets, two eyelash retailers, and a brand specializing in eyebrow shaping. Most brands are IP protected, with three additional trademarks pending, which will be leveraged to thwart competition.
 
Their distinctive business approach outshines others in the eCommerce space by offering customers an exclusive subscription model, where they can sign up and pay a monthly fee between $30 and $35. Over the span of less than a year, management has elevated the net profit from subscriptions from $40,000 to almost $400,000, achieving margins of 70% and a 60% front-end subscription conversion rate. Modest estimates for 2024 anticipate seller discretionary earnings of over $4 million, with substantial growth potential stemming from additional products included in the booming subscription initiative. Beyond those, the company mainly drives traffic to its various sites via astute Facebook and Instagram ads managed in-house and email and SMS marketing handled by a proficient agency.
 
This efficiently structured enterprise operates with minimal overhead costs, managing day-to-day activities through a highly skilled team committed to remaining with the business post-acquisition. The company boasts impressive metrics, including healthy average order values, 170,000 monthly visitors, and a gigantic email database of over 3 million individuals.
 
The current owners are eager to facilitate a smooth transition for the buyer and maintain open communication until they feel entirely confident. Furthermore, the company has two full-time employees based in the US who are capable of overseeing most business aspects. Immediate scale prospects include launching all brands on Amazon after the success of one and amplifying the ad budget to maximize customer LTV and profitability fully.
        """
    else:
        instructions += """
        Make sure to include the company's name in the introduction.
        """

    
    company_context += f"\n\nCompany Overview:\n{company_overview}"
    
    # Create the prompt
    company_intro_prompt = PromptTemplate(
        input_variables=[],
        partial_variables={"example": example, "instructions": instructions, "context": company_context, "section_title": section_title},
        template=company_intro_prompt_template,
    )

    
    # Generate the section content
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    chain = company_intro_prompt | llm | StrOutputParser()
    
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


