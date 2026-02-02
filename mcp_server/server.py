import os
from fastmcp import FastMCP
from github import Github
from dotenv import load_dotenv

load_dotenv()
mcp = FastMCP("GitHub-Tools")
gh = Github(os.getenv("GITHUB_TOKEN"))

@mcp.tool()
def search_repositories(query: str):
    """Search for GitHub repositories by name or keyword."""
    repos = gh.search_repositories(query)[:5]
    return [{"name": r.full_name, "description": r.description, "stars": r.stargazers_count} for r in repos]

@mcp.tool()
def get_repo_details(repo_name: str):
    """Get detailed info about a specific repo (e.g., 'owner/repo')."""
    repo = gh.get_repo(repo_name)
    return {
        "full_name": repo.full_name,
        "description": repo.description,
        "language": repo.language,
        "open_issues": repo.open_issues_count,
        "forks": repo.forks_count
    }
if __name__=="__main__":
    mcp.run(transport="stdio")
