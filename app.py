# app.py
from flask import Flask, render_template, request, jsonify
from chatv2 import load_chatbot_data, load_chatbot_model, get_chatbot_response

app = Flask(__name__)

words, labels, training, output, data = load_chatbot_data()
model = load_chatbot_model(training, output)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    bot_response = get_chatbot_response(user_input, model, words, labels, data)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
