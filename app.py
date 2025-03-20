from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

from dotenv import load_dotenv
import os

# Gemini imports
from google import genai
from google.genai import types
# ElevenLabs imports
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from io import BytesIO
import base64
# Chat imports
import logging
from google.genai.types import Content  # Import the correct type
# Flowchart imports
import mermaid
# Deepgram imports
from deepgram.utils import verboselogs
from deepgram import (
    DeepgramClient,
    SpeakOptions,
)

logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
story_instruct="""You are a historian and an interactive storyteller, tasked with creating immersive historical narratives. Your goal is to transform historical facts into engaging experiences, enabling learners to 'step into' the past rather than passively consuming information. Begin each story with 'Once upon a time, in a world where history came alive...' and continue with the user's input. End each story with 'And so, the threads of history continued to weave their intricate tale.'

To enhance the immersive experience, subtly incorporate interactive elements within the story. For example, present the user with choices that influence the narrative's direction, or ask them to solve historical puzzles.

As a hidden Easter egg, occasionally include subtle visual or textual references to 'Squid Game' within the story's descriptions or scenarios. These references should be brief and seamlessly integrated, serving as a playful nod to the show without detracting from the historical learning experience. Examples:

* Describe a scene with 'participants' facing a challenging 'game' or 'test'.
* Mention 'numbered participants' or 'players' in a historical context.
* Use geometric shapes (circle, triangle, square) in descriptions of objects or environments.

Remember, the primary focus is on delivering an engaging and educational historical narrative. The 'Squid Game' references should be subtle and serve as a hidden surprise, not a central theme.
"""
gemini_api_key = os.getenv('GEMINI_API_KEY')
gemini_client = genai.Client(api_key=gemini_api_key)

elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
elevenlabs_client = ElevenLabs(
  api_key=elevenlabs_api_key,
)



app = Flask(__name__)

def generate_story(prompt):
    response = gemini_client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(system_instruction=story_instruct),
    contents=[prompt]
    )
    return response.text

def generate_story_audio(story):
    # trim the story to less than 2000 characters
    story = story[:1999]
    try:
        SPEAK_TEXT = {"text": story}
        deepgram = DeepgramClient()
        options = SpeakOptions(
            model="aura-asteria-en",
        )
        response = deepgram.speak.rest.v("1").save("static/audio/output.mp3", SPEAK_TEXT, options)
        print(response.to_json(indent=4))
    except Exception as e:
        print(f"Exception: {e}")

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/storyteller', methods=['GET', 'POST'])
def storyterller():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        response = generate_story(prompt)
        audio = generate_story_audio(response)
        if response:
            # Generate Base64 audio to embed in HTML
            # audio_base64 = generate_story_audio(audio)
            # return render_template('storyteller.html', response=response, audio=audio_base64)
            return render_template('storyteller.html', response=response)

    return render_template('storyteller.html')

quiz_instruct = """You are a quiz master and you have to generate a quiz based on 
the user's input. Make 5 questions based on the user's input. 
The questions should be of medium difficulty. Each question should have 4 options. 
The correct answer should be one of the options. 
The quiz should be based on the user's input. Return the quiz in JSON format.

Use this JSON schema:

{    
'question': str
'a': str
'b': str
'c': str
'd': str
'correct': str
},
{
'question': str
'a': str
'b': str
'c': str
'd': str
'correct': str
},
{
'question': str
'a': str
'b': str
'c': str
'd': str
'correct': str
},
{
'question': str
'a': str
'b': str
'c': str
'd': str
'correct': str
},
{
'question': str
'a': str
'b': str
'c': str
'd': str
'correct': str
}

Return: list[quiz]

don't use ```json, just return the raw JSON object.
"""
def generate_quiz(topic):
    response = gemini_client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(system_instruction=quiz_instruct),
    contents=[topic]
    )
    print(response.text)
    response = response.text.replace("```json", "")
    response = response.replace("```", "")
    return json.loads(response)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        topic = request.form.get('topic')
        quiz_data = generate_quiz(topic)    
        if "```json" in quiz_data:
            # remove the ```json from the response
            quiz_data = quiz_data.replace("```json", "")
            quiz_data = quiz_data.replace("```", "")

        if quiz_data:
            return render_template('quiz.html', quiz_data=(quiz_data))
    return render_template('quiz.html')

chat_instruct = """You are a helpful chatbot. Respond to the user's questions or statements in a conversational manner.
Maintain context throughout the conversation. But keep the conversation only related to histroy. if the user asks about any other topic, bring back the conversation to history.
"""

chat_history = []  # Store conversation history

def generate_chat_response(user_input):
    global chat_history
    chat_history.append(Content(parts=[{"text": user_input}], role="user"))

    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(system_instruction=chat_instruct),
        contents=chat_history
    )

    if response.text: # check if text exists
        bot_response = response.text
        chat_history.append(Content(parts=[{"text": bot_response}], role="model"))
        return bot_response
    else:
        return "Sorry, I couldn't generate a response."

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input:
            bot_response = generate_chat_response(user_input)
            return render_template('chat.html', user_input=user_input, bot_response=bot_response, chat_history=chat_history)
    return render_template('chat.html', chat_history=chat_history)

flowchart_instruct = """You are a flowchart generator. Generate a flowchart in Mermaid syntax based on the user's topic.
The flowchart should be simple and easy to understand.
The flowchart should have at least 5 nodes.
Return only the mermaid code.
don't use ( and ) in the mermaid code. As it is wrong syntax.
"""

def generate_flowchart(topic):
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(system_instruction=flowchart_instruct),
        contents=[topic]
    )
    # replace the ```mermaid from the response
    response = response.text.replace("```mermaid", "")
    response = response.replace("```", "")
    print(response) #added print statement.
    return response

@app.route('/flowchart', methods=['GET', 'POST'])
def flowchart():
    if request.method == 'POST':
        topic = request.form.get('topic')
        flowchart_code = generate_flowchart(topic)
        if flowchart_code:
            if "graph" in flowchart_code: #basic check for valid mermaid code.
                return render_template('flowchart.html', flowchart_code=flowchart_code)
            else:
                return render_template('flowchart.html', flowchart_code="The AI returned invalid mermaid code.")
        else:
            return render_template('flowchart.html', flowchart_code="The AI returned an empty response.")
    return render_template('flowchart.html')

if __name__ == '__main__':
    app.run(debug=True)