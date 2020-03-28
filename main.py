from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
from chatterbot.response_selection import get_most_frequent_response
from chatterbot.comparisons import synset_distance
# chatbot = ChatBot('CMPE257')

chatbot = ChatBot(
    'CMPE257', logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        # 'chatterbot.logic.TimeLogicAdapter',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'statement_comparison_function': synset_distance,
            'maximum_similarity_threshold': 0.90
        }, {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'How to Login?',
            'output_text': 'Ok, here is a link: http://www.mtaas.com/login/'
        },

    ], preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    response_selection_method=get_most_frequent_response,
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri='mongodb+srv://admin:admin@cluster0-3inox.mongodb.net/test?retryWrites=true&w=majority'
)
# Create a new trainer for the chatbot
# trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
# trainer.train("chatterbot.corpus.english")


def get_feedback():

    text = input()

    if 'yes' in text.lower():
        return True
    elif 'no' in text.lower():
        return False
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback()


def get_resp(chatbot):
    while(True):
        try:
            input_statement = Statement(text=input())
            resp = chatbot.get_response(input_statement)
            print("bot: ", resp)
            print('\n Is "{}" a coherent response to "{}"? \n'.format(
                resp,
                input_statement.text
            ))
            if get_feedback() is False:
                print('please input the correct one')
                correct_response = Statement(text=input())
                chatbot.learn_response(correct_response, input_statement)
                print('Responses added to bot!')
        except(KeyboardInterrupt, EOFError, SystemExit):
            break


get_resp(chatbot)
