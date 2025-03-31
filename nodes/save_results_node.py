from state import GraphState
import os


def save_results_node(state: GraphState) -> GraphState:
    """Save the generated OM sections to files"""
    om_sections = state.get("om_sections", {})
    print("Generating OM Document...")
    
    if not om_sections:
        return {**state, "error": "No OM sections to save"}
    
    try:
        # Create output directory
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Create a combined file
        with open(f"{output_dir}/full_offer_memorandum.md", "w") as full_om:
            full_om.write("# OFFER MEMORANDUM\n\n")
            
            # Add each section to the full document
            for section_name, content in om_sections.items():
                section_title = ' '.join(word.capitalize() for word in section_name.split('_'))
                
                # Write to individual file
                with open(f"{output_dir}/{section_name}.md", "w") as section_file:
                    section_file.write(f"# {section_title}\n\n")
                    section_file.write(content)
                
                # Add to full document
                full_om.write(f"## {section_title}\n\n")
                full_om.write(f"{content}\n\n")
                full_om.write("---\n\n")
        
        print(f"Offer Memorandum generated successfully in the '{output_dir}' directory.")
        return {**state, "error": None}
    except Exception as e:
        return {**state, "error": f"Failed to save results: {str(e)}"}

