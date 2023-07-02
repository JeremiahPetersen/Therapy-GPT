from flask import Flask, render_template, request, jsonify 
from flask_cors import CORS
import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

conversation = []

def get_completion(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.3,
    )
    return response.choices[0].message["content"]

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    user_message = data.get('prompt')
    conversation.append({"role": "user", "content": user_message})
    model = data.get('model', 'gpt-3.5-turbo')
    response = get_completion(conversation, model)
    conversation.append({"role": "assistant", "content": response})
    return jsonify({"response": response})

@app.route('/api/reset', methods=['POST'])
def reset():
    global conversation
    conversation = []
    return jsonify({"status": "conversation reset"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
