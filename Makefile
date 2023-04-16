.PHONY: install-requirements
install-requirements:
	pip install -r requirements.txt

.PHONY: run-api-locally
run-api-locally: install-requirements
	OFFLINE=true sls offline --reloadHandler --stage dev

.PHONY: format
format:
	black . && isort .

.PHONY: deploy
deploy:
	sls deploy --stage dev