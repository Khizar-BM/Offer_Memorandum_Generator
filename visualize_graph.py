import os
from om_langgraph import build_graph

def visualize_graph():
    """Generate a visualization of the LangGraph workflow"""
    # Build the graph
    workflow = build_graph()
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Generate the visualization
    try:
        workflow.to_diagram("output/graph_visualization.png")
        print("Graph visualization saved to: output/graph_visualization.png")
    except Exception as e:
        print(f"Failed to generate visualization: {e}")
        print("Note: You may need to install the required dependencies for visualization:")
        print("pip install pygraphviz")
        print("or")
        print("pip install networkx pydot")

if __name__ == "__main__":
    visualize_graph() 