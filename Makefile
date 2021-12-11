project=zoomcamp-capstone
project_dir=/app
url=http://0.0.0.0:5000/predict

.PHONY: build
build:
	docker build . -t $(project)

.PHONY: shell
shell: build
	docker run -it --rm -v $(PWD):$(project_dir) $(project) /bin/bash

.PHONY: pretty
pretty: build
	docker run --rm -v $(PWD):$(project_dir) $(project) bash -c "black $(project_dir) && isort --atomic $(project_dir)"

.PHONY: run-service
run-service: build
	docker run --rm -p 5000:5000 -e PORT=5000 $(project)

run-client-remote: url=https://$(project).herokuapp.com/predict
run-client-local run-client-remote:
	pipenv run python predict_client.py --url $(url)

.PHONY: heroku-login
heroku-login:
	heroku login
	heroku container:login

.PHONY: heroku-deploy
heroku-deploy: build
	heroku container:push web --app zoomcamp-capstone
	heroku container:release web --app zoomcamp-capstone

.PHONY: heroku-tail
heroku-tail:
	 heroku logs --tail --app zoomcamp-capstone

data: build
	docker run -it --rm -v $(PWD):$(project_dir) $(project) ./download-data.sh

bin: build
	mkdir bin
	docker run -it --rm -v $(PWD):$(project_dir) $(project) python train.py
