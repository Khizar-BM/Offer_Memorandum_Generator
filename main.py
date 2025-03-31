
from dotenv import load_dotenv
from langsmith import traceable
from models import FireCrawlSchema
from om_langgraph import build_graph

from IPython.display import Image, display


# load the environment variables
load_dotenv()

@traceable
def main():
    """Run the OM generator graph"""
    # Build the graph
    workflow = build_graph()
    
    # Compile the graph
    app = workflow.compile()
    app.get_graph().draw_mermaid_png(output_file_path="graph.png")

    
    # Initialize with starting state
    initial_state = {
        "interview_data": "",
        "website_url": "https://www.shoptheboutique.com",  # Example URL from the interview
        "website_data": FireCrawlSchema(about_us="", website_content=""),
        "om_sections": {},
        "company_context": "",
        "current_section": "Company Overview",
        "error": None
    }
    
    # Execute the graph
    # for output in app.stream(initial_state, stream_mode="updates"):
    #     print(output)
    output = app.invoke(initial_state)
    
    print("Offer Memorandum generation complete!")


if __name__ == "__main__":
    main() 