from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('CMPE257')
# Create a new trainer for the chatbot
# trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
# trainer.train("chatterbot.corpus.english")


def get_resp(chatbot):
    while(True):
        try:
            resp = chatbot.get_response(input("me: "))
            print("bot: ", resp)
        except(KeyboardInterrupt, EOFError, SystemExit):
            break


get_resp(chatbot)
