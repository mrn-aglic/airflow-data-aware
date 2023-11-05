prep:
	sh ./prep.sh

build:
	docker compose down && docker compose build

down:
	docker compose down --volumes

start:
	docker compose up

stop:
	docker compose stop

run:
	make down && docker compose up
