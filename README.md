# github-dashboard

## Overview

Search for the repositories for any organization. You have the option to sort
them by number of forks, number of contributors or number of stars.

## Technologies

Use Django framework to build out the whole application.
Use python requests library to make http requests.

## Set up

Clone this repository.
`git clone <git_clone_link>`

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

Single template is rendered with different context. The UI is kept simple.
