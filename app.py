import os
import streamlit as st
import time
import io
from dotenv import load_dotenv
from om_langgraph import build_graph
from models import PortfolioData
from langgraph.graph import END
from langgraph.types import StreamWriter
import pypdf
from docx import Document

# Load environment variables
load_dotenv()

# Ensure APP_PASSWORD is set, defaulting to "admin" if not found
if "APP_PASSWORD" not in os.environ:
    os.environ["APP_PASSWORD"] = "admin"

# Initialize authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Initialize session state for portfolio businesses
if 'portfolio_businesses' not in st.session_state:
    st.session_state.portfolio_businesses = {}
    
# Initialize current business being edited
if 'current_business' not in st.session_state:
    st.session_state.current_business = ""

# Initialize main company name
if 'main_company_name' not in st.session_state:
    st.session_state.main_company_name = ""

# Initialize broker selection
if 'selected_broker' not in st.session_state:
    st.session_state.selected_broker = "Website Closers"

# Function to handle login
def login():
    # Get password from environment with fallback
    correct_password = os.getenv("APP_PASSWORD")
    
    # If password not found in env, use default "admin"
    if not correct_password:
        correct_password = "admin"
        
    # Compare input with correct password
    if st.session_state.password_input == correct_password:
        st.session_state.authenticated = True
    else:
        st.error("Incorrect password. Please try again.")

# Function to handle logout
def logout():
    st.session_state.authenticated = False
    st.session_state.password_input = ""

# Function to add a business to the portfolio
def add_business():
    business_name = st.session_state.business_name_input
    if business_name and business_name not in st.session_state.portfolio_businesses:
        st.session_state.portfolio_businesses[business_name] = {
            "website_urls": []
        }
        st.session_state.current_business = business_name
        st.session_state.business_name_input = ""

# Function to remove a business from the portfolio
def remove_business(business_name):
    if business_name in st.session_state.portfolio_businesses:
        del st.session_state.portfolio_businesses[business_name]
        if st.session_state.current_business == business_name:
            st.session_state.current_business = ""

# Function to add a URL to the current business
def add_business_url():
    business = st.session_state.current_business
    url = st.session_state.business_url_input
    if business and url and url not in st.session_state.portfolio_businesses[business]["website_urls"]:
        st.session_state.portfolio_businesses[business]["website_urls"].append(url)
        st.session_state.business_url_input = ""

# Function to remove a URL from a business
def remove_business_url(business, url):
    if business in st.session_state.portfolio_businesses and url in st.session_state.portfolio_businesses[business]["website_urls"]:
        st.session_state.portfolio_businesses[business]["website_urls"].remove(url)

# Function to extract text from PDF file
def extract_text_from_pdf(file):
    pdf_reader = pypdf.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

# Function to extract text from DOCX file
def extract_text_from_docx(file):
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Page configuration
st.set_page_config(
    page_title="Offer Memorandum Generator",
    page_icon="📄",
    layout="wide"
)

