from botal.handler import Handler
from botal.messengesrs import Terminal, Vk

# This is handler for the terminal
handler = Handler([Terminal()])


# Or you can use the handler for vk
# handler = Handler([Vk(login='Your vk login', password='Your vk password')])

# Or for terminal and vk both
# handler = Handler([Terminal, Vk(login='Your vk login', password='Your vk password')])

# This annotation indicates that this function will be called when message is received from a new user
@handler.handler()
def on_message(user_info):
    # user_info is an instance of the UserInfo object
    while True:
        # When user will write new message, it will be passed into this generator by using generator.send
        # message is an instance of the Message object
        message = yield
        # You can send message to the user by yielding it
        yield 'You typed: "{}"'.format(message.text)


if __name__ == '__main__':
    # Finally, we need to run handler
    handler.run_handler()

# Now run this code and type something in terminal. You will see something like this:
# Hello!
# You typed: "Hello!"
