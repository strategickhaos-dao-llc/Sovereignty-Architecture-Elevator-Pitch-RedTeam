"""
Git repository tools - Access file history, logs, and create snippets
"""
import subprocess
from pathlib import Path
from pydantic import BaseModel, Field
import yaml

# Load configuration
config_path = Path(__file__).parent.parent / "config.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

DEFAULT_REPO = Path(config.get("git", {}).get("default_repo_path", "/workspace"))


class GetFileAtCommitArgs(BaseModel):
    """Arguments for getting a file at a specific commit"""
    file_path: str = Field(description="Path to the file relative to repo root")
    commit_sha: str = Field(description="Git commit SHA or ref (e.g., 'HEAD', 'main', commit hash)")
    repo_path: str | None = Field(default=None, description="Optional repository path. Uses default if not specified")


class GitLogSummaryArgs(BaseModel):
    """Arguments for getting git log summary"""
    file_path: str | None = Field(default=None, description="Optional file path to get log for specific file")
    max_commits: int = Field(default=10, description="Maximum number of commits to include")
    repo_path: str | None = Field(default=None, description="Optional repository path. Uses default if not specified")


class CreateSnippetArgs(BaseModel):
    """Arguments for creating a code snippet from git"""
    file_path: str = Field(description="Path to the file")
    start_line: int = Field(description="Starting line number (1-indexed)")
    end_line: int = Field(description="Ending line number (inclusive)")
    commit_sha: str = Field(default="HEAD", description="Git commit SHA or ref")
    repo_path: str | None = Field(default=None, description="Optional repository path. Uses default if not specified")


def get_file_at_commit(args: GetFileAtCommitArgs) -> str:
    """Get the content of a file at a specific git commit."""
    repo_path = Path(args.repo_path) if args.repo_path else DEFAULT_REPO
    
    try:
        result = subprocess.run(
            ["git", "show", f"{args.commit_sha}:{args.file_path}"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}"
        
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: Git command timed out"
    except Exception as e:
        return f"Error executing git command: {str(e)}"


def git_log_summary(args: GitLogSummaryArgs) -> str:
    """Get a summary of recent git commits."""
    repo_path = Path(args.repo_path) if args.repo_path else DEFAULT_REPO
    
    try:
        cmd = [
            "git", "log",
            f"-{args.max_commits}",
            "--pretty=format:%h - %s (%an, %ar)",
            "--abbrev-commit"
        ]
        
        if args.file_path:
            cmd.append("--")
            cmd.append(args.file_path)
        
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}"
        
        if not result.stdout.strip():
            return "No commits found"
        
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: Git command timed out"
    except Exception as e:
        return f"Error executing git command: {str(e)}"


def create_snippet(args: CreateSnippetArgs) -> str:
    """Create a code snippet from a file at a specific commit with line numbers."""
    repo_path = Path(args.repo_path) if args.repo_path else DEFAULT_REPO
    
    try:
        # Get the full file content
        result = subprocess.run(
            ["git", "show", f"{args.commit_sha}:{args.file_path}"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}"
        
        lines = result.stdout.split('\n')
        total_lines = len(lines)
        
        # Validate line numbers
        if args.start_line < 1 or args.end_line > total_lines:
            return f"Error: Invalid line range. File has {total_lines} lines"
        
        if args.start_line > args.end_line:
            return "Error: start_line must be less than or equal to end_line"
        
        # Extract the snippet with line numbers
        snippet_lines = []
        for i in range(args.start_line - 1, args.end_line):
            snippet_lines.append(f"{i + 1:4d}. {lines[i]}")
        
        header = f"# {args.file_path} (lines {args.start_line}-{args.end_line} @ {args.commit_sha})\n"
        return header + "\n".join(snippet_lines)
        
    except subprocess.TimeoutExpired:
        return "Error: Git command timed out"
    except Exception as e:
        return f"Error creating snippet: {str(e)}"


# Attach tool metadata
get_file_at_commit.__tool__ = {
    "name": "git_get_file_at_commit",
    "description": "Retrieve the content of a file at a specific git commit or ref.",
    "parameters": GetFileAtCommitArgs.model_json_schema()
}

git_log_summary.__tool__ = {
    "name": "git_log_summary",
    "description": "Get a summary of recent git commits, optionally for a specific file.",
    "parameters": GitLogSummaryArgs.model_json_schema()
}

create_snippet.__tool__ = {
    "name": "git_create_snippet",
    "description": "Create a code snippet with line numbers from a file at a specific commit.",
    "parameters": CreateSnippetArgs.model_json_schema()
}
