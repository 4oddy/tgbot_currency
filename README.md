# tgbot_currency

Simple Telegram bot to know exchange rate of each currency 

It works by Russian Central Bank API

Also with this bot you can translate one currency in other

# how to start this bot

# With docker
 
First of all, insert your token into token.env file in this format

`token='your_token'`

Then, execute this

`docker build .`

This command will build an image of this app

Then, you have to do this

`docker run [image_id]`

This will start a new docker container on image you have done before
  
# Without docker
First of all, install requirements.txt by

`pip install -r requirements.txt`

Then, insert your Telegram bot's token into token.env file

`token='your_token'`

And in the end

`python main.py`

Enjoy!
