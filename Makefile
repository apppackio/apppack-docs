CLI_DOCS_DIR := src/command-line-reference

.PHONY: build
build: $(CLI_DOCS_DIR)
	SITE_URL=https://docs.apppack.io/ uv run zensical build --strict

# The CLI reference pages are gitignored, so a fresh clone has none. Generate
# them when the directory is missing, but leave an existing one alone -- CI runs
# `make cli-docs` explicitly and this avoids a second docgen there. Run
# `make cli-docs` to force a refresh against a newer CLI.
$(CLI_DOCS_DIR):
	$(MAKE) cli-docs

.PHONY: deploy
deploy:
	aws s3 sync --cache-control "max-age=2592000, public" --exclude "*.html" --acl public-read ./public/ s3://apppack-docs-20210105212657740100000002/
	aws s3 sync --cache-control "no-cache" --acl public-read ./public/ s3://apppack-docs-20210105212657740100000002/
	aws cloudfront create-invalidation --distribution-id EW46PJHD47UFG --paths '/*'

.PHONY: clean
clean:
	rm -rf ./public/*

.PHONY: cli-docs
cli-docs:
	apppack docgen --directory $(CLI_DOCS_DIR)
	uv run python scripts/generate_cli_nav.py

.PHONY: check-nav
check-nav:
	uv run python scripts/check_nav_complete.py

.PHONY: run
run: $(CLI_DOCS_DIR)
	uv run zensical serve
