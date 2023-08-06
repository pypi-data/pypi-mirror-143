# PyConversation

Zero-dependency library for chat-bot creators with deadlines.

It allows you to describe a conversation, talk with user according to your schema and restore it, if something went wrong.

### Table of contents

-   <a href="#quickstart">Quickstart</a>
-   <a href="#messages">Messages</a>
    -   <a href="#text">Text</a>
    -   <a href="#group">Group</a>
    -   <a href="#ask">Ask</a>
    -   <a href="#switch">Switch</a>
    -   <a href="#list-ask">ListAsk</a>
    -   <a href="#terminate-group">TerminateGroup</a>
    -   <a href="#own-messages">Creating Own Messages</a>
    -   <a href="#message-transfer">MessageTransfer</a>
-   <a href="#loggers">Loggers</a>
    -   <a href="#dict-logger">DictLogger</a>
    -   <a href="#json-file-logger">JsonFileLogger</a>
    -   <a href="#own-loggers">Creating Own Loggers</a>
-   <a href="#sender">Message Sender</a>
-   <a href="#compatibility">Compatibility</a>

## <a id="quickstart"></a>Quickstart

### First we need to create a message schema, which consists of messages.

Messages describe chat-bot's actions. For instance, send a text message, which doesn't need any feedback or ask a question. Each message has a unique id. Most common types of messages are `Group`, `Text` and `Ask`.

For full details about different message types <a href="#messages">see Messages</a>

`Group` is a kind of container, that holds list of other messages.

`Text` sends a text message, which doesn't require any feedback.

`Ask` sends a text message and waits for an answer

Enough theory, let's see an example!

```python
from pyconversation import Group, Text, Ask

fruit_bot_conversation = Group(
    id="root",
    children=[
        Text(id="root.hello", text="Hello!"),
        Ask(id="root.fruits", text="What fruits do you like?"),
        Text(id="root.bye", text="Bye"),
    ],
)
```

In this example, we create a schema for simple bot, who asks which fruits does user like. Root message is a `Group`. It holds a block of messages. First of them is a `Text` which sends user a greeting message. Second one (`Ask`) asks about user's favorite fruit and waits for answer. And finally, third `Text` message sends `Bye` to user.

### Second step - we need a logger

Logger is an object, which stores user's answers and message history. This library exposes 2 loggers:

-   `DictLogger` - stores data in a dictionary
-   `JsonFileLogger` - takes file path as a parameter and stores json data in this file

If you need something different, <a href="#own-loggers">see Creating Own Loggers</a>

But now let's use `DictLogger`

```python
from pyconversation import DictLogger

logger = DictLogger()
```

That's all!

For full loggers documentation <a href="#loggers">see Loggers</a>

### But how to send those messages?

The answer's simple - using a `MessageSender`!

Example code:

```python
from pyconversation import Group, Text, Ask, DictLogger, MessageSender

# Conversation from step 1
fruit_bot_conversation = Group(
    id="root",
    children=[
        Text(id="root.hello", text="Hello!"),
        Ask(id="root.fruits", text="What fruits do you like?"),
        Text(id="root.bye", text="Bye"),
    ],
)

# Logger from step 2
logger = DictLogger()

# Initialize a message sender
sender = MessageSender(
    root=fruit_bot_conversation, # Our conversation
    logger=logger, # Our logger
    send=print # A send function, which takes a string and sends the message. In this case, we use print to log messages to console
)

# Answer to the question before the first one is always empty
answer = None

# Send messages!
while True:
    # Send messages one by one, until we run into a message, which requires an answer
    # This function takes answer to previous question as a parameter
    sender.send_all_skippable(answer)

    # If all messages sent
    if sender.finished:
        # Dispose of sender's resources (like open files) and get the result!
        print("\nResult:", sender.finalize())
        break

    # If not all messages have been sent and we still need an answer, ask!
    answer = input()
```

Done! If you run this, you'll get the following in the console:

```
Hello!
What fruits do you like?
<your answer'll be here>
Bye

Result: {'root.fruits': '<your answer>'}
```

And one more example with decorated function (like in real chat-bots):

```python
bot = ... # Initialize chat bot

sender = None

@bot.connection
def on_connection(user_id):
    sender = MessageSender(
        root=conversation, # Our conversation
        logger=logger, # Our logger
        send=lambda text: bot.send(user_id, text)
    )

    sender.send_all_skippable(None)

@bot.message
def on_message(user_id, message):
    sender.send_all_skippable(message)

    if sender.finished:
        print("\nResult:", sender.finalize())
        sender = None
```

For full message sender documentation <a href="#sender">see Message Sender</a>

### You've created your first chat-bot with clever conversation! Here quick tutorial ends.

## <a id="messages"></a>Messages

### <a id="text"></a>Text

Text message sends some text, which doesn't require user's answer

Constructor parameters:

-   `id` (str) - unique message id
-   `text` (str) - text to send

