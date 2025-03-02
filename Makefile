start:
	uv run main.py

flask:
	uv run flask --app scripts/main run --port 8000

flask-debug:
	uv run flask --app main --debug run --port 8000