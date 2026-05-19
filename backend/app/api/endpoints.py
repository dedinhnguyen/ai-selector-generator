from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any, Dict
from app.agents.graph import selector_app

router = APIRouter()

class GenerationRequest(BaseModel):
    raw_html: str
    target_description: str

class GenerationResponse(BaseModel):
    status: str
    error_message: Optional[str] = None
    cleaned_html: Optional[str] = None
    selectors: Optional[Dict[str, Any]] = None
    explanation: Optional[str] = None
    confidence: Optional[float] = None

@router.post("/generate", response_model=GenerationResponse)
async def generate_selectors(request: GenerationRequest):
    initial_state = {
        "raw_html": request.raw_html,
        "target_description": request.target_description,
        "status": "processing"
    }
    
    try:
        # LangGraph invoke returns a dict corresponding to the final state
        final_state = await selector_app.ainvoke(initial_state)
        
        if final_state.get("status") == "error":
            raise HTTPException(status_code=400, detail=final_state.get("error_message"))
            
        return GenerationResponse(
            status="success",
            cleaned_html=final_state.get("cleaned_html"),
            selectors=final_state.get("generated_selectors"),
            explanation=final_state.get("explanation"),
            confidence=final_state.get("confidence_score")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
