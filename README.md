# Calhoun
Jupyter notebook preview service

### Background
This project is part of the Terra (née FireCloud) platform of service APIs. It is primarily intended to provide preview versions of notebooks for Terra-based web applications, such as the [Terra workbench](https://www.terra.bio) research environment. Originally written in Node.js and shelling out to `nbconvert`, this service is now written wholly in Python 3.7 so that it can be deployed in the Google App Engine Standard environment.

There is an argument to be made that the client application should interpret notebook JSON and handle it's own styling. It seems like it would be faster, and would eliminate the additional infrastructure. It could also be more customizable to the app context. But this app is fairly simple, and there's precedent that it works well for it's intended purpose. 

### Description
Your web-app needs to display read-only versions of Jupyter notebooks. 

Under the hood, Jupyter .ipynb files are JSON documents with a particular [format](https://nbformat.readthedocs.io). Jupyter provides a commandline tool / library [nbconvert](https://nbconvert.readthedocs.io) for interacting with these documents and converting them to various formats, in particular HTML.

This project is essentially nbconvert as a REST service. It takes notebook JSON and returns HTML that can be embedded in your application.

There are two routes:

/status is a health-check endpoint. It accepts GET requests and returns 200 'OK'.

/api/convert is the primary conversion endpoint. It accepts POST requests containing notebook JSON and returns HTML for displaying the notebook's content in the browser.
This endpoint is authorized via Terra's SAM authorization service. Calls therefore require an auth header supplying an Oauth2 bearer token (obtained via Google SSO or gcloud auth login). The token must represent a registered, enabled Terra/FireCloud  user.

### Framework.
This project uses the [Sanic](https://sanic.readthedocs.io) Python web framework. Calhoun's original Node.js code made use Node's async/await syntax. A couple of factors argue in favor of asynchronous request handling being an important feature:
1. The conversion itself may take some time
2. The intended authorization method involves a call to another webservice, which may take variable time
3. The intended consumer is a web-app with hundreds-to-thousands of monthly engaged users, and notebook previewing is a relatively common user task.

Python 3.5 introduced concurrency through coroutines supported by async/await syntax. Several web frameworks make use of asyncio. Finalists included aiohttp and Sanic. Some online reading provided anecdotal evidence indicated that performance was good for both frameworks. We appreciated Sanic's simple syntax, and thought it would be convenient for a small project like this, and readable for programmers coming from Node.

### Developing
Install dependencies

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements-min.txt
export FLASK_DEBUG=1
```


Write a config file
```sh
cp config.dev.py config.py
```

Run a local server
```sh
FLASK_DEBUG=1 python3 main.py
```
Or, to more closely emulate running in App Engine
```sh
FLASK_DEBUG=1 gunicorn -b :8000 main:app
```

Run unit tests locally
```sh
python test_convert.py 
```

Run automation tests locally
```sh
./scripts/automation-test.sh
```


Update/freeze dependencies
```sh
scripts/freeze-deps.sh
```
This creates a clean virtualenv, installs dependencies from `dependencies-min.txt`, and freezes the resulting environment in `requirements.txt` (which Google App Engine uses during deployment).

Deploy
```sh
TERRA_ENV=dev scripts/deploy.sh
```
