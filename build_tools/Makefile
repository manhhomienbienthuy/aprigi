APP_LIST ?= savings

install:
	pip install -r ../requirements/development.txt
	npm install

collectstatics: frontend
	../manage.py collectstatic --noinput

frontend:
	gulp

watch:
	gulp watch

docker:
	sudo docker-compose up

isort:
	@$(foreach app,$(APP_LIST),isort -rc ../$(app);)

isort-check:
	@$(foreach app,$(APP_LIST),isort -c -rc ../$(app);)

flake8:
	@$(foreach app,$(APP_LIST),flake8 --exclude=migrations ../$(app);)

autopep8:
	@$(foreach app,$(APP_LIST),autopep8 --in-place ../$(app)/*.py;)
