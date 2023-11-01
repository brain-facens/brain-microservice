import requests
import subprocess
from datetime import datetime, timedelta
import os 
import shutil 

def get_organization_members(org_name: str, access_token: str):
    # Define the API URL for listing organization members
    api_url = f'https://api.github.com/orgs/{org_name}/members'

    # Set up the headers with the access token
    headers = {
        'Authorization': f'token {access_token}'
    }

    # Initialize a list to store the user names
    user_names = []

    # GitHub API pagination
    page = 1
    per_page = 100  # Adjust this number as needed

    while True:
        params = {'page': page, 'per_page': per_page}
        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code == 200:
            members = response.json()
            if len(members) == 0:
                break
            for member in members:
                user_names.append(member['login'])
            page += 1
        else:
            print(f"Failed. Status code: {response.status_code}")
            break

    return user_names

def clone_repository(repo_url, target_dir):
    try:
        subprocess.check_output(['git', 'clone', repo_url, target_dir])
        return True
    except subprocess.CalledProcessError as e:
        return False
    
def cleanup_cache(cache_dir):
    now = datetime.now()
    for item in os.listdir(cache_dir):
        item_path = os.path.join(cache_dir, item)
        if os.path.isdir(item_path):
            directory_creation_time = datetime.fromtimestamp(os.path.getctime(item_path))
            age = now - directory_creation_time
            expiration_time = timedelta(seconds=1)
            if age > expiration_time:
                shutil.rmtree(item_path)
                print(f"Deleted: {item_path}")

def list_repository(token_git: str):
    session = requests.Session()
    session.headers.update({'Authorization': f'token {token_git}'})
    org_repo_url = 'https://api.github.com/orgs/brain-facens/repos'
    response = session.get(org_repo_url)

    if response.status_code == 200:
        data = response.json()
        # Extract the name of each repository and store it in a list
        repositories_info = [repo["name"] for repo in data]
        return repositories_info
    else:
        return []