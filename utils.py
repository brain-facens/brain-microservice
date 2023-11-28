from git import Repo
import re 
    
def clone_repo(name: str, url: str, local_dir: str = None):
    if local_dir is None:
        local_dir = f"projects/{name}"
    
    return Repo.clone_from(url, local_dir)


def is_valid_email(email: str) -> bool:
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(email_pattern, email))