Usage example:

```python
Text(id="hello", text="Hello, user!")
```

### <a id="group"></a>Group

Group is a message, which doesn't send anything and doesn't require an answer. It's just a container for a list of messages

Constructor parameters:

-   `id` (str) - unique message id
-   `children` (list\[message\]) - list of messages to send

Usage example:

```python
Group(
    id="group",
    children=[
        Text(id="hello", text="Hello!"),
        Text(id="bye", text="Good bye!"),
    ],
)
```

### <a id="ask"></a>Ask

Ask message send some text to user and waits for an answer

Constructor parameters:

-   `id` (str) - unique message id
-   `text` (str) - question text

Usage example:

```python
Ask(id="name", text="What's your name?")
```

### <a id="switch"></a>Switch

Switch message asks user a question and sends a message depending on user's answer.

Constructor parameters:

-   `id` (str) - unique message id
-   `text` (str) - question text
-   `answer_map` (dict\[str, message\]) - dict, where key is user's answer and value is a message
-   `fallback` (message?) - message, which'll be sent if answer doesn't match anything in `answer_map` dict
-   `repeat_on_fallback` (bool?) - if true, after fallback was sent question is asked over and over again until answer matches something in `answer_map` dict

Usage example:

```python
Switch(
    id="fruit"
    text="What fruit do you like?"
    answer_map={
        "apple": Text(id="apple", text="Yeah, apples are delicious!"),
        "peach": Text(id="peach", text="Me too!"),
        "feijoa": Text(id="feijoa", text="I don't know that fruit!"),
    },
    fallback=Text(id="dont_understand", text="Sorry, I didn't understand you"),
    repeat_on_fallback=True
)
```

### <a id="list-ask"></a>ListAsk

ListAsk asks user a question and waits for several answers.

In result dictionary it's represented by an array.

Constructor parameters:

-   `id` (str) - unique message id
-   `text` (str) - question text
-   `stop_command` (str) - if user sends this string as an answer, ListAsk finishes waiting for answers
-   `max_count` (int?) - maximal count of answers

Usage example:

```python
ListAsk(
    id="fruits",
    text="What fruits do you like? Enter 'that's all' if you can't remember any more",
    stop_command="that's all",
    max_count=10,
)
```

### <a id="terminate-group"></a>TerminateGroup

TerminateGroup sends another message and then terminates sending group, inside which it is located

Constructor parameters:

-   `id` (str) - unique message id
-   `child` (message?) - message to send before terminating the group

Usage example:

```python
Group( # This group's gonna be terminated
    id="group",
    children=[
        Text(id="hello", text="Hello!"),
        Switch(
            id="bye_condition",
            text="Can I say bye?",
            answer_map={
                "yes": Text(id="bye", text="Good bye!")
            },
            fallback=TerminateGroup(
                id="terminate",
                child=Text(id="eh", text="Eh..."),
            ),
        ),
        Text(id="what", text="What?!"), # This will not be sent,
    ],
)
```

### <a id="own-messages"></a>Creating Own Messages

Every message is a class, so to create your own message, you just need to inherit `BaseMessage` class (It can be imported like this: `from pyconversation import BaseMessage`)

Usage example:

```python
from pyconversation import Text, BaseMessage, BaseLogger, MessageTransfer, MessageTransferGenerator

class HelloMessage(BaseMessage):
    username: str

    def __init__(self, *, id: str, username: str) -> None:
        super().__init__(id=id) # BaseMessage takes one parameter - id
        self.username = username

    def _base_iterator(self, logger: BaseLogger) -> MessageTransferGenerator: # This is an abstract method
        text_message = Text(id=f"{self.id}.text", text=f"Hello, {self.username}!")

        yield from text_message.iterator(logger)

        answer = yield MessageTransfer(
            id=self.id,
            text="Is it your real name?",
        )

        logger.log(self.id, answer)
```

As you can see, each message has an iterator method, which takes logger as a parameter and returns a generator. Also, this message gets an answer and logs it to logger. Details on how to interact with logger and log answers will be explained in <a href="#loggers">Loggers</a>

But what is that `MessageTransfer` object? It's used to pass string message to sender and get an answer. Details in next article.

### <a id="message-transfer"></a>MessageTransfer

Message transfer is used to pass string message to sender and get an answer. It can be `yield`ed from message's generator.

Constructor parameters:

-   `id` (str) - message's unique id
-   `text` (str?) - text, which'll be sent to user or None, if you don't want to ask any questions, you just need an answer
-   `skip` (bool?) - if true, this question doesn't need an answer and won't wait for it.
-   `terminate_group` (bool?) - when this is true, group which intercepted such transfer processes it and terminates.

Usage example in upper **Creating Own Messages** section

## <a id="loggers"></a>Loggers

Loggers are used to store users' answers and message history.

Message history is a list, where question ids are stored. It's used to restore conversation. For example, if user has already answered several questions and suddenly the server stops, last sent message id will be taken from history, and conversation will begin from the last message.

