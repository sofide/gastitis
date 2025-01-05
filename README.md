# Gastitis
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)

**Gastitis** is a Telegram bot designed to help you track your expenses easily and efficiently.

---

## Setting Up a Development Environment


Follow these instructions to get a copy of the project up and running on your local machine.

### Creating a Telegram Bot

To test or deploy this project, you need to create your own bots via **BotFather**.  
Refer to the [Telegram Bot documentation](https://core.telegram.org/bots#6-botfather) for detailed steps.

It's recommended to create two bots:
- **Testing Bot**: For use in your [development environment](#setting-up-a-dev-environment).
- **Production Bot**: For deployment in your live environment.

### Creating a settings file 

Prepare a configuration file at `gastitis/secret_settings.py` with the following content:

```python
TELEGRAM_BOT_TOKEN = ''  # Place your bot token here.

DJANGO_SECRET_KEY = ''  # Generate a Django secret key (see https://docs.djangoproject.com/en/4.1/ref/settings/#secret-key).

DATABASE_SETTINGS = None  # Use 'None' to run Gastitis with SQLite.

DATABASE_SETTINGS = {  # Use these settings for a specific database (e.g., PostgreSQL).
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': '',  # Database name.
    'USER': '',  # Database username.
    'PASSWORD': '',  # Database password.
    'HOST': '127.0.0.1',
    'PORT': '5432',
}
```

>  Note: For setting up a specific database like PostgreSQL, refer to the [Database Setup Guide](docs/database_setup.md).

### Setting Up Google Credentials for the /export Command
The `/export` command requires Google credentials. Follow these steps to set them up:

1. Create a Google service account following the gspread documentation.
2. Download the credentials JSON file provided by Google.
3. Save the JSON file to the following location: gastitis/google_credentials.json.


### Installation Steps

1. Create a virtual environment and activate it:
```bash
python3 -m venv env
source env/bin/activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Apply database migrations:
```bash
python manage.py migrate
```

4. Start your bot:
```bash
python manage.py startbot
```
You can now interact with your bot in Telegram! Use /help to see the available commands.

### Accessing the Admin Panel

If you want to view the expenses you've added or any other data stored by your bot, you need to create 
a superuser for the Django admin panel:

1. Create a superuser:
```bash
python manage.py createsuperuser
```

2. Run the development server:
```bash
python manage.py runserver
```

3. Access the admin panel: Open your browser and go to http://localhost:8000/admin. Log in with the superuser 
credentials you created in the previous step.

You can now explore the data your bot has generated!


### Extra Optional Steps: Configure Your Telegram Bot

Enhance your Telegram bot's functionality by customizing its settings. Follow the instructions in the [Bot Manual Settings](docs/bot_manual_settings.md) for detailed guidance.  

## Contributing

- After making any changes to the code, please run the [functional tests](docs/functional_testing.md) to ensure everything is working as expected.
- If you are adding a new command, follow the instructions in the [Create a New Command](docs/create_new_command.md) section.

## Authors

* Sofía Denner

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
