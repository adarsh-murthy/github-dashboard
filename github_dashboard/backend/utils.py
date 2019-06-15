"""Some helper functions."""
import os
import requests

GITHUB_API = "https://api.github.com"
GITHUB_API_KEY = os.environ.get("GITHUB_API_KEY")

# Headers to make calls to github
HEADERS = {"Authorization": "Token {}".format(GITHUB_API_KEY)}


def get_repositories(organization):
    """Get repositories from github for an organization."""
    # Construct the url.
    url = "{}/orgs/{}/repos".format(GITHUB_API, organization)
    response = requests.get(url, headers=HEADERS)
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
    response = requests.get(contributors_url, headers=HEADERS)
    repo["contributors_count"] = len(response.json())
    return repo
