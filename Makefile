project=zoomcamp-capstone
project_dir=/app

.PHONY: build
build:
	docker build . -t $(project)

.PHONY: shell
shell: build
	 docker run -it --rm -v $(PWD):$(project_dir) $(project) /bin/bash

.PHONY: pretty
pretty: build
	docker run --rm -v $(PWD):$(project_dir) $(project) bash -c "black $(project_dir) && isort --atomic $(project_dir)"

#.PHONY: pipenv-update
#pipenv-update: build
#	docker run --rm -v $(PWD):$(project_dir) $(project) pipenv update

.PHONY: run-service
run-service: build
	docker run --rm -p 5000:5000 -e PORT=5000 $(project)

#  heroku container:push web --app zoomcamp-capstone
#  heroku container:release web --app zoomcamp-capstone
#  heroku logs --tail --app zoomcamp-capstone

# TODO Make client configurable in terms of URL base
.PHONY: run-client
run-client: build
	docker run --rm $(project) python predict_client.py
