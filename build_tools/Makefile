APP_LIST ?= savings about expenses
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

check-style:
	$(foreach app,$(APP_LIST),isort -c -rc ../$(app) --skip migrations;)
	$(foreach app,$(APP_LIST),flake8 --exclude=migrations ../$(app);)

fix-style:
	$(foreach app,$(APP_LIST),isort -rc ../$(app) --skip migrations;)
	$(foreach app,$(APP_LIST),autopep8 --in-place ../$(app)/*.py ../$(app)/templatetags/*.py;)

collecttranslation:
	cd .. && $(foreach lang,$(LANG_LIST),./manage.py makemessages -l $(lang);)

translate:
	cd .. && $(foreach lang,$(LANG_LIST),./manage.py compilemessages -l $(lang);)

test:
	cd .. && ./manage.py test $(APP_LIST)
