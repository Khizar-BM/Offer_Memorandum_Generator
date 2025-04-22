from typing import List

from pydantic import BaseModel
from models import FireCrawlSchema, BusinessWebsiteData, BusinessReviewData, PortfolioData
from state import GraphState
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")


def scrape_website_node(state: GraphState) -> GraphState:
    """Node implementation for scraping websites"""
    # Get URLs from portfolio sources
    portfolio_urls = state.get("portfolio_website_urls", {})
    
    # Initialize portfolio data if it doesn't exist
    portfolio_data = state.get("portfolio_data", PortfolioData())
    result = {}
    
    try:
        app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        
        # Process portfolio URLs
        for business_name, urls in portfolio_urls.items():
            if not urls:
                continue
                
            try:
                print(f"Scraping {len(urls)} websites for business: {business_name}...")
                data = app.extract(
                    urls, 
                    {
                        'prompt': f'I need you to extract all the details you can about the business that can be helpful to write an offer memorendum. Identify this business specific information.',
                        'schema': FireCrawlSchema.model_json_schema(),
                    }
                    )
                
                # Add business data to portfolio
                business_data = BusinessWebsiteData(
                    business_name=business_name,
                    about_us=data["data"]["about_us"],
                    website_content=data["data"]["website_content"]
                )
                portfolio_data.business_websites[business_name] = business_data
                
            except Exception as e:
                print(f"Failed to scrape website for business: {business_name}. Error: {str(e)}")
                continue
            
          
        
        # Add portfolio data to result
        result["portfolio_data"] = portfolio_data
        return result
        
    except Exception as e:
        print(f"Failed to scrape websites: {str(e)}")
        return {"error": f"Failed to scrape websites: {str(e)}"}


def scrape_reviews_node(state: GraphState) -> GraphState:
    """Node implementation for scraping reviews"""
    # Get URLs from portfolio sources
    portfolio_review_urls = state.get("portfolio_review_urls", {})
    # Get portfolio data from previous node
    portfolio_data = state.get("portfolio_data", PortfolioData())
    result = {}

    class ReviewData(BaseModel):
        reviews: List[str]
    
    try:
        app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        
        # Process portfolio review URLs
        for business_name, urls in portfolio_review_urls.items():
            if not urls:
                continue

            try:
                print(f"Scraping {len(urls)} review sites for business: {business_name}...")
                data = app.extract(
                    urls,
                    {
                        'prompt': "Get all reviews from this page. After that, filter them by 5 star ratings if ratings are available",
                        'schema': ReviewData.model_json_schema()
                    }
                )
                
                # Extract the five-star reviews
                all_reviews = data["data"].get("reviews", [])
                
                # Add business reviews to portfolio
                business_reviews = BusinessReviewData(
                    business_name=business_name,
                    five_star_reviews=all_reviews
                )
                portfolio_data.business_reviews[business_name] = business_reviews

            except Exception as e:
                print(f"Failed to scrape reviews for business: {business_name}. Error: {str(e)}")
                continue
            
       
    
        # Add portfolio data to result
        result["portfolio_data"] = portfolio_data
        return result
        
    except Exception as e:
        print(f"Failed to scrape reviews: {str(e)}")
        return {"error": f"Failed to scrape reviews: {str(e)}"}


