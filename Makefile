prep:
	sh ./prep.sh

build-cl:
	docker compose down --volumes --rmi="all" && docker compose build

build:
	make down && docker compose build

down:
	docker compose down --volumes

start:
	docker compose up

stop:
	docker compose stop

run:
	make down && docker compose up
