from langgraph.graph import StateGraph, START, END
from app.agents.state import SelectorState
from app.agents.nodes import parse_html_node, generate_selector_node, explanation_node

def build_graph():
    workflow = StateGraph(SelectorState)
    
    workflow.add_node("parser", parse_html_node)
    workflow.add_node("generator", generate_selector_node)
    workflow.add_node("explainer", explanation_node)
    
    workflow.add_edge(START, "parser")
    
    def check_parser(state: SelectorState):
        if state.get("status") == "error":
            return "end"
        return "generate"
        
    workflow.add_conditional_edges("parser", check_parser, {"end": END, "generate": "generator"})
    
    def check_generator(state: SelectorState):
        if state.get("status") == "error":
            return "end"
        return "explain"
        
    workflow.add_conditional_edges("generator", check_generator, {"end": END, "explain": "explainer"})
    
    workflow.add_edge("explainer", END)
    
    return workflow.compile()

selector_app = build_graph()
