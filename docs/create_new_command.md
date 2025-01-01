# Create a New Command

There are a few steps to follow when creating a new command.

## Create the Command and Add the Respective Handler

First, add your code to `bot/handlers.py` and register your new command in the `HANDLERS` constant at the end of the file.

## Update the Help Command

You must also update the `/help` command to include the new command.

## Add the Command to the Command List

You need to add the command in the [Bot Manual Settings](/bot_manual_settings.md) and set up the full, updated command 
list in your Telegram bot (by talking to BotFather).

## (Optional) Add Instructions to Functional Test the New Command

Edit the [Functional Testing](/functional_testing.md) to include the new command.
