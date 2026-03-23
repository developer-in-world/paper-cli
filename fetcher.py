import requests
from typing import List, Dict, Optional
import defusedxml.ElementTree as ET
import time

_LAST_REQUEST_TIME = 0.0
_MIN_DELAY = 3.0  # arXiv official policy: 3 seconds between requests

def _execute_query(search_query: str, max_results: int) -> Optional[List[Dict]]:
    global _LAST_REQUEST_TIME
    
    # Enforce strict global rate limits to securely protect user IPs from being banned
    elapsed = time.time() - _LAST_REQUEST_TIME
    if elapsed < _MIN_DELAY:
        time.sleep(_MIN_DELAY - elapsed)
        
    _LAST_REQUEST_TIME = time.time()

    base_url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': search_query,
        'start': 0,
        'max_results': max_results,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        papers = []
        
        for entry in root.findall('atom:entry', namespace):
            title_elem = entry.find('atom:title', namespace)
            summary_elem = entry.find('atom:summary', namespace)
            link_elem = entry.find('atom:id', namespace)
            
            if title_elem is None or summary_elem is None or link_elem is None:
                continue
                
            title = title_elem.text.replace('\n', ' ').strip() if title_elem.text else "Unknown Title"
            summary = summary_elem.text.replace('\n', ' ').strip() if summary_elem.text else ""
            link = link_elem.text.strip() if link_elem.text else ""
            
            authors = [author.find('atom:name', namespace).text for author in entry.findall('atom:author', namespace) if author.find('atom:name', namespace) is not None]
            
            papers.append({
                'title': title,
                'authors': authors,
                'abstract': summary,
                'url': link
            })
            
        return papers
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print(f"\narXiv Rate Limit Exceeded (429)! Please wait 2-3 minutes before trying again.")
        else:
            print(f"HTTP error fetching from arXiv: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching from arXiv: {e}")
        return None
    except ET.ParseError as e:
        print(f"XML parsing error from arXiv: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in fetcher: {e}")
        return None

def fetch_arxiv_papers(query: str, category: Optional[str] = None, max_results: int = 10) -> List[Dict]:
    """Fetches papers from arXiv securely with Google-style fallback logic."""
    if not query or not query.strip():
        return []
        
    query_str = query.strip()
    
    # Phase 1: Try an Exact Phrase Match (Google behavior)
    exact_match_query = f'all:"{query_str}"'
    if category:
        exact_match_query = f'({exact_match_query}) AND cat:{category}'
        
    papers = _execute_query(exact_match_query, max_results)
    
    if papers is None:
        return [] # Network error occurred, abort early
    
    # Phase 2: If successfully connected but 0 matches found, fallback to loose matching
    if len(papers) == 0:
        print("\n[INFO] Exact match not found. Falling back to broad related-words search...")
        
        loose_query = f'all:{query_str}'
        if category:
            loose_query = f'({loose_query}) AND cat:{category}'
            
        fallback_papers = _execute_query(loose_query, max_results)
        return fallback_papers if fallback_papers is not None else []
        
    return papers
