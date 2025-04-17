import os
import streamlit as st
import time
import io
from dotenv import load_dotenv
from om_langgraph import build_graph
from models import FireCrawlSchema
from langgraph.graph import END
from langgraph.types import StreamWriter

# Load environment variables
load_dotenv()

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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title">Offer Memorandum Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="info-text">Generate professional Offer Memoranda for business acquisitions with AI</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="section-title">Settings</div>', unsafe_allow_html=True)
    
    # Input method selection
    input_method = st.radio(
        "Select input method:",
        ["Enter Text", "Upload File"]
    )
    
    # Display and adjust API key
    api_key = os.getenv("OPENAI_API_KEY", "")
    masked_key = "•" * (len(api_key) - 4) + api_key[-4:] if api_key else ""
    
    st.markdown('<div class="section-title">API Configuration</div>', unsafe_allow_html=True)
    st.text(f"OpenAI API Key: {masked_key}")
    
    if st.button("Update API Key"):
        new_key = st.text_input("Enter new OpenAI API Key:", type="password")
        if new_key:
            # Update .env file
            with open(".env", "r") as f:
                env_lines = f.readlines()
            
            with open(".env", "w") as f:
                for line in env_lines:
                    if line.startswith("OPENAI_API_KEY="):
                        f.write(f"OPENAI_API_KEY={new_key}\n")
                    else:
                        f.write(line)
            
            st.success("API Key updated successfully!")
            st.rerun()

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
        uploaded_file = st.file_uploader("Upload interview transcript", type=["txt"])
        if uploaded_file is not None:
            interview_data = uploaded_file.getvalue().decode("utf-8")
            st.success("File uploaded successfully!")
    
    # Website URL
    website_url = st.text_input(
        "Website URL:",
        placeholder="https://example.com",
        help="Enter the business website URL"
    )
    
    # Generate button
    if st.button("Generate Offer Memorandum", type="primary", disabled=not (interview_data and website_url)):
        if not interview_data:
            st.error("Please provide interview data")
        elif not website_url:
            st.error("Please provide a website URL")
        else:
            with st.spinner("Generating Offer Memorandum..."):
                # Progress bar and status updates
                progress_placeholder = st.empty()
                status_placeholder = st.empty()
                progress_placeholder.progress(0)
                
                # Build the graph
                workflow = build_graph()
                app = workflow.compile()
                
                # Initialize with starting state
                initial_state = {
                    "interview_data": interview_data,
                    "website_url": website_url,
                    "website_data": FireCrawlSchema(about_us="", website_content=""),
                    "om_sections": {},
                    "company_context": "",
                    "current_section": "Company Overview",
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
                                st.session_state.last_website = website_url
                                st.balloons()
                    
                    # If we didn't get a final result from the progress updates,
                    # use the final state from the graph execution
                    if not final_result:
                        # Run one more time to get the final state
                        final_result = app.invoke(initial_state)
                        st.session_state.om_results = final_result
                        st.session_state.last_website = website_url
                
                except Exception as e:
                    st.error(f"Error generating OM: {str(e)}")
    
    st.markdown("""
    <div class="info-text" style="margin-top: 30px;">
        <b>How it works:</b><br>
        1. Enter the seller interview data or upload a transcript file<br>
        2. Provide the business website URL for additional information<br>
        3. Click "Generate Offer Memorandum" to create a comprehensive OM<br>
        4. View the generated sections in the "View Results" tab
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title">Generated Offer Memorandum</div>', unsafe_allow_html=True)
    
    if "om_results" in st.session_state:
        results = st.session_state.om_results
        website = st.session_state.last_website
        
        st.markdown(f"**Business Website:** {website}")
        
        # Get the sections from the results
        om_sections = results.get("om_sections", {})
        
        if not om_sections:
            st.warning("No OM sections found in the results")
        else:
            # Create tabs for each section
            section_tabs = st.tabs(list(om_sections.keys()))
            
            for i, (section_name, section_content) in enumerate(om_sections.items()):
                with section_tabs[i]:
                    st.markdown(section_content)
        
        # Check if we have the DOCX file path from the result
        docx_path = results.get("word_document_path", "")
        if docx_path and os.path.exists(docx_path):
            # Read the DOCX file
            with open(docx_path, "rb") as file:
                docx_bytes = file.read()
            
            # Download button for the existing DOCX
            st.download_button(
                label="Download Offer Memorandum (DOCX)",
                data=docx_bytes,
                file_name="offer_memorandum.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        else:
            st.warning("Generated DOCX file not found. Try regenerating the Offer Memorandum.")
    else:
        st.info("No Offer Memorandum has been generated yet. Go to the 'Generate OM' tab to create one.") 