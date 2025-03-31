# Offer Memorandum Generator

This agent creates comprehensive Offer Memorandums (OMs) for businesses based on seller interview questions and information scraped from company websites.

## Project Structure

```
.
├── main.py                     # Original application implementation
├── om_langgraph.py             # LangGraph implementation
├── website_scraper.py          # Base website scraper
├── website_scraper_node.py     # LangGraph node for website scraping
├── section_generator_node.py   # LangGraph node for section generation
├── om_generator_graph.py       # Initial LangGraph implementation
├── questions.txt               # Seller interview questions and answers
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables file
└── output/                     # Generated Offer Memorandum files
    ├── executive_summary.md
    ├── business_overview.md
    └── ...
```

## Features

- Loads seller interview data from a text file as context
- Scrapes company websites for additional information
- Generates Offer Memorandum sections step-by-step with LLM
- Each section is generated with an example in the prompt
- Saves each section as separate markdown files and a combined document
- **NEW**: LangGraph implementation for modular, stateful, multi-step workflow

## Setup

1. Clone this repository
2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example` and add your OpenAI API key:
   ```
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

## Usage

### Original Implementation

```
python main.py
```

### LangGraph Implementation (Recommended)

```
python om_langgraph.py
```

The generated Offer Memorandum sections will be saved in the `output` directory.

## LangGraph Implementation

The LangGraph implementation provides several advantages:

1. **Modularity**: Each step in the process is a separate node in the graph
2. **State Management**: All data is passed explicitly between nodes through the graph state
3. **Error Handling**: Robust error handling at each step
4. **Conditional Flows**: The graph can branch based on conditions
5. **Visualization**: The graph structure makes the workflow easy to understand
6. **Extensibility**: Easy to add new nodes or modify the workflow

The workflow has the following nodes:

- `load_interview_data`: Loads the seller interview from a file
- `process_website`: Scrapes the company website and formats the data
- `generate_section`: Generates a specific section of the OM
- `save_results`: Saves the completed OM to the output directory

## Customization

### Adding New Sections

To add new sections to the Offer Memorandum, modify the section order list in `section_generator_node.py`:

```python
section_order = [
    "executive_summary", 
    "business_overview", 
    "product_description", 
    "market_analysis", 
    "financial_information", 
    "operations", 
    "growth_opportunities", 
    "transition_plan",
    "your_new_section"  # Add your new section here
]
```

Then add an example for the new section in `get_section_example`:

```python
section_examples = {
    # ... existing examples ...
    "your_new_section": "This is an example of the new section you're adding."
}
```

### Website Scraping

The website scraper in `website_scraper.py` can be customized to extract specific information from different types of websites. Modify the scraping methods to target the specific HTML elements or content you need.

### Modifying the Workflow

To modify the graph workflow, edit the `build_graph` function in `om_langgraph.py`. You can add new nodes, change edges, or modify conditional logic.

## Limitations

- The website scraper is a basic implementation and may not work for all websites, especially single-page applications or sites with complex JavaScript.
- The quality of the generated content depends on the provided context and examples. 