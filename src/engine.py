import os
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def run_inference_prompt(prompt: str, temperature: float = 0.7, max_tokens: int = 512) -> str:
    """
    Unified Groq Engine.
    This replaces the local model inference from the original script.
    """
    system_message = (
        "You are a professional Mock Trial Legal Assistant. "
        "STRICT RULES: 1. Do not repeat yourself. 2. Be concise. "
        "3. If you finish your point, stop immediately. 4. Never loop phrases."
    )
    
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            # Use the instant model for sub-2-second responses
            model="llama-3.1-8b-instant", 
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"
