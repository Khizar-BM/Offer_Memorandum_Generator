section_generator_prompt_template = """
    You are an expert writer used to generating Offer Memorandums. You are tasked with creating the {section_title} section of an Offer Memorandum for a business.
    
    Use the following context about the business:
    {context}
    
    Here is an example of a {section_title} section. Make sure to follow the same format and writing style:
    {example}
    
    Here are the instructions specific to the {section_title} section:
    {instructions}
    """
    

facts_sheet_prompt_template = """
    You are an expert writer used to generating Offer Memorandums. You are tasked writing a list of Key Valuation Points for a business.
    
    Use the following context about the business:
    {context}
    
    Here is an example of a some key valuation points. Make sure to follow the same format and writing style:
    {example}
    
    Return the facts in a list of strings.

    ONLY WRITE 5-7 KEY VALUATION POINTS.
    
    """

scaling_strategy_prompt_template = """
    You are an expert writer and analyst used to generating Offer Memorandums. You are tasked with identifying the key methods for scaling a particular business business.
    
    Use the following context about the business:
    {context}
    
    Here is an example of a Scaling Strategy section. Make sure to follow the same format and writing style:
    {example}
    
   You need to write a section about it (almost 1 page) and also return a list of 5-7 key scaling opportunities for the business.
    
    """




company_summary_prompt_template = """
    You are an expert writer used to generating Offer Memorandums. You are tasked with creating the Company Summary section of an Offer Memorandum for a business.
    
    Use the following context about the business:
    {context}

    Here is an example of a Company Summary section. Make sure to follow the same format and writing style:
    {example}
    
    Here are the instructions specific to the Company Summary section:
    {instructions}
    
    """

company_intro_prompt_template = """
    You are an expert writer used to generating Offer Memorandums. You are tasked with creating the Company Introduction section of an Offer Memorandum for a business.
    Highlight the strengths of the business.
    
    Use the following context about the business:
    {context}

    Here is an example of a Company Introduction section. Make sure to follow the same format and writing style:
    {example}
    
    Here are the instructions specific to the Company Introduction section:
    {instructions}
    
    """

marketplace_overview_prompt_template = """
    You are an expert writer used to generating Offer Memorandums. Given the following context about a business, write a Marketplace Content section for an Offer Memorandum.
    
    Use the following context about the business:
    {context}

    Here is an example of a Marketplace Content section. Make sure to follow the same format and writing style as the example:
    {example}
    
    Here are the instructions specific to the Marketplace Content section:
    {instructions}
    
    """

about_us_prompt_template = """
    You are an expert business analyst and writer. Given the following context about a business, write an About Us section as it would appear on a website. Don't make it longer than 2 paragraphs.
    
    Use the following context about the business:
    {context}
    
    """

industry_overview_prompt_template = """
    You are an expert business analyst and writer. Given the following context about a business, write an overview about that industry.
    
    Use the following context about the business:
    {context}
    
    Here is an example of an Industry Overview. Make sure to follow the same format and writing style as the example:
    {example}

    """
