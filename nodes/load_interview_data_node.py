from state import GraphState


def load_interview_data(state: GraphState) -> GraphState:
    """Load interview data from file and store in state"""
    try:
        with open("questions.txt", 'r') as file:
            interview_text = file.read()
        
        return {"interview_data": interview_text}
    except Exception as e:
        return {"error": f"Failed to load interview data: {str(e)}"}
