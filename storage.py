import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
import contextlib

DB_FILE = Path.home() / '.paper_cli_storage.db'

@contextlib.contextmanager
def get_db_connection():
    """Context manager ensuring safe SQLite connections without memory leaks."""
    conn = sqlite3.connect(DB_FILE, timeout=10) # Timeout prevents lock wait infinite hangs
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        with conn: # Handles commit/rollback automatically
            conn.execute('''
                CREATE TABLE IF NOT EXISTS papers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT UNIQUE,
                    authors TEXT,
                    url TEXT,
                    github_url TEXT,
                    github_stars INTEGER,
                    summary TEXT,
                    tags TEXT
                )
            ''')

def save_paper(paper: Dict, repo: Optional[Dict], summary: str, tags: List[str] = None):
    if not paper or 'title' not in paper:
        return
        
    try:
        authors_str = ", ".join(paper.get('authors', [])) if paper.get('authors') else ""
        tags_str = ", ".join(tags) if tags else ""
        
        with get_db_connection() as conn:
            with conn: 
                conn.execute('''
                    INSERT OR REPLACE INTO papers 
                    (title, authors, url, github_url, github_stars, summary, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(paper.get('title', 'Unknown')), 
                    authors_str, 
                    str(paper.get('url', '')), 
                    str(repo['url']) if repo and 'url' in repo else None,
                    int(repo['stars']) if repo and 'stars' in repo else 0,
                    str(summary) if summary else "",
                    tags_str
                ))
    except sqlite3.Error as e:
        print(f"Database error while saving paper: {e}")
    except Exception as e:
        print(f"Failed to save paper: {e}")

def search_saved_papers(query: str = "") -> List[Dict]:
    results = []
    try:
        with get_db_connection() as conn:
            if query and query.strip():
                # Input Validation & Safe parameterized queries
                safe_query = f'%{query.strip()}%'
                cursor = conn.execute('''
                    SELECT * FROM papers 
                    WHERE title LIKE ? OR tags LIKE ? 
                    ORDER BY id DESC
                    LIMIT 100
                ''', (safe_query, safe_query))
            else:
                cursor = conn.execute('SELECT * FROM papers ORDER BY id DESC LIMIT 50')
                
            results = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error while searching: {e}")
        
    return results
