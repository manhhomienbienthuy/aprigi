![Aprigi](https://bytebucket.org/manhhomienbienthuy/aprigi/raw/c53e73941bb1532b824ee69a62a68dfe86e45d45/static_src/img/logo.svg)

# Aprigi: App for my April girl.

[![Build Status](https://travis-ci.org/manhhomienbienthuy/aprigi.svg?branch=master)](https://travis-ci.org/manhhomienbienthuy/aprigi)
[![Coverage Status](https://coveralls.io/repos/github/manhhomienbienthuy/aprigi/badge.svg)](https://coveralls.io/github/manhhomienbienthuy/aprigi)
[![Requirements Status](https://requires.io/github/manhhomienbienthuy/aprigi/requirements.svg?branch=master)](https://requires.io/github/manhhomienbienthuy/aprigi/requirements/?branch=master)
[![Deps Status](https://david-dm.org/manhhomienbienthuy/aprigi.svg)](https://david-dm.org/manhhomienbienthuy/aprigi)
[![devDeps Status](https://david-dm.org/manhhomienbienthuy/aprigi/dev-status.svg)](https://david-dm.org/manhhomienbienthuy/aprigi?type=dev)

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

> This repository is stored in
> both [bitbucket](https://bitbucket.org/manhhomienbienthuy/aprigi)
> and [Github](https://github.com/manhhomienbienthuy/aprigi)

Aprigi is the website and service helps you spend smarter and save
more.  Aprigi will help you pull all your accounts and investments
into one place so you can track your spending, create a budget and get
tips for reducing fees and saving money.

Money is very important for life today. Our mission is to empower
people to make better financial decisions, so they can be good with
money.  Aprigi helps peole keep track of expenses and budgets to reach
their saving goals.  It's simplest way to manage personal finances.
Aprigi will help you understand where your money goes, so you can plan
to spend more effectively.  Forget notebook, pen or excel sheet, you
are able to manage your personal and family finance on this website.

# Key features:

- Easy to manage and track your Saving
- Calculator in application
- Expense tracker and Money manager
- Budget planner
- It's free (and always will be)

We try to make the product perfect.  But we can not controll all
potential bugs.  We welcome you to help us improve this website.

# Set up

We use [`pip`](https://pypi.python.org/pypi/pip)
and [`yarn`](https://yarnpkg.com/en/) to manage installation of
dependencies.  Please install them before.  (Alternatively, you can
use `npm` instead of `yarn`).  Make sure you
have [`NodeJS`](https://nodejs.org/en/) on your machine.

To run locally, do ONE of the following methods

## Method 1: Configure virtualenv

### Create virtualenv

### Install dependencies

```console
pip install -r requirements/development.txt
yarn
```

Alternatively use the make task

```console
make install
```

### Set up environment variables

Update your `.bashrc` to set up environment variables.  Please see
`conf/.env.example` for more information.

### Create databases

```console
createuser -d your-db-username
createdb -O your-db-username your-dbname
```

Please use the same username and password as the ones you've used in
your `POSTGRES_USER`, `POSTGRES_PASSWORD` environment variables.

### Migrate and create superuser

```console
./manage.py migrate
./manage.py createsuperuser
```

### Compile the CSS and JS and other assets

```console
make frontend
```

or

```console
gulp
```

### Finally run the server

```console
./manage.py runserver 0.0.0.0:8000
```

## Method 2: Use docker and docker-compose

### Install docker and docker-compose

Follow the instructions to
install [docker](https://docs.docker.com/engine/installation/)
and [docker-compose](https://docs.docker.com/compose/install/) if you
don't have them on your machine.

### Create containers

Create `conf/.env` similary to `conf/.env.example` and save your
information.  Run the following command to build and start containers:

```console
make docker
```

### Migrate and create superuser

```console
sudo docker exec -it aprigi_web bash
./manage.py migrate
./manage.py createsuperuser
exit
```

Now server is ready for you.  But you also need to compile SCSS, JS
and others and make in run properly

```console
make frontend
```

or

```console
gulp
```

# Running the tests

Then in the root directory (next to the ``manage.py`` file) run

```console
tox
```

Behind the scenes this will run the usual `./manage.py test`
management command with a preset list of apps that we want to test as
well as [flake8](https://flake8.readthedocs.io/) for code quality
checks.  We collect test coverage data as part of that `tox` run, to
show the result simply run

```console
coverage report
```

or for a HTML-based report

```console
coverage html
```

# Supported browsers

The goal of the site is to target various levels of browsers,
depending on their ability to use the technologies in use on the site,
such as HTML5, CSS3, SVG, webfonts.

- Desktop browsers, except as noted below, are **A grade**, meaning
  that everything needs to work.
- IE < 10 is **not supported** (based on Microsoft's support).
- Mobile browsers should be considered **B grade** as well.  Mobile
  Safari, Firefox on Android and the Android Browser should support
  the responsive styles as much as possible but some degredation can't
  be prevented due to the limited screen size and other platform
  restrictions.

# File locations

Static files such as CSS, JavaScript or image files can be found in
the ``static`` subdirectory.  (Source files are in `static_src`
folder)

Templates can be found in the `templates` subdirectory.

# Assets (Styles, Javascript and others)

CSS is written in [SCSS](http://sass-lang.com/) and Javascript
libraries such as React are install by `yarn`.

You can use the following command to install dependencies for project:

```console
yarn
```

If you want to update libraries, you can use the above command again.

SCSS and Javascript (include React JSX) are compiled by using gulp,
you can use

```console
gulp
```

or a make task for this

```console
make frontend
```

to compile all of them.  It's also managing other assets such as
images and root files (`robots.txt`, `humans.txt`).

Alternatively you can also run the following command in a separate
shell to continuously watch for changes to the assets files and
automatically compile them

```console
gulp watch
```
