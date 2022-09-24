.PHONY: docs
.PHONY: run-local
.PHONY: run-prod

docs:
	pip3 install --quiet -r requirements-docs.txt
	rm -rf docs/_build
	make -C docs html
	open docs/_build/html/index.html

run-local:
	docker-compose stop
	docker-compose build
	docker-compose -f docker-compose.yml -f docker-compose.local.yml up	

run-prod:
	docker-compose stop
	docker-compose build
	docker-compose -f docker-compose.yml -f docker-compose.deploy.yml up -d
