import argparse
import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from fetcher import fetch_arxiv_papers
from code_finder import find_github_repo
from config import get_api_key
from summarizer import summarize_abstract
from storage import init_db, save_paper, search_saved_papers

console = Console()

def setup_keys():
    github_token = get_api_key("GITHUB_TOKEN", "GitHub Personal Access Token is used to avoid rate limits (10 req/min) for repo searches.")
    mistral_apiKey = get_api_key("MISTRAL_API_KEY", "Mistral API Key is used for generating paper summaries.")
    return github_token, mistral_apiKey

def display_paper(title, url, repo, summary, tags=""):
    code_text = f"[Code available on GitHub]({repo['url']}) (⭐ {repo['stars']} Stars)" if repo else "*No open-source code found*"
    tags_text = f"**Tags:** {tags}\n\n" if tags else ""
    content = f"{tags_text}**Paper URL:** {url}\n\n**Code:** {code_text}\n\n**Abstract Summary:**\n{summary}"
    console.print(Panel(Markdown(content), title=f"[bold cyan]{title}[/bold cyan]", border_style="blue", expand=False))

def cmd_search(args, github_token, mistral_token):
    console.print(f"\n[bold blue]Fetching top {args.limit} papers for '{args.query}' from arXiv...[/bold blue]")
    papers = fetch_arxiv_papers(args.query, args.category, args.limit)
    
    if not papers:
        console.print("[red]No papers found or error occurred.[/red]")
        return
        
    console.print(f"[green]Found {len(papers)} papers! Searching for GitHub code and summarizing...[/green]\n")
    
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
    
    for paper in papers:
        repo = find_github_repo(paper['title'], github_token)
        summary = summarize_abstract(paper['abstract'], mistral_token)
        
        display_paper(paper['title'], paper['url'], repo, summary, tags=",".join(tags))
        
        if args.save:
            save_paper(paper, repo, summary, tags)
            console.print("[green][OK] Saved to local knowledge base[/green]\n")
            
    console.print("\n[dim]Run with other keywords to explore more papers![/dim]")

def cmd_saved(args):
    records = search_saved_papers(args.query)
    if not records:
        console.print("[yellow]No saved papers found.[/yellow]")
        return
        
    console.print(f"\n[bold blue]Found {len(records)} saved papers:[/bold blue]\n")
    for row in records:
        repo = {'url': row['github_url'], 'stars': row['github_stars']} if row['github_url'] else None
        display_paper(row['title'], row['url'], repo, row['summary'], row['tags'])

def interactive_mode():
    console.print(Panel("[bold cyan]🧠 Welcome to Paper CLI![/bold cyan]\n[dim]developed by mg[/dim]\n\nYou double-clicked the app, so we launched the interactive research assistant!"))
    
    try:
        github_token, mistral_token = setup_keys()
        
        while True:
            query = input("\nWhat scientific topic do you want to research? (Type 'exit' or press Enter to quit): ").strip()
            if not query or query.lower() in ['exit', 'quit']:
                break
                
            # Build fake args payload
            class Args: pass
            args = Args()
            args.query = query
            args.limit = 3
            args.category = None
            args.save = False
            args.tags = ""
            
            cmd_search(args, github_token, mistral_token)
            
            console.print("\n[dim]Ready for another search![/dim]")
            
    except KeyboardInterrupt:
        pass
    finally:
        print("\n")
        input("Press Enter to close this window...")

def main():
    init_db()
    
    # Auto-detect if user double-clicked the .exe directly from Windows File Explorer
    if len(sys.argv) == 1:
        interactive_mode()
        return
        
    parser = argparse.ArgumentParser(description="Research Paper to Code CLI Tool (developed by mg)")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search arXiv for papers")
    search_parser.add_argument("query", type=str, help="Keyword or category to search for (e.g., 'transformer')")
    search_parser.add_argument("--category", type=str, default=None, help="Optional domain filter (e.g., 'cs.CV', 'cs.LG')")
    search_parser.add_argument("--limit", type=int, default=5, help="Number of papers to fetch")
    search_parser.add_argument("--save", action="store_true", help="Save the fetched results to the local database")
    search_parser.add_argument("--tags", type=str, default="", help="Comma-separated tags to apply when saving")
    
    # Saved command
    saved_parser = subparsers.add_parser("saved", help="View or search saved papers")
    saved_parser.add_argument("query", type=str, nargs="?", default="", help="Optional keyword to filter saved papers by title or tag")
    
    args = parser.parse_args()
    
    if args.command == "search":
        github_token, mistral_token = setup_keys()
        cmd_search(args, github_token, mistral_token)
    elif args.command == "saved":
        cmd_saved(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
