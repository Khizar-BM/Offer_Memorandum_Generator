import os
from nodes.about_us_node import about_us_node
from nodes.company_facts_node import company_facts_node
from nodes.company_intro_node import company_intro_node
from nodes.company_summary_node import company_summary_node
from nodes.consolidate_info_node import consolidate_info_node
from nodes.industry_overview_node import industry_overview_node
from nodes.marketplace_content_node import marketplace_content_node
from nodes.save_results_node import save_results_node
from nodes.load_interview_data_node import load_interview_data
from nodes.scaling_opportunity_node import scaling_strategy_node
from nodes.scraping_node import scrape_website_node
from state import GraphState
from dotenv import load_dotenv
# from nodes.website_scraper_node import scrape_website_node, WebsiteScraperInput
from nodes.company_overview_node import company_overview_node
from langgraph.graph import StateGraph, END, START

# Load environment variables
load_dotenv()



# # Define the nodes (steps) in our workflow



# def process_website(state: GraphState) -> GraphState:
#     """Process website data"""
#     website_url = state.get("website_url", "")
    
#     if not website_url:
#         return {**state, "website_data": "", "error": "No website URL provided"}
    
#     # Call the website scraper node
#     scraper_input = {"url": website_url}
#     scraper_result = scrape_website_node(scraper_input)
    
#     if scraper_result["status"] == "error":
#         return {**state, "error": scraper_result["formatted_data"]}
    
#     return {**state, "website_data": scraper_result["formatted_data"], "error": None}



# Build the graph
def build_graph():
    """Create and return the LangGraph workflow"""
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("load_interview_data", load_interview_data)
    workflow.add_node("scrape_website", scrape_website_node)
    workflow.add_node("consolidate_info", consolidate_info_node)
    workflow.add_node("company_overview", company_overview_node)
    workflow.add_node("marketplace_content", marketplace_content_node)
    workflow.add_node("company_intro", company_intro_node)
    workflow.add_node("company_facts", company_facts_node)
    workflow.add_node("scaling_strategy", scaling_strategy_node)
    workflow.add_node("company_summary", company_summary_node)
    workflow.add_node("about_us", about_us_node)
    workflow.add_node("industry_overview", industry_overview_node)
    # workflow.add_node("process_website", process_website)
    workflow.add_node("save_results", save_results_node)
    
    # Add edges - Define the flow
    workflow.add_edge(START, "load_interview_data")
    workflow.add_edge(START, "scrape_website")
    workflow.add_edge("scrape_website", "consolidate_info")
    workflow.add_edge("load_interview_data", "consolidate_info")
    workflow.add_edge("consolidate_info", "company_overview")
    workflow.add_edge("company_overview", "marketplace_content")
    workflow.add_edge("marketplace_content", "company_intro")
    workflow.add_edge("company_intro", "company_facts")
    workflow.add_edge("company_facts", "scaling_strategy")
    workflow.add_edge("scaling_strategy", "company_summary")
    workflow.add_edge("company_summary", "about_us")
    workflow.add_edge("about_us", "industry_overview")
    workflow.add_edge("industry_overview", "save_results")
   
    
    # workflow.add_edge("save_results", END)
    workflow.add_edge("save_results", END)
    
    # Set the entry point
    
    return workflow

