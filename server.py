from flask import Flask
from flask import request, jsonify
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from flask_cors import CORS
import sys
import os
import dbconnection

app = Flask(__name__)
CORS(app)

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


@app.route('/getSuggestions', methods=["POST"])
def getSuggestions():
    try:
        print("Inside getSuggestions")
        data = request.get_json()
        role = data['Role']
        page = data['Page']
        suggestions = database.suggestions
        result = suggestions.find_one({"Role": role, "Page": page})
        # resp = chatbot.get_response(question)
        # print("Question: ", question)
        # print("Answer: ", resp)
        # print(result['Questions'])
        return jsonify({"suggestions": result['Questions']})
    except(Exception):
        print("Exception:: ")


@app.route('/save', methods=["POST"])
def save_questions():
    try:
        print("Inside saveQuestions")
        data = request.get_json()
        role = data['Role']
        page = data['Page']
        questions = data['Questions']
        print(data, role, questions)
        # resp = chatbot.get_response(questions)
        res = saveSuggestions(role, page, questions)
        print(res)
        # print("Question: ", question)
        # print("Answer: ", resp)
        # print(result)
        return jsonify({"response": "Done"})
    except(Exception):
        print("Exception:: ")


def conn():
    connectionString = "mongodb+srv://admin:admin@cluster0-3inox.mongodb.net/test?retryWrites=true&w=majority"
    db_name = "test"
    sys.path.append(os.path.abspath("../"))
    from dbconnection.connect import MongoConnection
    connection = MongoConnection(connectionString, db_name)
    database = connection.connect()
    return database


def saveSuggestions(role, page, questions):
    print("Inside saveSuggestions", role, page, questions)
    suggestions = database.suggestions
    res = suggestions.insert_one({"Role": role,
                                  "Page": page,
                                  "Questions": questions
                                  })
    return res


if __name__ == '__main__':
    database = conn()
    app.run(host='0.0.0.0', port=80)
