# Gastitis

Telegram bot as a tool to keep track of your expenses.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for
development and testing purposes. See deployment for notes on how to deploy the project on a live
system.

### How to use

Once you have your server setup, just start a chat with your bot using the Telegram client.
For a description of available commands, use the `/help` command.


### Creating a Telegram Bot

In order to test or deploy this project, first you have to talk to Bot Father to create your own
bots. More details [here](https://core.telegram.org/bots#6-botfather).

I strongly recommend to create two bots: one for testing, to be used in your
[dev environment](#setting-up-a-dev-environment) and another one for production, used in the
[deployment](#deployment).


### Setting up a dev environment

First, you need to [create a testing Telegram Bot](#creating-a-telegram-bot).

Once you have your testing bot, you need to create a file in `gastitis/secret_settings.py` with the
following content with the token of your testing bot)

```python
TELEGRAM_BOT_TOKEN = '' # place here your bot token

DJANGO_SECRET_KEY = '' # place here a django secret_key (https://docs.djangoproject.com/en/4.1/ref/settings/#secret-key)

DATABASE_SETTINGS = {  # Set None to use sqlite
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': '',  # database name
    'USER': '',  # database user
    'PASSWORD': '', # database password
    'HOST': '127.0.0.1',
    'PORT': '5432',
}
```

Next, you have to create a new virtual environment, install the requirements, run the migrations
and start the dev bot:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py startbot
```
Now you can talk to your bot in telegram! Send your bot `/help` to see the available commands.

If you want to watch the expenses you have load, or any other information saved by your bot, you
need to create a super user:
```
python manage.py createsuperuser
```
Follow the prompt steps and create a user, then run the web locally:
```
python manage.py runserver
```
From your browser, go to http://localhost:8000/admin enter your username and password (created in
the previous step) and now you can explore the data that your bot has generated!


## Deployment

You can easily deploy this project on Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

You will need to set the environment variable `BOT_TOKEN` to a valid Telegram Bot authorization
token. This implies [creating your own Telegram bot](#creating-a-telegram-bot).

## Authors

* Sofía Denner

## License

TBD
