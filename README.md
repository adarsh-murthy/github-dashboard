# github-dashboard

## Overview

Search for the repositories for any organization. You have the option to sort
them by number of forks, number of contributors or number of stars.

## Technologies

- Python 3 for language.
- Django framework to build out the whole application.
- python requests library to make http requests.

## Set up

Clone this repository.

`git clone git@github.com:adarsh-murthy/github-dashboard.git`

If you use virtual environment (highly recommend), then create a new
environment for this project.

Install all the dependencies

`pip install -r requirements.txt`

Set a new environment variable to use your github api token

`export GITHUB_API_TOKEN=<token>`

Run the server locally
```
cd github_dashboard
python manage.py runserver
```

Visit http://localhost:8000/index

You should be able to search for your organization.


## Implementation detail

### Backend

We cache the organziation repositories so that we don't fetch from github every
time. The contributors count requires additional request, which are performed
only if the filter is selected (also cached).

In this project, local default cache is used but you can switch it out for any
caching backend.

### Frontend

Single template is rendered with different context. The UI is kept simple.
You have a single form to Input the organization and select a filter.
If successful, you will see a list of repositories for the specified
organization hyperlinked to the repository. If not, you see the respective
error.

### Assumptions

- Cache is not really cleared at any point so assumes that repositories don't
  change.
- If request to get the contributors fails for any reason, that number is shown
  as zero.
