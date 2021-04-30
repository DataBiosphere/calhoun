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

A swagger-ui page is available at /api/docs on any running instance. For existing instances, those are:

* dev: https://calhoun.dsde-dev.broadinstitute.org/api/docs
* alpha: https://calhoun.dsde-alpha.broadinstitute.org/api/docs
* perf: https://calhoun.dsde-perf.broadinstitute.org/api/docs
* staging: https://calhoun.dsde-staging.broadinstitute.org/api/docs
* prod: https://calhoun.dsde-prod.broadinstitute.org/api/docs

### Framework
This project uses the [Flask](https://flask.palletsprojects.com/en/1.1.x/) Python web framework.

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

Or, run a local containerized server which is useful for testing R functionality
```sh
docker image build . -t calhoun-test:0
docker kill t1
docker run -e FLASK_DEBUG=1 --rm -itd --name t1 -p 8000:8000 calhoun-test:0
```

Load pages from localhost:
* http://localhost:8000/status
* http://localhost:8000/api/docs/

Run unit tests locally
```sh
./scripts/unit-test.sh
```

Run automation tests locally
```sh
gcloud auth login <any-terra-dev-user>
RUN_AUTHENTICATED_TEST=1 ./scripts/automation-test.sh
```

Update/freeze dependencies
```sh
scripts/freeze-deps.sh
```
This creates a clean virtualenv, installs dependencies from `dependencies-min.txt`, and freezes the resulting environment in `requirements.txt` (which Google App Engine uses during deployment).

### Deployment

TODO add section about k8s deployment
