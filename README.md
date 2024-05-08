# Calhoun
Jupyter notebook preview service

### Background
This project is part of the Terra platform of service APIs. It is primarily intended to provide preview versions of notebooks and R markdown files for Terra-based web applications, such as the [Terra workbench](https://www.terra.bio) research environment.

### Description
Your web-app needs to display read-only versions of Jupyter notebooks and R markdown files.

Under the hood, Jupyter .ipynb files are JSON documents with a particular [format](https://nbformat.readthedocs.io). Jupyter provides a commandline tool / library [nbconvert](https://nbconvert.readthedocs.io) for interacting with these documents and converting them to various formats, in particular HTML.

Similarly, R Markdown .Rmd files are documents with a particular [format](https://bookdown.org/yihui/rmarkdown/markdown-document.html), and the [rmarkdown](https://cran.r-project.org/web/packages/rmarkdown/index.html) package provides mechanisms for converting R Markdown documents to HTML.

This project is essentially nbconvert and rmarkdown as a REST service. It takes an input notebook or R Markdown document and returns HTML that can be embedded in your application.

### OpenAPI

A swagger-ui page is available at /swagger-ui/ on any running instance. For existing instances, those are:

* dev: https://calhoun.dsde-dev.broadinstitute.org/swagger-ui/
* alpha: https://calhoun.dsde-alpha.broadinstitute.org/swagger-ui/
* perf: https://calhoun.dsde-perf.broadinstitute.org/swagger-ui/
* staging: https://calhoun.dsde-staging.broadinstitute.org/swagger-ui/
* prod: https://calhoun.dsde-prod.broadinstitute.org/swagger-ui/

### Framework
This project uses the [Flask](https://flask.palletsprojects.com/en/1.1.x/) Python web framework.


## Managing dependencies

We use [Poetry](https://python-poetry.org/docs/) to manage our dependencies. From their website: 

> Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. Poetry offers a lockfile to ensure repeatable installs, and can build your project for distribution.


Install [Poetry](https://python-poetry.org/docs/)

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

If you need to change any dependency versions:
- update the pyproject.toml file
- run the following to update the lock file
  
```sh
poetry lock
```

Install dependencies
```sh
poetry install
```

Update dependencies
```sh
poetry update
```

Export to requirements.txt. Google App Engine uses this for deployment.
```
poetry export -f requirements.txt --output requirements.txt --without-hashes
```


## Run locally

Either run a local containerized server:

```sh
docker image build . -t calhoun-test:0
docker kill t1
docker run -e FLASK_DEBUG=1 --rm -itd --name t1 -p 8080:8080 calhoun-test:0
```

### or 

run a local app with [Flask](https://flask.palletsprojects.com/en/1.1.x/):

```sh
python3 -m venv env
source env/bin/activate
pip install Flask
export FLASK_DEBUG=1
```

### Install dependencies

Install [Pandoc](https://pandoc.org/installing.html) and R
```sh
brew install pandoc
brew install R
```

Install R packages
```sh
R
> install.packages(c("rmarkdown", "stringi", "tidyverse", "Seurat", "ggforce"))
```

Install [Poetry](https://python-poetry.org/docs/) and project dependencies
```sh
curl -sSL https://install.python-poetry.org
poetry install
```

Write a dev config file
```sh
cp config.py config.dev.py 
```

Ensure etc/hosts file has the following record:
```
127.0.0.1       local.dsde-dev.broadinstitute.org
```

Once complete, copy `vault read secret/dsde/firecloud/dev/common/server.crt` to `/etc/ssl/certs` and 
`vault read secret/dsde/firecloud/dev/common/server.key` to `/etc/ssl/private`.

Run a local server
```sh
DEVELOPMENT='true' SAM_ROOT='https://sam.dsde-dev.broadinstitute.org' python3 main.py
```




Access the application locally:
* https://local.dsde-dev.broadinstitute.org:8080/status
* https://local.dsde-dev.broadinstitute.org:8080/api/docs/

Run unit tests locally
```sh
./scripts/unit-test.sh
```

Run automation tests locally
```sh
gcloud auth login <any-terra-dev-user>
RUN_AUTHENTICATED_TEST=1 ./scripts/automation-test.sh
```



### Deployment

TODO add section about k8s deployment
