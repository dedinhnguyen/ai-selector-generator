from typing import TypedDict, Optional, Any, Dict

class SelectorState(TypedDict):
    raw_html: str
    target_description: str
    cleaned_html: Optional[str]
    generated_selectors: Optional[Dict[str, Any]]
    explanation: Optional[str]
    confidence_score: Optional[float]
    status: str
    error_message: Optional[str]
