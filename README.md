# BOTAL
Botal is a Python microframework for creating bots. Example for Vk:
```python
from botal import Botal
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll

sess = VkApi(token='SECRET')
api = sess.get_api()
lp = VkLongPoll(sess)

handler = Botal(filter(lambda x: x.to_me, lp.listen()), lambda x: x.user_id)

@handler.handler
def on_message(user_id):
    while True:
        api.messages.send(user_id, message='You typed: {}'.format((yield).text))

if __name__ == '__main__':
    handler.run()
```
This code will respond on any message from vk. Why do you need to choice botal?
* Simple code
* Messengers integration
* Simple testing

## Installation
You can install botal by this command:
```
pip install git+git://github.com/dvec/botal
```
