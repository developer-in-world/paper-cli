import requests
from typing import Optional

# SECURITY: Input length ceiling to prevent massive prompts leading to DOS or token exhaustion
MAX_ABSTRACT_LENGTH = 5000 

def summarize_abstract(abstract: str, api_key: Optional[str]) -> str:
    """Summarizes research paper abstract using Mistral."""
    if not api_key:
        return "[dim]No Mistral API key provided. Skipping summary.[/dim]"
        
    if not abstract:
        return "[dim]No abstract available to summarize.[/dim]"
        
    # Input Validation
    if len(abstract) > MAX_ABSTRACT_LENGTH:
        abstract = abstract[:MAX_ABSTRACT_LENGTH] + "... [truncated]"
        
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    prompt = f"Summarize the following research paper abstract in exactly 3 short bullet points:\n- Problem\n- Method\n- Key Contribution\n\nAbstract:\n{abstract}"
    
    payload = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 150
    }
    
    try:
        # SECURITY FIX: Explicit timeout added
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        
        result = response.json()
        choices = result.get('choices', [])
        if not choices:
            return "[red]Empty response from Mistral API.[/red]"
            
        return choices[0].get('message', {}).get('content', '').strip()
        
    except requests.exceptions.RequestException as e:
        return f"[red]Summary Network Error: {e}[/red]"
    except Exception as e:
        return f"[red]Summary Error: {e}[/red]"
