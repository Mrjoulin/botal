# BOTAL
Botal is a Python microfraemwork for creating bots for **any** messenger in list bellow. Write code once and use on any messenger. In addition, your code will be simple as a console application. Look at this example ([with comments](https://github.com/dvec/botal/tree/master/examples/helloworld/helloworld.py)):
```python
from botal.handler import Handler
from botal.datatypes import Message
from botal.messengesrs import Terminal, Telegram

handler = Handler([Terminal(), Telegram(token='Your telegram bot token')])

@handler.handler
def on_message(user):
    while True:
        user.send(Message('You typed: ' + (yield).text))

if __name__ == '__main__':
    handler.run_handler()
```
This code will respond on any message from telegram. Also, you can write a message in stdin, and bot will respond to it. This is a very powerful tool for testing bots. You don't need to write a bot from messenger, you can do right in IDE!
Why do you need to choice botal?
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