# Styling
st.markdown("""
<style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 24px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    .info-text {
        font-size: 16px;
        margin-bottom: 20px;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .url-item {
        display: flex;
        align-items: center;
        padding: 8px;
        margin: 4px 0;
        background-color: #f8f9fa;
        border-radius: 4px;
    }
    .url-text {
        flex-grow: 1;
        margin-right: 10px;
    }
    .business-card {
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: rgba(255, 255, 255, 0.05);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .business-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .portfolio-summary {
        background-color: rgba(0, 102, 204, 0.1);
        border: 1px solid rgba(0, 102, 204, 0.2);
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .portfolio-summary-title {
        font-size: 24px;
        font-weight: bold;
        color: #2196F3;
        margin-bottom: 15px;
        border-bottom: 2px solid #2196F3;
        padding-bottom: 8px;
    }
    .business-stat {
        display: flex;
        justify-content: space-between;
        padding: 5px 0;
        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
    }
    .business-stat-label {
        font-weight: 600;
        color: inherit;
    }
    .business-stat-value {
        font-weight: 600;
        color: #2196F3;
    }
    .logout-button {
        position: absolute;
        top: 20px;
        right: 20px;
    }
    /* Hide Streamlit branding and hamburger menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 2rem; }
    
    /* Login page styling */
    div[data-testid="stVerticalBlock"] {
        gap: 0;
    }
    div[data-testid="stForm"] {
        background-color: transparent;
        border: none;
    }
    /* Status banners styling */
    div.stAlert {
        margin: 25px 0;
        border-radius: 6px;
    }
    /* Success banner */
    div[data-baseweb="notification"] {
        margin: 15px 0;
    }
    
    /* Info banner - blue background (for the "No brands added yet" message) */
    div.element-container div.stAlert.st-ae.st-af.st-ag.st-ah.st-ai.st-aj.st-ak.st-al {
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# Login screen if not authenticated
if not st.session_state.authenticated:
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 style="text-align: center; color: white; margin-top: 120px; margin-bottom: 50px;">Offer Memorandum Generator</h1>', unsafe_allow_html=True)
        st.text_input("Enter Password", type="password", key="password_input")
        # Add spacing between password field and login button
        st.markdown('<div style="margin-top: 35px;"></div>', unsafe_allow_html=True)
        st.button("Login", on_click=login, use_container_width=True)
else:
    # Logout button
    with st.container():
        col1, col2 = st.columns([6, 1])
        with col2:
            st.button("Logout", on_click=logout, key="logout_button")
    
    # Header
    st.markdown('<div class="main-title">Offer Memorandum Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-text">Generate professional Offer Memoranda for business acquisitions with AI</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="section-title">Settings</div>', unsafe_allow_html=True)
        
        # Broker selection
        st.session_state.selected_broker = st.selectbox(
            "Select Broker:",
            ["Website Closers", "SellerForce"],
            index=0 if st.session_state.selected_broker == "Website Closers" else 1
        )
        
        # Input method selection
        input_method = st.radio(
            "Select input method:",
            ["Enter Text", "Upload File"]
        )
        
        # Portfolio company toggle
        is_portfolio_company = st.checkbox(
            "Is this for multiple businesses?",
            value=False,
            help="Check this if the OM is for multiple businesses in a portfolio"
        )
        
        # Clear the "Main Business" entry when switching to portfolio mode
        if is_portfolio_company and "Main Business" in st.session_state.portfolio_businesses:
            if len(st.session_state.portfolio_businesses) == 1:  # Only remove if it's the only business
                del st.session_state.portfolio_businesses["Main Business"]
                st.session_state.current_business = ""

    # Main content area
    tab1, tab2 = st.tabs(["Generate OM", "View Results"])

    with tab1:
        st.markdown('<div class="section-title">Input Information</div>', unsafe_allow_html=True)
        
        # Input method handling
        interview_data = ""
        
        if input_method == "Enter Text":
            interview_data = st.text_area(
                "Paste the interview data:",
                height=200,
                help="Paste the transcript of your seller interview here"
            )
        else:  # Upload File
            uploaded_file = st.file_uploader("Upload interview transcript", type=["txt", "docx", "pdf"])
            if uploaded_file is not None:
                try:
                    file_type = uploaded_file.name.split('.')[-1].lower()
                    
                    if file_type == 'txt':
                        interview_data = uploaded_file.getvalue().decode("utf-8")
                    elif file_type == 'pdf':
                        interview_data = extract_text_from_pdf(uploaded_file)
                    elif file_type == 'docx':
                        interview_data = extract_text_from_docx(uploaded_file)
                    
                    st.success(f"File uploaded successfully! Extracted {len(interview_data)} characters.")
                    
                    # Show a preview of the extracted text
                    with st.expander("Preview extracted text"):
                        st.text(interview_data[:500] + "..." if len(interview_data) > 500 else interview_data)
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
        
        # Business data input UI
        st.markdown('<div class="section-title">Business Information</div>', unsafe_allow_html=True)
        
        # Main Company Name input
        st.text_input(
            "Main Company/Parent Company Name:",
            value=st.session_state.main_company_name,
            placeholder="Enter parent company name",
            key="main_company_name",
            help="The parent company or overall business name for the portfolio"
        )
        
        # Add business input - only show in portfolio mode
        if is_portfolio_company:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text_input(
                    "Brand Name:",
                    placeholder="Enter brand name",
                    key="business_name_input"
                )
            with col2:
                st.markdown('<div style="padding-top: 26px;"></div>', unsafe_allow_html=True)
                st.button("Add Brand", on_click=add_business)
        
        # Default to a single business if none added and not in portfolio mode
        if not is_portfolio_company:
            if not st.session_state.portfolio_businesses:
                st.session_state.portfolio_businesses["Main Business"] = {
                    "website_urls": []
                }
                st.session_state.current_business = "Main Business"
            elif "Main Business" not in st.session_state.portfolio_businesses:
                # Create a "Main Business" entry and move existing data to it
                first_business = list(st.session_state.portfolio_businesses.keys())[0]
                st.session_state.portfolio_businesses["Main Business"] = st.session_state.portfolio_businesses[first_business]
                del st.session_state.portfolio_businesses[first_business]
                st.session_state.current_business = "Main Business"
        
        # Business selection for editing
        if st.session_state.portfolio_businesses:
            business_names = list(st.session_state.portfolio_businesses.keys())
            
            # If not portfolio mode and there's only one business, select it automatically
            if not is_portfolio_company and len(business_names) == 1:
                st.session_state.current_business = business_names[0]
                selected_business = business_names[0]
            else:
                # Business selection dropdown - only show in portfolio mode
                if is_portfolio_company:
                    selected_business = st.selectbox(
                        "Select brand to edit:",
                        [""] + business_names,
                        index=0 if st.session_state.current_business == "" else business_names.index(st.session_state.current_business) + 1
                    )
                    
                    if selected_business != st.session_state.current_business:
                        st.session_state.current_business = selected_business
                else:
                    # In non-portfolio mode, just use the default business
                    selected_business = business_names[0]
                    st.session_state.current_business = selected_business
            
            # Display and edit selected business
            if st.session_state.current_business:
                business = st.session_state.current_business
                
                # In portfolio mode, show the business title and remove button
                if is_portfolio_company:
                    st.markdown(f'<div class="business-title">{business}</div>', unsafe_allow_html=True)
                    
                    # Add Remove Business button - only if portfolio mode or not the Main Business
                    if st.button(f"Remove Brand", key=f"remove_{business}"):
                        remove_business(business)
                        st.rerun()
                
                # Website URLs section for this business
                st.markdown("### Website URLs")
                
                # URL input with add button
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text_input(
                        "Website URL:",
                        placeholder="https://example.com",
                        key="business_url_input"
                    )
                with col2:
                    st.markdown('<div style="padding-top: 26px;"></div>', unsafe_allow_html=True)
                    st.button("Add URL", on_click=add_business_url, key="add_business_url")
                
                # Display URLs with remove buttons
                if st.session_state.portfolio_businesses[business]["website_urls"]:
                    for url in st.session_state.portfolio_businesses[business]["website_urls"]:
                        with st.container():
                            col1, col2 = st.columns([0.9, 0.1])
                            with col1:
                                st.text(url)
                            with col2:
                                st.button("Remove", key=f"remove_url_{business}_{url}", on_click=remove_business_url, args=(business, url))
                else:
                    if is_portfolio_company:
                        st.info(f"No website URLs added for this brand yet.")
                    else:
                        st.info("No website URLs added yet.")
        else:
            st.info("No brands added yet. Please add at least one brand.")
        
        # Portfolio Summary - Only show in portfolio mode
        if is_portfolio_company and st.session_state.portfolio_businesses:
            st.markdown('<div class="portfolio-summary">', unsafe_allow_html=True)
            st.markdown('<div class="portfolio-summary-title">Portfolio Summary</div>', unsafe_allow_html=True)
            
            # Display main company name at the top
            st.markdown(f"""
            <div style="margin-bottom: 20px; padding: 10px; background-color: rgba(33, 150, 243, 0.1); border-radius: 5px; border: 1px solid rgba(33, 150, 243, 0.2);">
                <div style="font-size: 18px; font-weight: 600; color: #2196F3; margin-bottom: 5px;">Parent Company:</div>
                <div style="font-size: 20px; font-weight: 700;">{st.session_state.main_company_name}</div>
            </div>
            """, unsafe_allow_html=True)
            
            for business_name, business_data in st.session_state.portfolio_businesses.items():
                st.markdown(f"""
                <div class="business-card">
                    <div class="business-title">{business_name}</div>
                    <div class="business-stat">
                        <span class="business-stat-label">Website URLs:</span>
                        <span class="business-stat-value">{len(business_data["website_urls"])}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Generate button and validation
        generate_button_disabled = False
        
        if not interview_data:
            generate_button_disabled = True
        
        # Validation - need at least one business with at least one website URL
        valid_business = False
        for business, data in st.session_state.portfolio_businesses.items():
            if data["website_urls"]:
                valid_business = True
                break
        
        if not valid_business:
            generate_button_disabled = True
        
        if st.button("Generate Offer Memorandum", type="primary", disabled=generate_button_disabled):
            with st.spinner("Generating Offer Memorandum..."):
                # Progress bar and status updates
                progress_placeholder = st.empty()
                status_placeholder = st.empty()
                progress_placeholder.progress(0)
                
                # Build the graph
                workflow = build_graph()
                app = workflow.compile()
                # app.get_graph().draw_mermaid_png(output_file_path="graph1.png")

                
                # Initialize portfolio data structure
                portfolio_data = PortfolioData()
                
                # Get website URLs from portfolio businesses
                portfolio_website_urls = {
                    business: data["website_urls"] 
                    for business, data in st.session_state.portfolio_businesses.items()
                }
                
                # Initialize with starting state
                initial_state = {
                    "interview_data": interview_data,
                    "portfolio_website_urls": portfolio_website_urls,
                    "portfolio_data": portfolio_data,
                    "om_sections": {},
                    "company_context": "",
                    "current_section": "Company Overview",
                    "is_portfolio": is_portfolio_company,
                    "selected_broker": st.session_state.selected_broker,
                    "main_company_name": st.session_state.main_company_name,
                    "error": None
                }
                
                try:
                    # Stream using custom mode to receive progress_update chunks
                    final_result = None
                    
                    for chunk in app.stream(initial_state, stream_mode="custom"):
                        # Check if this is a progress update chunk
                        if "progress_update" in chunk:
                            update = chunk["progress_update"]
                            status = update.get("status", "")
                            progress = update.get("progress", 0)
                            
                            # Update the UI with progress information
                            if status:
                                status_placeholder.text(f"{status}")
                            
                            progress_placeholder.progress(progress)
                            
                            # Check if this is the final result
                            result = update.get("result")
                            if result and progress >= 0.99:
                                final_result = result
                                progress_placeholder.progress(1.0)
                                status_placeholder.success("Offer Memorandum generated successfully!")
                                st.session_state.om_results = result
                                st.session_state.is_portfolio = is_portfolio_company
                                st.balloons()
                    
                    # If we didn't get a final result from the progress updates,
                    # use the final state from the graph execution
                    if not final_result:
                        # Run one more time to get the final state
                        final_result = app.invoke(initial_state)
                        st.session_state.om_results = final_result
                        st.session_state.is_portfolio = is_portfolio_company
                
                except Exception as e:
                    st.error(f"Error generating OM: {str(e)}")

        st.markdown("""
        <div class="info-text" style="margin-top: 30px;">
            <em>Note: This tool uses AI to generate content based on the information provided.</em>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        if "om_results" in st.session_state:
            result = st.session_state.om_results
            
            if "word_document_path" in result:
                st.success("Offer Memorandum generated successfully!")
                
                # Display download button for the Word document
                with open(result["word_document_path"], "rb") as file:
                    # Get main company name for filename
                    company_name = st.session_state.main_company_name.strip() or "Offer_Memorandum"
                    # Replace spaces and special characters with underscores for filename
                    safe_company_name = ''.join(c if c.isalnum() else '_' for c in company_name)
                    
                    st.download_button(
                        label="Download Word Document",
                        data=file,
                        file_name=f"{safe_company_name}_OM.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                
                # Display each section
                st.markdown("## Generated Sections")
                
                all_sections = [
                    ("Marketplace Overview", "marketplace_overview"),
                    ("Company Introduction", "company_intro"),
                    ("Company Overview", "company_overview"),
                    ("Company Summary", "company_summary"),
                    ("Facts Sheet", "facts_sheet"),
                    ("About Us", "about_us"),
                    ("Scaling Strategy", "scaling_strategy"),
                    ("Scaling Opportunities", "scaling_opportunities"),
                    ("Industry Overview", "industry_overview")
                ]
                
                # Create tabs for each section
                tabs = st.tabs([section[0] for section in all_sections])

                # Get the selected broker from session state
                selected_broker = st.session_state.get("selected_broker", "Website Closers")
                
                for i, (section_name, section_key) in enumerate(all_sections):
                    with tabs[i]:
                        content = result.get("om_sections", {}).get(section_key, "")
                        if content:
                            # Replace "Website Closers" with "SellerForce" in the displayed content if that broker is selected
                            if selected_broker == "SellerForce":
                                content = content.replace("Website Closers", "SellerForce")
                            st.markdown(content)
                        else:
                            st.info(f"No content generated for {section_name}")
            
            elif "error" in result and result["error"]:
                st.error(f"Error: {result['error']}")
            
            else:
                st.warning("Generation completed but no document was produced.")
        
        else:
            st.info("No results to display. Please generate an Offer Memorandum first.") 