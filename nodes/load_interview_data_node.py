from state import GraphState


def load_interview_data(state: GraphState) -> GraphState:
    """Load interview data from state"""
    try:
        # Get interview data from state (provided by user)
        interview_text = state.get("interview_data", "")
        
        # As a fallback, if interview data is not in state (empty),
        # try reading from the file (for backwards compatibility)
        if not interview_text:
            try:
                with open("questions.txt", 'r') as file:
                    interview_text = file.read()
            except Exception:
                # If file reading also fails, just use empty string
                pass
        
        return {"interview_data": interview_text}
    except Exception as e:
        return {"error": f"Failed to load interview data: {str(e)}"}
