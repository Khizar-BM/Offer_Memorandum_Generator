from models import FireCrawlSchema
from state import GraphState
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")


def scrape_website_node(state: GraphState) -> GraphState:
    """Node implementation for scraping a website"""
    url = state.get("website_url")
    #    use Firecrawl to scrape the website with error handling
    try:
        app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        print("Scraping website...")
        data = app.extract([
        url
        ], {
            'prompt': 'I need you to extract all the details you can about this business that can be helpful to write an offer memorendum about this business. ',
            'schema': FireCrawlSchema.model_json_schema(),
        })
        print(data)


        website_data = FireCrawlSchema(**data["data"])

        return {"website_data": website_data}
    except Exception as e:
        print(f"Failed to scrape website: {str(e)}")
        return {"error": f"Failed to scrape website: {str(e)}"}


