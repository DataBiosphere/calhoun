#!/usr/bin/env bash

# Build and start calhoun
docker image build . -t calhoun-test:0
docker kill t1 || true
docker run \
  -e FLASK_DEBUG=1 \
  -e SAM_ROOT=https://sam.dsde-dev.broadinstitute.org \
  -e SWAGGER_CLIENT_ID=enter-client-id-here \
  -e SWAGGER_REALM=broad-dsde-dev \
  --rm -itd --name t1 -p 8080:8080 calhoun-test:0

# Wait for calhoun to start
sleep 30

# /status test case
status_code=$(curl -sI --write-out %{http_code} -o /dev/null http://127.0.0.1:8080/status)

exit_code=$?
if [ $? -ne 0 ] ; then
  echo -e "  ** Failure! Curl command failed with exit code $exit_code."
  docker kill t1 || true
  exit 1
fi

echo "Response from /status: $status_code"

if [ "$status_code" != "200" ] ; then
  echo -e "  ** Failure! Expected 200 but was $status_code."
  docker kill t1 || true
  exit 1
fi

if [ "$RUN_AUTHENTICATED_TEST" = "1" ] ;
then
  for f in `ls notebooks/*.{ipynb,Rmd}`
  do
    if [[ "$f" == *.ipynb ]]
    then
      api="/api/convert"
      content_type="application/json"
    else
      api="/api/convert/rmd"
      content_type="text/plain"
    fi

    rm $f.html
    echo -e "\nConverting $f..."

    status_code=$(curl -s --write-out %{http_code} -o $f.html \
      -X POST -H "Content-Type: $content_type" -H "Accept: text/html" \
      -H "Authorization: Bearer $(gcloud auth print-access-token)" \
      --data-binary @$f \
      http://127.0.0.1:8080$api)

      exit_code=$?
      if [ $? -ne 0 ] ; then
        echo -e "  ** Failure! Curl command failed with exit code $exit_code."
        docker kill t1 || true
        exit 1
      fi

     echo "Status code: $status_code"
     echo "Output saved to: $f.html"

    if [ "$status_code" != "200" ] ; then
      echo -e "  ** Failure! Expected 200 but was $status_code."
      docker kill t1 || true
      exit 1
    fi
  done
else
  echo "Skipping authenticated tests."
fi

echo -e "\nAll tests passed!\n"
docker kill t1 || true
exit 0
