.PHONY: build
build:
	SITE_URL=https://docs.apppack.io/ pdm run mkdocs build

.PHONY: deploy
deploy:
	aws s3 sync --cache-control "max-age=2592000, public" --exclude "*.html" --acl public-read ./public/ s3://apppack-docs-20210105212657740100000002/
	aws s3 sync --cache-control "no-cache" --acl public-read ./public/ s3://apppack-docs-20210105212657740100000002/
	aws cloudfront create-invalidation --distribution-id EW46PJHD47UFG --paths '/*'

.PHONY: clean
clean:
	rm -rf ./public/*
