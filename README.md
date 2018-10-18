# Calhoun
Notebook preview service

### Requirements
- Docker
- Node 8

### Developing
Install deps
```sh
npm install
```

Write config file
```sh
cp config.dev.json config.json
```

Build docker image (you only have to do this once, unless you change the Dockerfile)
```sh
docker build -t calhoun .
```

Build docs
```sh
npm run generate-docs
```

Start a dev server on port 8080 with auto-reload
```sh
docker run --rm -it -p 8080:8080 -v $PWD:/app calhoun npm run start-dev
```

Lint
```sh
npm run lint
```

Deploy
```sh
TERRA_ENV=dev scripts/deploy.sh
```
