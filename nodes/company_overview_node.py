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
    is_portfolio = state.get("is_portfolio", False)

    current_section = "company_overview"
    
    section_title = ' '.join(word.capitalize() for word in current_section.split('_'))
    
    print(f"Generating {section_title}...")

    example  =  company_overview_example
    # Combine context
    instructions = """
Mention the high level attributes of the company - outlining what the company does and interesting facts about it. Do not mention the company's actual name or anything else that can identify it in the Company Overview because this is also the information that is placed on the website and in email blasts. A buyer cannot see the OM until they have signed a non-disclosure agreement (NDA) .. so everything in the OM is protected until that NDA is signed.
You also have to ALWAYS mention the Business Broker Takeaways  like in the example, which is where we outline the 3 most important things about this company.
"""
    if is_portfolio:
        instructions += """
        Special Instructions: The data contains information about multiple brands/businesses. Make sure to write accordingly, as presented in the example below:
        Example:
        Website Closers® presents an Amazon FBA eCommerce Company operating under 4 separate brands in the Herbal Medicine vertical. The company has blossomed into the lucrative position of the #1 Amazon brand in their niche, benefiting from unique market positioning, high consumer demand, and high barriers to entry.
This deal offers four different brands across different categories: herbal supplements, sanitary products, LED lighting, and their herbal brand. They have an AOV of $25 and over 500 SKUs spread across these different brands and own multiple exclusive molds for their own products to strengthen their competitive edge and product defensibility. No single supplier or customer accounts for more than 15% of their purchases or revenue, reducing dependency risk.

Business Broker Takeaways
1. Full Team in Place. The company has a full operational team in place, which includes, but isn't limited to, 5 product managers, 1 accountant, 5 product designers, and 2 junior account managers. This team handles all design, logistics, procurement, finance, HR, and customer service, allowing ownership to dedicate just a 20-hour workweek to business development, new product ideas, and team calls.
2. Strong Marketing Strategy. The niche that the company's lifestyle brand is based in sees advertising restrictions, which prevent new competitors from scaling quickly. The company has overcome this barrier through a 95% organic sales mix for this brand, reducing their dependence on paid ads and serving as evidence of the popularity of their offerings. Another brand generates 59% of their sales organically. The company also utilizes a polished PPC strategy on Amazon, with the goal of holding the top 5 rankings for key product lines and driving traffic to certain new products.
3. Established Supply Chain. The brand utilizes a fully integrated supply chain with 3PL storage in the US, Germany, and Japan and smooth FBA integration. They also benefit from favorable, pre-negotiated supplier terms, which allow for deferred balance payments after goods are received. This improves their cash flow, which, coupled with their team covering logistics and procurement, makes the fulfillment process much smoother.
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


