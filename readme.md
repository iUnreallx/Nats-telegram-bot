## NATS WITH TELEGRAM BOT MAILING SYSTEM

**What can this bot do?**
* Able to greet the user
* Subscribe user to newsletter
* Send as administrator
* Ensure that all messages are delivered
* Clear the database to resend the newsletter

**How to install and use the bot?**
* Get your token from @BotFather and put it in .env.
* Start your postgres data resources, start the server and transfer the data for connection.
* Run nats in your terminal, make sure there is a connection
* Next, create a stream that will serve as our intermediary:
* thread > sudo nats add MESSAGES --subjects "messages.*" --storage file --storage limits
* Now we need Python 3.x
* Let's install everything depending on: > pip install -r require.txt
* Let's put all the variables in .env
* Let's run the bot: python3 bot.py

Ready!