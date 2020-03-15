from flask import Flask
from flask import request, jsonify
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

app = Flask(__name__)


# chatbot = ChatBot('CMPE257')
chatbot = ChatBot(
    'CMPE257',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri='mongodb+srv://admin:admin@cluster0-3inox.mongodb.net/test?retryWrites=true&w=majority'
)

# Create a new trainer for the chatbot
trainer = ListTrainer(chatbot)
@app.route('/train', methods=["POST"])
def chatbotTrainer():
    print("Inside Training")
    data = request.get_json()
    conversation = data['data']
    # print(conversation)
    trainer.train(conversation)
    result = "Model is trained"
    # print(result)
    return jsonify({"response": result})


@app.route('/inference', methods=["POST"])
def get_resp():
    try:
        print("Inside inference")
        data = request.get_json()
        question = data['q']
        resp = chatbot.get_response(question)
        # print("Question: ", question)
        # print("Answer: ", resp)
        # print(result)
        return jsonify({"response": str(resp)})
    except(Exception):
        print("Exception:: ")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
