from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# chatbot = ChatBot('CMPE257')
chatbot = ChatBot(
    'CMPE257',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri='mongodb+srv://admin:admin@cluster0-3inox.mongodb.net/test?retryWrites=true&w=majority'
)

# Create a new trainer for the chatbot
trainer = ListTrainer(chatbot)

# Train the chatbot based on the english corpus
# trainer.train("chatterbot.corpus.english")

# Get a response to an input statement
# resp = chatbot.get_response("Hello, how are you today?")
# print(resp)


def train_model(trainer):
    conversation = []
    while(True):
        try:
            conversation.append(input())
        except(KeyboardInterrupt, EOFError, SystemExit):
            trainer.train(conversation)
            break


train_model(trainer)
