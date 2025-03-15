start:
	uv run scripts/main.py

flask:
	uv run flask --app scripts/main run --port 8000

gunicron:
	uv run gunicorn --workers=4 --bind=127.0.0.1:8000 scripts/main:app

flask-debug:
	uv run flask --app scripts/main --debug run --port 8000

lint:
	uv run flake8 .\scripts\main.py