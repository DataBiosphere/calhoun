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

## Developing
Install dependencies

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements-min.txt
export FLASK_DEBUG=1
```

### R dependencies

Install [Pandoc](https://pandoc.org/installing.html)
```sh
brew install pandoc
```

```sh
R
> install.packages(c("rmarkdown", "stringi", "tidyverse", "Seurat", "ggforce"))
```


Write a config file
```sh
cp config.dev.py config.py
```

Ensure hosts file has the following record:
```
127.0.0.1       local.dsde-dev.broadinstitute.org
```

Update main.py to use Broad's wildcard SSL certificates.
These certificates are the same ones used for any of our web applications.
To get these certificates, run the `configure.rb` script by following the instructions under the title [Running Leo Locally](https://broadworkbench.atlassian.net/wiki/spaces/IA/pages/104399223/Callisto+Developer+Handbook#CallistoDeveloperHandbook-RunningLeoLocally)

Once complete, copy `leonardo/config/server.*` to `/etc/ssl/certs`.

Configure flask to look for the SSL Certificates

```py
# main.py
if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', ssl_context=('/etc/ssl/certs/server.crt', '/etc/ssl/certs/server.key'))
```

Edit config.py to use development authentication.
``` py
SAM_ROOT = 'https://sam.dsde-dev.broadinstitute.org'
```

Run a local server
```sh
python3 main.py
```

Or, run a local containerized server which is useful for testing R functionality
```sh
docker image build . -t calhoun-test:0
docker kill t1
docker run -e FLASK_DEBUG=1 --rm -itd --name t1 -p 8080:8080 calhoun-test:0
```

Load pages from localhost:
* http://localhost:8080/status
* http://localhost:8080/api/docs/

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
