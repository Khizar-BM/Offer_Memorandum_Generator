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
from nodes.scraping_node import scrape_website_node, scrape_reviews_node
from nodes.company_overview_node import company_overview_node
from state import GraphState
from dotenv import load_dotenv
from langgraph.types import StreamWriter
from functools import partial
from langgraph.graph import StateGraph, END, START

# Load environment variables
load_dotenv()

# Wrapper functions to add streaming capabilities to nodes
def stream_node_wrapper(node_func, node_name, node_idx, total_nodes, node_descriptions):
    """Wraps a node function to add streaming progress updates"""
    
    def wrapped_node(state: GraphState, writer: StreamWriter = None):
        # Get the human-readable description
        description = node_descriptions.get(node_name, node_name)
        
        # Calculate progress (start of this node)
        progress = node_idx / total_nodes
        
        # Emit progress update at the start
        if writer:
            writer({
                "progress_update": {
                    "status": description,
                    "progress": progress,
                    "node": node_name
                }
            })
        
        # Call the original node function
        result = node_func(state)
        
        # Calculate progress (end of this node)
        progress = min((node_idx + 1) / total_nodes, 0.99)
        
        # Emit progress update at the end
        if writer:
            writer({
                "progress_update": {
                    "status": f"Completed: {description}",
                    "progress": progress,
                    "node": node_name
                }
            })
        
        return result
    
    return wrapped_node

def final_node_wrapper(node_func, node_name, node_descriptions):
    """Wraps the final node to add the complete result to the progress update"""
    
    def wrapped_node(state: GraphState, writer: StreamWriter = None):
        # Get the human-readable description
        description = node_descriptions.get(node_name, node_name)
        
        # Emit progress update at the start
        if writer:
            writer({
                "progress_update": {
                    "status": description,
                    "progress": 0.99,
                    "node": node_name
                }
            })
        
        # Call the original node function
        result = node_func(state)
        
        # Emit final progress update with the complete result
        if writer:
            writer({
                "progress_update": {
                    "status": "Generation Complete",
                    "progress": 1.0,
                    "node": node_name,
                    "result": result
                }
            })
        
        return result
    
    return wrapped_node

# Build the graph
def build_graph():
    """Create and return the LangGraph workflow"""
    workflow = StateGraph(GraphState)
    
    # Node descriptions for human-readable status
    node_descriptions = {
        "load_interview_data": "Loading interview data",
        "scrape_website": "Scraping websites",
        "scrape_reviews": "Scraping customer reviews",
        "consolidate_info": "Consolidating information",
        "company_overview": "Generating Company Overview",
        "marketplace_content": "Generating Marketplace Analysis",
        "company_intro": "Generating Company Introduction",
        "company_facts": "Generating Company Facts",
        "scaling_strategy": "Generating Scaling Strategy",
        "company_summary": "Generating Company Summary",
        "about_us": "Generating About Us",
        "industry_overview": "Generating Industry Overview",
        "save_results": "Saving results"
    }
    
    # Map node names to their function implementations
    node_functions = {
        "load_interview_data": load_interview_data,
        "scrape_website": scrape_website_node,
        "scrape_reviews": scrape_reviews_node,
        "consolidate_info": consolidate_info_node,
        "company_overview": company_overview_node,
        "marketplace_content": marketplace_content_node,
        "company_intro": company_intro_node,
        "company_facts": company_facts_node,
        "scaling_strategy": scaling_strategy_node,
        "company_summary": company_summary_node,
        "about_us": about_us_node,
        "industry_overview": industry_overview_node,
        "save_results": save_results_node
    }
    
    # Define the node order and total count for progress calculation
    node_order = [
        "load_interview_data",
        "scrape_website",
        "scrape_reviews",
        "consolidate_info",
        "company_overview",
        "marketplace_content",
        "company_intro",
        "company_facts",
        "scaling_strategy",
        "company_summary",
        "about_us",
        "industry_overview",
        "save_results"
    ]
    total_nodes = len(node_order)
    
    # Add nodes with streaming wrappers
    for idx, node_name in enumerate(node_order):
        if node_name == "save_results":
            # Special handling for the final node
            wrapped_node = final_node_wrapper(
                node_functions[node_name], 
                node_name, 
                node_descriptions
            )
        else:
            # Regular nodes
            wrapped_node = stream_node_wrapper(
                node_functions[node_name], 
                node_name, 
                idx, 
                total_nodes, 
                node_descriptions
            )
        
        workflow.add_node(node_name, wrapped_node)
    
    # Add edges - Define the flow
    workflow.add_edge(START, "load_interview_data")
    workflow.add_edge(START, "scrape_website")
    workflow.add_edge(START, "scrape_reviews")
    workflow.add_edge("scrape_website", "consolidate_info")
    workflow.add_edge("scrape_reviews", "consolidate_info")
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
    workflow.add_edge("save_results", END)
    
    return workflow

