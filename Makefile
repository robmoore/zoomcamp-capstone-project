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

.PHONY: run-service
run-service: build
	docker run --rm -p 5000:5000 -e PORT=5000 $(project)

.PHONY: run-client-local
run-client-local: build
	docker run --rm -v $(PWD):$(project_dir) $(project) bash -c "gunicorn --daemon predict:app && python predict_client.py"

.PHONY: run-client-remote
run-client-remote:
	docker run --rm -v $(PWD):$(project_dir) $(project) python predict_client.py --url https://$(project).herokuapp.com/predict

.PHONY: heroku-login
heroku-login:
	heroku login

.PHONY: heroku-deploy
heroku-deploy: build
	heroku container:login
	heroku container:push web --app $(project)
	heroku container:release web --app $(project)

.PHONY: heroku-tail
heroku-tail:
	 heroku logs --tail --app $(project)

data: build
	docker run -it --rm -v $(PWD):$(project_dir) $(project) ./download-data.sh

bin: build
	mkdir bin
	docker run -it --rm -v $(PWD):$(project_dir) $(project) python train.py
