from git import Repo
    
def clone_repo(name: str, url: str, local_dir: str = None):
    if local_dir is None:
        local_dir = f"projects/{name}"
    
    return Repo.clone_from(url, local_dir)