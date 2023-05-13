.DEFAULT_GOAL := help

# This help function will automatically generate help/usage text for any make target that is commented with "##".
# Targets with a singe "#" description do not show up in the help text
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'


generate-inputs: ## Generate a dict of inputs from actions.yml into repo_manager/utils/__init__.py
	./.github/scripts/replace_inputs.sh

install-action-lint-mac: ## Install actionlint (used in pre-commit) on a mac using homebrew
	brew install actionlint

install-action-lint: ## Install actionlint (used in pre-commit) using go install
	go install github.com/rhysd/actionlint/cmd/actionlint@latest

actionlint: ## run actionlint with our ignores
	actionlint

test: ## Run our unit tests
	pytest
