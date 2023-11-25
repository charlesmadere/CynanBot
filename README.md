# CynanBot

Welcome to the repository for [CynanBot](https://www.twitch.tv/cynanbot), the Twitch trivia game bot.

If you'd like to add CynanBot to your Twitch stream, please talk to me on Discord (`smCharles#1100`) or Twitch ([`smcharles`](https://www.twitch.tv/smcharles)). However, given the time I've put into this bot in the past, and also just generally continue to do, I am asking for a small donation (one month sub to my Twitch channel). I understand if you don't want to pay this, that is fine, the bot is open source after all. However, I have no obligation or responsibility to help you with your own fork or variant of this bot, if you choose to go that route. Feel free to chat with me if you have any questions.

CynanBot is rapidly growing, and its codebase is split between two repositories. This repository seeks to encapsulate all of the Twitch/bot related code, whereas [CynanBotCommon](https://github.com/charlesmadere/CynanBotCommon) is where all of the business logic is.

---

to install:
```
python -m pip install pipenv
python -m pipenv install
```

to install the `CynanBotCommon` library:
```
python -m pip install -r requirements.txt
```

for an editable (development) install,
assuming `CynanBotCommon` is a sibling directory to `CynanBot`:
```
python -m pip install -e ../CynanBotCommon/
```

This might require:
```
python -m pip install --upgrade pip
```
