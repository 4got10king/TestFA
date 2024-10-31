.PHONY: run-server fill-data clean install migrate run-server-nh stop-server flush-redis list-redis app app-logs debug backup_data product

DC = docker-compose
LOGS = docker logs
APP_CONTAINER = backend


flush-redis:
	docker exec redis redis-cli FLUSHALL

list-redis:
	sudo docker exec redis redis-cli KEYS '*' | xargs -I {} sudo docker exec redis redis-cli GET {}

clean:
	@echo "Removing lock..."
	@rm poetry.lock

install:
	@echo "Installing dep..."
	@poetry install
	@sudo apt-get update && sudo apt-get install ffmpeg libsm6 libxext6  -y
	@poetry lock


migrate:
	@echo "Applying database migrations..."
	@poetry run alembic upgrade head
	@echo "Migrations applied successfully."


run-server:
	@echo "Starting server..."
	@poetry run python3 run.py

run-server-nh:
	@echo "Starting server..."
	@nohup poetry run python3 run.py & echo $$! > start_pid

stop-server:
	@sudo netstat -tulnp | grep ':8081' | awk '{print $7}' | cut -d'/' -f1 | xargs -r sudo kill -2


app:
	@echo "Building container"
	sed -i '' 's/DB__HOST=localhost/DB__HOST=postgres/' .env
	sed -i '' 's/REDIS_ENDPOINT=redis:\/\/localhost:6379/REDIS_ENDPOINT=redis:\/\/redis:6379/' .env
	${DC} up --build -d

app-logs:
	${LOGS} ${APP_CONTAINER} -f

debug:
	sed -i '' 's/DB__HOST=postgres/DB__HOST=localhost/' .env
	sed -i '' 's/REDIS_ENDPOINT=redis:\/\/redis:6379/REDIS_ENDPOINT=redis:\/\/localhost:6379/' .env
	docker-compose -f debug.yml up -d

run_migr:
	@echo "Applying database migrations..."
	@poetry run alembic upgrade head
	@echo "Migrations applied successfully."
	@echo "Starting server..."
	@poetry run python3 run.py