import requests

from django.core.cache import cache
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View

from .utils import get_repositories, update_repos_with_contributor_count


def get_index(request):
    return render(request, "base.html")


def get_repositories_for_org(request):
    """GETs list of repositories for a github organization."""
    # Grab the organization from the request query parameters.
    organization = request.GET.get("organization", None)

    # Grab the sorting method.
    sort_by = request.GET.get("sort_by", "forks_count")

    if not organization:
        return render(
            request,
            "index.html",
            {"error": "No organization provided", "organization": ""},
        )

    # Make sure organization is of type string.
    if not isinstance(organization, str):
        return render(
            request,
            "index.html",
            {"error": "Organization has to be of type string"},
        )

    # Making the organization to lower strings.
    organization = organization.lower()

    # Checking if we already have the repositories in cache.
    content = cache.get(organization)

    # If not, get them from github.
    if not content:
        try:
            content = get_repositories(organization)
        except ValueError as exc:
            return render(request, "index.html", {"error": str(exc)})
        # Set the repositories in cache.
        cache.set(organization, content)
    # sort the repositories specified by user.
    if sort_by == "forks_count":
        content = sorted(
            content, key=lambda repo: repo["forks_count"], reverse=True
        )

    if sort_by == "stargazers_count":
        content = sorted(
            content, key=lambda repo: repo["stargazers_count"], reverse=True
        )

    # Contributor count is not on the repositories. We need to do additional
    # processing here.
    if sort_by == "contributors_count":
        if content[0].get("contributors_count", None) is None:
            content = update_repos_with_contributor_count(content)
            cache.set(organization, content)
        content = sorted(
            content, key=lambda repo: repo["contributors_count"], reverse=True
        )
    return render(
        request, "index.html", {"data": content, "organization": organization}
    )


def github_api_key(request):
    """Stores github API token in cache."""
    if request.method == "post":
        api_token = request.POST.get("api_key")
        cache.set("api_key", api_token)
    return render(request, "add_api_key.html")
