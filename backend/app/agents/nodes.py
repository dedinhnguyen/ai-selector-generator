from bs4 import BeautifulSoup
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import settings
import json
import re

from app.agents.state import SelectorState

def get_llm(temperature=0.1, use_json_format=True):
    """Factory function to get the configured LLM."""
    provider = settings.LLM_PROVIDER.lower()
    
    if provider == "google":
        return ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=temperature
        )
    elif provider == "deepseek":
        return ChatOpenAI(
            model=settings.DEEPSEEK_MODEL,
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
            temperature=temperature
        )
    elif provider == "groq":
        return ChatOpenAI(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            base_url=settings.GROQ_BASE_URL,
            temperature=temperature
        )
    elif provider == "grok":
        return ChatOpenAI(
            model=settings.GROK_MODEL,
            api_key=settings.GROK_API_KEY,
            base_url=settings.GROK_BASE_URL,
            temperature=temperature
        )
    else: # Default to Ollama
        return ChatOllama(
            model=settings.LLM_MODEL, 
            base_url=settings.OLLAMA_BASE_URL, 
            temperature=temperature, 
            format="json" if use_json_format else None
        )

# Initialize LLMs using the factory
llm = get_llm(temperature=0.1, use_json_format=True)
explainer_llm = get_llm(temperature=0.3, use_json_format=False)

def parse_html_node(state: SelectorState) -> SelectorState:
    """Cleans up the raw HTML, removing useless tags and deeply nested SVGs, to save tokens."""
    try:
        raw = state["raw_html"]
        soup = BeautifulSoup(raw, 'lxml')

        # Remove scripts, styles, noscripts
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        
        # Remove paths in svg because they are too long
        for path in soup.find_all('path'):
            path.decompose()

        # Remove inline styles
        for tag in soup.find_all(True):
            if tag.has_attr('style'):
                del tag['style']

        cleaned = str(soup)
        
        # Minify output by removing excessive newlines and spaces
        cleaned = re.sub(r'\n\s*\n', '\n', cleaned)
        
        return {"cleaned_html": cleaned.strip(), "status": "processing"}
    except Exception as e:
        return {"status": "error", "error_message": f"HTML Parsing Error: {str(e)}"}

def generate_selector_node(state: SelectorState) -> SelectorState:
    """Uses LLM to generate the selector strategies in JSON format."""
    if state.get("status") == "error":
        return state

    system_prompt = (
        "You are an expert QA Automation Engineer. Your task is to analyze the provided HTML snippet "
        "and generate robust, reliable locators (XPath, CSS, Playwright, Selenium, Cypress) for the Target Element described by the user.\n"
        "Guidelines:\n"
        "- Prioritize semantic attributes: data-testid, data-cy, aria-label, name, and role.\n"
        "- Avoid fragile auto-generated attributes (like dynamic IDs: id='id-3132') or long chained CSS.\n"
        "- The xpath and cssSelector MUST be valid and unique for the target element within the context provided.\n"
        "- You must output strictly valid JSON with the following structure:\n"
        "{\n"
        "  \"target\": \"<Name of element>\",\n"
        "  \"xpath\": \"<best xpath>\",\n"
        "  \"cssSelector\": \"<best css selector>\",\n"
        "  \"playwright\": \"page.locator('<selector>')\",\n"
        "  \"selenium\": \"By.xpath('<xpath>')\",\n"
        "  \"cypress\": \"cy.get('<selector>')\",\n"
        "  \"confidence\": <float 0.0 to 1.0>\n"
        "}"
    )

    human_prompt = f"""
    HTML Snippet:
    ```html
    {state['cleaned_html']}
    ```

    Target Element Description: {state['target_description']}

    Generate locators in strictly JSON format. Do not add any text outside the JSON block.
    """

    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        response = llm.invoke(messages)
        content = response.content.strip()
        
        # In case the model wrapped it in markdown json block
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        result_json = json.loads(content)
        
        return {"generated_selectors": result_json, "confidence_score": result_json.get("confidence", 0.0), "status": "processing"}
    except Exception as e:
         return {"status": "error", "error_message": f"Selector Generation Error: {str(e)}\nRaw Response: {response.content if 'response' in locals() else 'None'}"}

def explanation_node(state: SelectorState) -> SelectorState:
    """Generates an explanation for why the generated selector is good."""
    if state.get("status") == "error" or not state.get("generated_selectors"):
         return state

    system_prompt = "You are a QA automation expert. Concisely explain (in Vietnamese) why the generated selector is robust and reliable based on the HTML provided."
    
    gen = state["generated_selectors"]
    human_prompt = f"""
    HTML Snippet:
    ```html
    {state['cleaned_html']}
    ```
    
    Generated Selectors:
    {json.dumps(gen, indent=2)}
    
    Explain why these locators (specifically the XPath and CSS) are good and stable for automation testing. Emphasize what attributes were selected to ensure stability (like data-testid, unique text, etc).
    """
    
    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        response = explainer_llm.invoke(messages)
        return {"explanation": response.content, "status": "success"}
    except Exception as e:
        return {"status": "error", "error_message": f"Explanation Error: {str(e)}"}
