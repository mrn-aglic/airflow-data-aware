prep:
	sh ./prep.sh

build-cl:
	make down-rmi && docker compose build

build:
	make down && docker compose build

down:
	docker compose down --volumes

down-rmi:
	docker compose down --volumes --rmi="all"

start:
	docker compose up

stop:
	docker compose stop

run:
	make down && docker compose up
