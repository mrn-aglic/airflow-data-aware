prep:
	sh ./prep.sh

build:
	docker compose down && docker compose build

down:
	docker compose down --volumes

run:
	make down && docker compose up
