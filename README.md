# BOTAL
Botal is a Python microframework for creating bots. Example for Vk:
```python
from botal import VkBot

bot = VkBot(tokens=['SECRET_1', 'SECRET_2'])

@bot.handler
def on_message(user_id):
    while True:
        bot.messages.send(user_id, message='You typed: {}'.format((yield).text))

if __name__ == '__main__':
    bot.run()
```
This code will respond on any message from vk. Why do you need to choice botal?
* Simple code
* Messengers integration
* Simple testing

## Installation
You can install botal by this command:
```
pip install git+git://github.com/Mrjoulin/botal
```
