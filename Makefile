start:
	uv run scripts/main.py

flask:
	uv run flask --app scripts/main run --port 8000

flask-debug:
	uv run flask --app scripts/main --debug run --port 8000

lint:
	uv run flake8 .\scripts\main.py