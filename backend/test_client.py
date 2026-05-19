import asyncio
from app.agents.graph import selector_app

async def main():
    sample_html = """
    <div class="login-container">
        <h1>Welcome Back</h1>
        <form>
            <input type="text" id="random-id-843" class="input-field" placeholder="Email Address" 
                   data-testid="email-input" name="email" />
            <input type="password" id="pw-89" class="input-field" placeholder="Password" />
            
            <button type="submit" class="tw-bg-blue-500 tw-text-white tw-p-4 tw-rounded w-full" 
                    id="submit-btn" data-cy="login-submit-button">
                <span>Sign In To The App</span>
            </button>
            <a href="/forgot">Forgot Password?</a>
        </form>
    </div>
    """

    print("Testing Email Input...\n")
    result1 = await selector_app.ainvoke({
        "raw_html": sample_html,
        "target_description": "Email input field",
        "status": "processing"
    })
    
    print("--- Result for Email Input ---")
    if result1.get("status") == "error":
        print(f"Error: {result1.get('error_message')}")
    else:
        print(f"Selectors: {result1.get('generated_selectors')}")
        print(f"\nExplanation:\n{result1.get('explanation')}")
    
    print("\n" + "="*50 + "\n")

    print("Testing Submit Button...\n")
    result2 = await selector_app.ainvoke({
        "raw_html": sample_html,
        "target_description": "Submit Login Button",
        "status": "processing"
    })
    
    print("--- Result for Submit Button ---")
    if result2.get("status") == "error":
        print(f"Error: {result2.get('error_message')}")
    else:
        print(f"Selectors: {result2.get('generated_selectors')}")
        print(f"\nExplanation:\n{result2.get('explanation')}")

if __name__ == "__main__":
    asyncio.run(main())
