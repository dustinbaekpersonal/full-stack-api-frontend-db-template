delete-git-branch:
	git remote prune origin
	git fetch --prune

uv-setup:
	pip install uv
	uv venv

uv-dev:
	uv pip compile requirements/prod.in -o requirements/prod.txt
	uv pip compile requirements/test.in -o requirements/test.txt
	uv pip compile requirements/dev.in -o requirements/dev.txt
	uv pip sync requirements/dev.txt
