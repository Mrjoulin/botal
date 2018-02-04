# BOTAL
Botal is a Python microfraemwork for creating bots for **any** messenger in list bellow. Write code once and use on any messenger. In addition, your code will be simple as a console application. Look at this example ([with comments](https://github.com/dvec/botal/tree/master/examples/helloworld/helloworld.py)):
```python
from botal.handler import Handler
from botal.message import Message
from botal.messengesrs import TelegramMessenger

handler = Handler(TelegramMessenger(token='Your telegram bot token'))

@handler.handler
def on_message(user_id):
    while True:
        handler.messenger.send(user_id, Message('You typed: ' + (yield).text))

if __name__ == '__main__':
    handler.run_handler()
    while True:
        pass
```
This code will respond on any message from telegram. Why do you need to choice botal?
* Simple code
* Messengers integration
* Simple testing

### Supported messengers
* Telegram
* Vk

## Installation
You can install botal by this command:
```
pip install git+git://github.com/dvec/botal
```
