"""Some helper functions."""
import os
import requests

from django.core.cache import cache

GITHUB_API = "https://api.github.com"
def get_github_api_key():
    """Get the github API key from the cache."""
    return cache.get('api_key', None)


github_api_key = get_github_api_key()

headers = {}
if github_api_key:
    # Headers to make calls to github
    headers = {"Authorization": "Token {}".format(github_api_key)}


def get_repositories(organization):
    """Get repositories from github for an organization."""
    # Construct the url.
    url = "{}/orgs/{}/repos".format(GITHUB_API, organization)
    response = requests.get(url, headers=headers)
    if not response.status_code == 200:
        raise ValueError(response.json().get("message"))
    content = response.json()
    return content


def update_repos_with_contributor_count(repos):
    """For a list of repositories, update each repository with its contributor
    count.
    """
    new_content = []
    for repo in repos:
        repo = update_repo_with_contributor_count(repo)
        new_content.append(repo)
    return new_content


def update_repo_with_contributor_count(repo):
    """Given a repository, update it to have the number of contributors."""
    contributors_url = repo.get("contributors_url")
    response = requests.get(contributors_url, headers=headers)
    if response.status_code == 200:
        repo["contributors_count"] = len(response.json())
    else:
        repo["contributors_count"] = 0
    return repo
