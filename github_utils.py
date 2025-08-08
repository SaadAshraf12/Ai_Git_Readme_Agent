import os
import tempfile
from git import Repo
from github import Github

def create_new_repo(github_token, repo_name, private=True):
    g = Github(github_token)
    user = g.get_user()
    repo = user.create_repo(name=repo_name, private=private)
    return repo.clone_url.replace("https://", f"https://{github_token}@")

def clone_repo(repo_url, github_token):
    tmp_dir = tempfile.mkdtemp()
    repo = Repo.clone_from(repo_url, tmp_dir, env={"GIT_TERMINAL_PROMPT": "0"})
    return tmp_dir

def push_files_to_repo(repo_path, files, readme_text, commit_message="Add README and code"):
    # Save README
    readme_path = os.path.join(repo_path, "README.md")
    with open(readme_path, "w", encoding='utf-8') as f:
        f.write(readme_text)

    # Save code files
    for file in files:
        file_path = os.path.join(repo_path, file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())

    # Git push
    repo = Repo(repo_path)
    repo.git.add(all=True)
    repo.index.commit(commit_message)
    origin = repo.remote(name='origin')
    origin.push()
