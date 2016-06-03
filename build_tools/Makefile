APP_LIST ?= savings
LANG_LIST ?= vi

all: docker

install:
	pip install -r ../requirements/development.txt
	npm install

collectstatics: frontend-production
	../manage.py collectstatic --noinput

frontend:
	gulp

frontend-production:
	gulp --production

docker: frontend
	sudo docker-compose up

check-style: isort-check flake8

fix-style: isort autopep8

isort:
	$(foreach app,$(APP_LIST),isort -rc ../$(app);)

isort-check:
	$(foreach app,$(APP_LIST),isort -c -rc ../$(app);)

flake8:
	$(foreach app,$(APP_LIST),flake8 --exclude=migrations ../$(app);)

autopep8:
	$(foreach app,$(APP_LIST),autopep8 --in-place ../$(app)/*.py;)

collecttranslation:
	cd .. && $(foreach lang,$(LANG_LIST),./manage.py makemessages -l $(lang);)

translate:
	cd .. && $(foreach lang,$(LANG_LIST),./manage.py compilemessages -l $(lang);)
