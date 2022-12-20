# Get notified for a change to a DMOJ problem

import requests
import json
import os


def send_message(content):
    """Send a message through a Discord webhook"""
    contents = {
        'content': content,
        'username': "Dmöj",
        'avatar_url': "https://static.dmoj.ca/texoid/5b0b81327dfdd019a2540ac001f3161cbcf74b0b/png"
    }
    r = requests.post(
        os.getenv("DMOJ_WEBHOOK_URL"),
        data=contents)
    assert r.status_code in [200, 204]


def format_problem_pp(problem):
    return str(int(problem['points'])) + 'p' * problem['partial']

def format_problem_url(pid):
    return f"https://dmoj.ca/problem/{pid}"

def format_problem(pid, problem):
    name = problem['name']
    url = format_problem_url(pid)
    pp = format_problem_pp(problem)
    group = problem['group']
    return f"{name} ({pp}, {group}) - {url}"


PROBLEM_CACHE = ".dmoj_problem_list.json"

# new problem list
r = requests.get("https://dmoj.ca/api/problem/list")
assert r.status_code == 200
content = r.text
new = json.loads(content)

# old problem list
try:
    with open(PROBLEM_CACHE, 'r') as fp:
        old = json.load(fp)
except:
    open(PROBLEM_CACHE, "w").write(content)
    send_message("Problem list cache initialized.")
    __import__('sys').exit()

# check added problems
for problem in new:
    if problem not in old:
        s = format_problem(problem, new[problem])
        send_message("New problem:\n" + s)

# check deleted problems
for problem in old:
    if problem not in new:
        s = format_problem(problem, old[problem])
        send_message("Disappeared problem:\n" + s)

# check PP changes
for problem in new:
    if problem not in old:
        continue
    old_pp = format_problem_pp(old[problem])
    new_pp = format_problem_pp(new[problem])
    if old_pp != new_pp:
        url = format_problem_url(problem)
        name = new[problem]['name']
        group = new[problem]['group']
        s = f"{name} (~~{old_pp}~~ {new_pp}, {group}) - {url}"
        send_message("Problem point change:\n" + s)

# update problem list
open(PROBLEM_CACHE, "w").write(content)
