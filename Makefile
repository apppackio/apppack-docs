
.venv/bin/python3.9:
	python3.9 -m venv --prompt $(shell basename $(shell pwd)) .venv
	.venv/bin/pip install -U pip setuptools wheel

.PHONY: install
install: .venv/bin/python3.9
	.venv/bin/pip install -r requirements.txt

.PHONY: build
build:
	.venv/bin/mkdocs build

.PHONY: deploy
deploy: build
	aws s3 sync --cache-control "max-age=2592000, public" --exclude "*.html" --acl public-read ./public/ s3://apppack-docs-20210105212657740100000002/
	aws s3 sync --cache-control "no-cache" --acl public-read ./public/ s3://apppack-docs-20210105212657740100000002/
	aws cloudfront create-invalidation --distribution-id EW46PJHD47UFG --paths '/*'

.PHONY: clean
clean:
	rm -rf ./public/*
