CLI_DOCS_DIR := src/command-line-reference
PUBLIC_DIR := public
BUCKET := s3://apppack-docs-20210105212657740100000002

# Floor for the pre-deploy sanity check. The site builds a few hundred pages;
# anything near this number means the build produced almost nothing and the
# sync below would delete most of the live site.
MIN_HTML_PAGES := 50

.PHONY: build
build: $(CLI_DOCS_DIR)
	SITE_URL=https://docs.apppack.io/ uv run --frozen zensical build --strict

# The CLI reference pages are gitignored, so a fresh clone has none. Generate
# them when the directory is missing, but leave an existing one alone -- CI runs
# `make cli-docs` explicitly and this avoids a second docgen there. Run
# `make cli-docs` to force a refresh against a newer CLI.
$(CLI_DOCS_DIR):
	$(MAKE) cli-docs

# `deploy` prunes the bucket, so refuse to run against a build that clearly did
# not finish -- otherwise a truncated artifact takes the live site down with it.
.PHONY: check-build
check-build:
	@test -f $(PUBLIC_DIR)/index.html || { \
	  echo "check-build: $(PUBLIC_DIR)/index.html is missing -- refusing to deploy"; \
	  exit 1; \
	}
	@pages=$$(find $(PUBLIC_DIR) -name '*.html' | wc -l | tr -d ' '); \
	if [ "$$pages" -lt $(MIN_HTML_PAGES) ]; then \
	  echo "check-build: only $$pages HTML pages in $(PUBLIC_DIR)/, expected at least $(MIN_HTML_PAGES) -- refusing to deploy"; \
	  exit 1; \
	fi; \
	echo "check-build: $$pages HTML pages, ok"

# Two passes: assets get a long cache lifetime, pages get none. The second pass
# skips whatever the first already uploaded.
#
# --delete belongs on the second pass, not the first: the first is filtered to
# non-HTML and would leave orphaned pages behind, while the second is unfiltered
# and sees every key in the bucket. Only keys absent from the build are removed,
# so no live page goes missing.
.PHONY: deploy
deploy: check-build
	aws s3 sync --cache-control "max-age=2592000, public" --exclude "*.html" --acl public-read $(PUBLIC_DIR)/ $(BUCKET)/
	aws s3 sync --cache-control "no-cache" --delete --acl public-read $(PUBLIC_DIR)/ $(BUCKET)/
	aws cloudfront create-invalidation --distribution-id EW46PJHD47UFG --paths '/*'

.PHONY: clean
clean:
	rm -rf ./public/*

.PHONY: cli-docs
cli-docs:
	apppack docgen --directory $(CLI_DOCS_DIR)
	uv run --frozen python scripts/generate_cli_nav.py

# Regenerates src/changelog and the changelog-nav block in mkdocs.yml.
# Needs GitHub credentials for the private repositories (gh auth or GITHUB_TOKEN).
.PHONY: changelog
changelog:
	uv run --frozen python scripts/aggregate_changelogs.py

.PHONY: check-nav
check-nav:
	uv run --frozen python scripts/check_nav_complete.py

.PHONY: run
run: $(CLI_DOCS_DIR)
	uv run --frozen zensical serve
