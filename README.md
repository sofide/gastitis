# Gastitis

Telegram as a tool to keep track of your expenses

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### How to use

Once you have your server setup, just start a chat with your bot using the Telegram client. For a description of available commands, use the `/help` command.

### Setting up a dev environment

Just create a new virtual environment, install the requirements, run the migrations and start the dev bot:
```
python3 -m venv env
source env/bin/activate
python manage.py migrate
python manage.py startbot
```

## Deployment

You can easily deploy this project on Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

You will need to set the environment variable `BOT_TOKEN` to a valid Telegram Bot authorization token. This implies creating your own Telegram bot. More details [here](https://core.telegram.org/bots#6-botfather).

## Authors

* Sofía Denner

## License

TBD
