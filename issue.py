import multiprocessing

import time
from dotenv import load_dotenv
import os

from utils import insert_document, get_items

from github import Github

load_dotenv()

g = Github( os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'])

# def get_issues(repo, since=None):
#     direction="desc"
#     if since:
#         return repo.get_issues(state="all", direction=direction)
#     else:
#         return repo.get_issues(state="all", direction=direction)

# issues = repo.get_issues(state="all", direction="asc")
# print(issues.totalCount)

# for issue in issues[:10]:
#     print(issue.number)
    
def insert_issue(repo_name, issue):
    # print("\ni ---")
    # print(issue.html_url)
    # print(issue.number)
    # print(issue.title)
    # print(issue.created_at)
    # print(issue.body) # can be blank
    
    
    document = {
        "number": issue.number,
        "url": issue.html_url,
        "domains": ["https://github.com"],
        "title": issue.title,
        "id": f'github-{repo_name}-issue-{issue.id}',
        "created_at": issue.created_at,
        "data_type": "issue",
        "body": issue.body
    }
    
    return insert_document(document)
    
def insert_comment(repo_name, comment, issue_id):
    # print("c ---")
    # print(comment.html_url)
    # print(comment.created_at)
    # print(comment.body)
    
    document = {
        "url": comment.html_url,
        "domains": ["https://github.com"],
        "id": f'github-{repo_name}-issue-comment-{comment.id}',
        "created_at": comment.created_at,
        "data_type": "comment",
        "body": comment.body,
        "issue_id": issue_id
    }
    
    return insert_document(document)

def save_issues(repo):
    
    # issues = get_issues(repo, since=None)
    issues = get_items(repo.get_issues, since=None)
    
    # processes = []
    for issue in issues[:10]:
        # multiprocessing is not working. Probably due to multiple requests do Github' servers
        # p = multiprocessing.Process(target=handle_issue, args=(issue,))
        # processes.append(p)
        # p.start()
        inserted = insert_issue(repo.name, issue)
        
        if not inserted:
            # handle ?
            return False
        
        comments = issue.get_comments()
        for comment in comments:
            inserted = insert_comment(repo.name, comment, issue.id)
            if not inserted:
            # handle ?
                return False
        
    # for process in processes:
    #     process.join()
    return True

repo = g.get_repo("bitcoin/bitcoin")

tic = time.time()
save_issues(repo)
toc = time.time()

print('Done in {:.4f} seconds'.format(toc-tic))
