# Frustrated_Programmer
A bot that finds profanity in latest public github commit messages and tweet randomly.

https://twitter.com/frustrated_bro

![bot_image](https://i.imgur.com/byTdo5C.png)

## Installation

It uses Tweepy to access twitter API

```
pip install tweepy 

```


## Configuration

Create an [app in twitter](https://apps.twitter.com/) and copy-paste consumer_key,consumer_secret,access_token and access_token_secret to the config.py file.

## TODO

- [x] Fix new line bug
- [x] Filter duplicate messages
- [ ] Handle when early hours search returns empty
- [ ] Better error handling
- [ ] Fix relative path	