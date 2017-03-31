# Makefile for Aprigi
# Description: The app for my April girl
# Copyright (C) 2016-present Anh Tranngoc
# This file is distributed under the same license as the aprigi package.
# Anh Tranngoc <naa@sfc.wide.ad.jp>, 2016.

APP_LIST ?= savings about expenses
LANG_LIST ?= vi

all: docker

install:
	pip install -r requirements/development.txt
	npm install

collectstatics: frontend-production
	./manage.py collectstatic --noinput

frontend:
	node_modules/gulp/bin/gulp.js

frontend-production:
	rm -rf static
	node_modules/gulp/bin/gulp.js --production

docker: frontend
	sudo docker-compose up

check-style:
	$(foreach app,$(APP_LIST),isort -c -rc $(app) --skip migrations;)
	$(foreach app,$(APP_LIST),flake8 --exclude=migrations $(app);)

fix-style:
	$(foreach app,$(APP_LIST),isort -rc $(app) --skip migrations;)
	$(foreach app,$(APP_LIST),autopep8 --in-place $(app)/*.py $(app)/templatetags/*.py;)

collecttranslation:
	$(foreach lang,$(LANG_LIST),./manage.py makemessages -l $(lang);)

translate:
	$(foreach lang,$(LANG_LIST),./manage.py compilemessages -l $(lang);)

migrations-check:
	./manage.py makemigrations --check --dry-run
test: migrations-check
	@coverage run --source=. ./manage.py test -v2 $(APP_LIST)

ci: test
	@coverage report
