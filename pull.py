import time
from dotenv import load_dotenv
import os
from elastic_enterprise_search import AppSearch

from utils import insert_document, get_items

from github import Github

load_dotenv()

app_search = AppSearch(
    os.environ['APP_SEARCH_BASE_URL_FN'],
    os.environ['APP_SEARCH_API_KEY'],
)

g = Github( os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'])

def insert_pull(repo_name, pull):
    document = {
        "number": pull.number,
        "url": pull.html_url,
        "domains": ["https://github.com"],
        "title": pull.title,
        "id": f'github-{repo_name}-pull-{pull.id}',
        "created_at": pull.created_at,
        "data_type": "pull-request",
        "body": pull.body
    }
    
    return insert_document(document)

def insert_comment(repo_name, comment, issue_id):
    document = {
        "url": comment.html_url,
        "domains": ["https://github.com"],
        "id": f'github-{repo_name}-pull-comment-{comment.id}',
        "created_at": comment.created_at,
        "data_type": "comment",
        "body": comment.body,
        "issue_id": issue_id
    }
    
    return insert_document(document)

def save_pulls(repo):
    pulls = get_items(repo.get_pulls, since=None)
    print(pulls)
    
    for pull in pulls[:10]:
        inserted = insert_pull(repo.name, pull)
        
        if not inserted:
            # handle ?
            return False
        
        comments = pull.get_comments()
        for comment in comments:
            inserted = insert_comment(repo.name, comment, pull.id)
            if not inserted:
            # handle ?
                return False
    
repo = g.get_repo("bitcoin/bitcoin")

tic = time.time()
save_pulls(repo)
toc = time.time()

print('Done in {:.4f} seconds'.format(toc-tic))