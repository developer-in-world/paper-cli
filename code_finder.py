import requests
import urllib.parse
from typing import Optional, Dict
from datetime import datetime

def parse_github_date(date_str: str) -> datetime:
    """Safely parses GitHub ISO 8601 datetimes."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return datetime.utcnow()

def find_github_repo(paper_title: str, github_token: Optional[str] = None) -> Optional[Dict]:
    """Searches GitHub for repositories related to the paper securely."""
    if not paper_title or not paper_title.strip():
        return None
        
    base_url = "https://api.github.com/search/repositories"
    query = urllib.parse.quote(paper_title.strip())
    url = f"{base_url}?q={query}&sort=stars&order=desc"
    
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    if github_token:
        headers['Authorization'] = f'token {github_token}'
        
    try:
        # SECURITY FIX: Mandatory timeout added
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('items', [])
        if not items:
            return None
            
        best_repo = None
        best_score = -1
        now = datetime.utcnow()
        
        for item in items[:5]:
            stars = item.get('stargazers_count', 0)
            
            pushed_at_str = item.get('pushed_at', '')
            if pushed_at_str:
                pushed_at = parse_github_date(pushed_at_str)
                days_ago = max(0, (now - pushed_at).days)
                recency_bonus = max(0, 500 - days_ago)
            else:
                recency_bonus = 0
                
            score = stars + recency_bonus
            
            if score > best_score:
                best_score = score
                best_repo = item
                
        if best_repo:
            return {
                'repo_name': best_repo.get('full_name', 'Unknown'),
                'stars': best_repo.get('stargazers_count', 0),
                'url': best_repo.get('html_url', ''),
                'description': best_repo.get('description', '')
            }
        return None
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
             print("[yellow]GitHub API rate limit exceeded. Consider providing a token.[/yellow]")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[red]Network Error searching GitHub: {e}[/red]")
        return None
    except Exception as e:
        print(f"[red]Unexpected error searching GitHub: {e}[/red]")
        return None
