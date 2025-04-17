# Offer Memorandum Generator

This application generates comprehensive and professional Offer Memoranda for business acquisition opportunities using AI, web scraping, and structured document generation.

## Features

- Automated web scraping of business websites
- AI-powered document generation
- Integration with interview data
- Comprehensive analysis of business opportunities
- User-friendly interface

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   LANGCHAIN_API_KEY=your_langchain_api_key
   LANGCHAIN_PROJECT=your_langchain_project
   LANGCHAIN_TRACING_V2=true
   ```

## Usage

### Command Line Interface

Run the application via command line:

```bash
python main.py
```

### Web Interface

1. Start the Streamlit web application:
   ```bash
   streamlit run app.py
   ```

2. Access the web interface in your browser at http://localhost:8501

3. Using the web interface:
   - Enter seller interview data directly or upload a transcript file
   - Provide the business website URL
   - Click "Generate Offer Memorandum" to start the process
   - View the generated OM sections in the "View Results" tab
   - Download the complete OM document

## Project Structure

- `main.py`: Command-line entry point for the application
- `app.py`: Streamlit web interface
- `om_langgraph.py`: LangGraph workflow definition
- `models.py`: Data models
- `state.py`: State management for the workflow
- `prompts.py`: AI prompt templates
- `examples.py`: Example data
- `nodes/`: Individual processing nodes for the OM generation workflow
- `output/`: Generated OM documents

## Workflow

The OM generation process follows these steps:

1. Load interview data from the user input
2. Scrape the business website for additional information
3. Consolidate all available information
4. Generate the following OM sections:
   - Company Overview
   - Marketplace Analysis
   - Company Introduction
   - Company Facts
   - Scaling Strategy
   - Company Summary
   - About Us
   - Industry Overview
5. Save the final OM document

## Notes

- The application requires an active internet connection for web scraping and API access
- OpenAI API usage incurs costs based on your account's pricing plan
- The quality of the generated OM depends on the quality of the input data

## License

[License information] 