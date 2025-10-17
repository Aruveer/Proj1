# github_utils.py
import os
from github import Github
from github.GithubException import UnknownObjectException

# The GitHub Token is loaded from the environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    # We raise an error here to catch the issue early, but the main.py
    # should be robust to this if the env is not set before startup.
    pass 

def get_github_client():
    """Initializes and returns the PyGithub client."""
    if not GITHUB_TOKEN:
        raise EnvironmentError("GITHUB_TOKEN environment variable is not set.")
    return Github(GITHUB_TOKEN)

def get_user_login(g: Github):
    """Returns the authenticated user's login name."""
    return g.get_user().login

def create_repo(repo_name: str, description: str) -> object:
    """
    Creates a new public GitHub repository.
    Returns the PyGithub repository object.
    """
    g = get_github_client()
    user = g.get_user()
    try:
        repo = user.create_repo(
            repo_name,
            description=description,
            private=False,  # Must be public
            license_template='mit'
        )
        print(f"✅ Repository '{repo_name}' created successfully.")
        return repo
    except Exception as e:
        # If the repo already exists, try to return it
        print(f"Error creating repository, attempting to retrieve existing: {e}")
        try:
            return user.get_repo(repo_name)
        except Exception:
            raise Exception(f"Failed to create or retrieve repo: {e}")

def push_files_to_repo(repo: object, files: dict, commit_message: str) -> str:
    """
    Pushes a dictionary of files (filename: content) to the 'main' branch.
    Returns the SHA of the new commit.
    """
    branch = "main"
    
    # Process all files
    for file_path, content in files.items():
        try:
            # Check if file exists to decide on create/update
            contents = repo.get_contents(file_path, ref=branch)
            # Update file
            repo.update_file(
                path=file_path,
                message=f"Update {file_path}: {commit_message}",
                content=content,
                sha=contents.sha,
                branch=branch
            )
            print(f"   -> Updated file: {file_path}")
        except UnknownObjectException:
            # File does not exist, create it
            repo.create_file(
                path=file_path,
                message=f"Create {file_path}: {commit_message}",
                content=content,
                branch=branch
            )
            print(f"   -> Created file: {file_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            raise

    # Get the final commit SHA
    final_commit = repo.get_commits(sha=branch)[0]
    print(f"✅ Files pushed. Commit SHA: {final_commit.sha}")
    return final_commit.sha

def enable_github_pages(repo: object, branch: str = 'main') -> str:
    """
    Enables GitHub Pages deployment from the specified branch and returns the URL.
    """
    # Try to set the pages source
    try:
        # Assumes the user has configured Pages to deploy from 'main'
        repo.set_pages_source(source={"branch": branch, "path": "/"})
        print(f"✅ GitHub Pages source set to branch '{branch}'.")
    except Exception as e:
        # This often fails if Pages is controlled via a GitHub Action (which is common)
        print(f"Warning: Failed to set Pages source (may be controlled by Actions): {e}")

    # Construct the Pages URL (format is predictable)
    try:
        username = get_user_login(get_github_client())
    except EnvironmentError:
        # Fallback if token is missing
        username = "GITHUB_USER" 
        
    pages_url = f"https://{username.lower()}.github.io/{repo.name}/"
    print(f"💡 Predicted Pages URL: {pages_url}")
    return pages_url
