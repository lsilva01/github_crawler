import time
from dotenv import load_dotenv
import os
from elastic_enterprise_search import AppSearch

from utils import insert_document

from github import Github

load_dotenv()

app_search = AppSearch(
    os.environ['APP_SEARCH_BASE_URL_FN'],
    os.environ['APP_SEARCH_API_KEY'],
)

g = Github( os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'])


def insert_commit(repo_name, commit):
    
    git_commit = commit.commit
    
    document = {
        "sha": commit.sha,
        "url": commit.html_url,
        "domains": ["https://github.com"],
        "message": git_commit.message,
        "id": f'github-{repo_name}-commit-{commit.sha}'
    }
    
    # print(document["id"])
    # print("\n----\n")
    # return True
    return insert_document(document)

def save_commits(repo):
    commits = repo.get_commits()
    for commit in commits[:10]:
        inserted = insert_commit(repo.name, commit)
        
        if not inserted:
            # handle ?
            return False
    
repo = g.get_repo("bitcoin/bitcoin")
  
tic = time.time()
save_commits(repo)
toc = time.time()

print('Done in {:.4f} seconds'.format(toc-tic))