build:
	docker build -t app .

run:
	docker run -d --rm -p 8000:8000 --name app app

build-push:
	docker build -t arais.gitlab.yandexcloud.net:5050/erickarais/app:test .
	docker push arais.gitlab.yandexcloud.net:5050/erickarais/app:test