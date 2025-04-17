from models import FireCrawlSchema, ReviewsSchema
from state import GraphState
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")


def scrape_website_node(state: GraphState) -> GraphState:
    """Node implementation for scraping a website"""
    urls = state.get("website_urls", [])
    
    # Check if URLs is empty
    if not urls:
        return {"error": "No URLs provided for scraping"}
    
    #    use Firecrawl to scrape the websites with error handling
    try:
        app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        print(f"Scraping {len(urls)} websites...")
        data = app.extract(
            urls, 
            {
                'prompt': 'I need you to extract all the details you can about this business that can be helpful to write an offer memorendum about this business. ',
                'schema': FireCrawlSchema.model_json_schema(),
            }
        )
        print(data)

        website_data = FireCrawlSchema(**data["data"])

        return {"website_data": website_data}
    except Exception as e:
        print(f"Failed to scrape websites: {str(e)}")
        return {"error": f"Failed to scrape websites: {str(e)}"}


def scrape_reviews_node(state: GraphState) -> GraphState:
    """Node implementation for scraping reviews"""
    urls = state.get("review_urls", [])
    
    # Check if URLs is empty
    if not urls:
        # No error, just return empty reviews
        return {"review_data": ReviewsSchema(five_star_reviews=[], total_count=0)}
    
    # Use Firecrawl to scrape reviews with error handling
    try:
        app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        print(f"Scraping {len(urls)} review sites...")
        data = app.extract(
            urls,
            {
                'prompt': 'Extract all five-star reviews for this business. Only include reviews with 5-star ratings.',
                'schema': {
                    "type": "object",
                    "properties": {
                        "five_star_reviews": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        )
        print(data)
        
        # Extract the five-star reviews
        all_reviews = data["data"].get("five_star_reviews", [])
        
        # Create ReviewsSchema instance
        review_data = ReviewsSchema(
            five_star_reviews=all_reviews,
            total_count=len(all_reviews)
        )
        
        return {"review_data": review_data}
    except Exception as e:
        print(f"Failed to scrape reviews: {str(e)}")
        return {"error": f"Failed to scrape reviews: {str(e)}"}