### <a id="dict-logger"></a>DictLogger

DictLogger stores answers and history in-memory (in a dictionary). So it's just an example to play with the library. Don't use it in production code.

No constructor parameters.

Usage example:

```python
logger = DictLogger()
```

### <a id="json-file-logger"></a>JsonFileLogger

JsonFileLogger stores everything in a JSON file. JSON file stays on the computer anyway, so when server suddenly stops and the reboots, your bot'll be able to continue conversation from the right place.

Constructor parameters:

-   `file_path` (str) - JSON file's absolute path. It must be unique between all conversations on this server.

Usage example:

```python
logger = JsonFileLogger(pathlib.Path(__file__).parent / "conversation.json")
```

### <a id="own-loggers"></a>Creating Own Loggers

If you need to create your own logger (and you'll need it more often, than creating own messages) you need to inherit the `BaseLogger` class.

It has the following abstract methods:

-   `log` (-> None) - stores answer by message's unique id

    Parameters:

    -   `id` (str) - message unique id
    -   `value` (str) - answer

-   `set_array` (-> None) - initializes empty list in answer dictionary using message unique id as a key

    Parameters:

    -   `id` (str) - message unique id

-   `add_array_item` (-> None) - add item to existing list using message id as answer dictionary key

    Parameters:

    -   `id` (str) - message unique id
    -   `value` (str) - value to add to list

-   `get` (-> union\[str, list\[str\], None\]) - get message answer or list of answers by message id if exists

    Parameters:

    -   `id` (str) - message unique id

-   `get_result_dict` (-> dict\[str, union\[str, list\[str\]\]\]) - get full answer dictionary

    No parameters

And also the following virtual methods (not necessary to implement):

-   `reset_history` (-> None) - remove all elements from message history list

    No parameters

-   `log_last_id` (-> None) - add message id to message history list

    Parameters:

    -   `id` (str) - message unique id

-   `get_last_id` (-> str?) - get last sent message id (last element in message history list)

    No parameters

-   `finalize` (-> None) - dispose of logger's resources (open files, socket connections, etc.)

    **Note**: This method is called when the conversation is finished. So, for instance, `JsonFileLogger` deletes it's data file in this method.

    No parameters

Usage example:

```python
from typing import Union, List, Dict
from pyconversation import BaseLogger

class MySocketLogger(BaseLogger):
    socket: Socket

    def __init__(self) -> None:
        super().__init__()
        self._connect_socket()

    def log(self, id: str, value: str) -> None:
        self.socket.emit("SET_OR_REPLACE", {"id": id, "value": value})

    def set_array(self, id: str) -> None:
        self.socket.emit("SET_OR_REPLACE", {"id": id, "value": []})

    def add_array_item(self, id: str, value: str) -> None:
        self.socket.emit("ADD_ARRAY_ITEM", {"id": id, "value": value})

    def get(self, id: str) -> Union[str, List[str]]:
       return self.socket.emit("GET", {"id": id})

    def get_result_dict(self) -> Dict[str, Union[str, List[str]]]:
        return self.socket.emit("GET_ALL")

    def reset_history(self) -> None:
        self.socket.emit("SET_HISTORY", [])

    def log_last_id(self, id: str) -> None:
        self.socket.emit("ADD_HISTORY", id)

    def get_last_id(self, id: str) -> Union[str, None]:
        if not self.socket.emit("HISTORY_EMPTY"):
            return self.socket.emit("GET_LAST_IN_HISTORY")

    def finalize(self) -> None:
        self.socket.emit("CLEAR_EVERYTHING")
        self._disconnect_socket()

    def _connect_socket(self) -> None:
        self.socket = ... # We'll log our data using a socket

    def _disconnect_socket(self) -> None:
        self.socket.disconnect()
        self.socket = None
```

## <a id="sender"></a>Message Sender

Message sender is used to simplify conversation restoring and message sending.

Constructor parameters:

-   `root` (message) - root message (aka message schema)
-   `logger` (logger) - logger
-   `send` (function (str) -> None) - send function (takes string and sends it to user)
-   `headline_text` (str?) - text, which'll be sent to user whent message sender is constructed. Whether conversation is constructed or restored, it's sent anyway.
-   `stop_command` (str?) - if user sends this as an answer, conversation terminates.

Exposed properties:

-   `finished` (bool) - is conversation finished (true if all messages have been sent or conversation has been stopped by stop command)
-   `terminated` (bool) - is conversation terminated (true if conversation was stopped by stop command)

Exposed methods:

-   `send_all_skippable`
    Send all messages until sender runs into a message, which requires an answer.

    Parameters:

    -   `prev_answer` (str?) - answer to previous message

See usage example in <a href="#quickstart">Quickstart</a>

## <a id="compatibility"></a>Compatibility

This library is compatible with Python>=3.6

&copy; 2021 Roman Melamud
