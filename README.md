# Immersive History Learning Platform

This project is a web-based platform designed to provide an immersive and engaging history learning experience. It combines interactive storytelling, AI-powered content generation, and gamified elements to make history more accessible and enjoyable.

## Features

* **Interactive Storytelling:**
    * Users can generate personalized historical stories based on their prompts.
    * Stories are crafted to be immersive, allowing users to "step into" the past.
    * Subtle "Squid Game" Easter eggs are integrated for added engagement.
* **AI-Powered Quiz Generation:**
    * Users can generate quizzes on various historical topics.
    * Quizzes include multiple-choice questions with AI-generated content.
    * "Squid Game" themed messages are displayed based on quiz performance.
* **AI Chatbot:**
    * An AI chatbot provides conversational learning about history.
    * The chatbot maintains context and keeps the conversation focused on historical topics.
    * The bot responds in a "Squid Game" themed fashion.
* **Flowchart Generation:**
    * Users can generate flowcharts about any topic, to help them remember the information.
    * The flowcharts can be downloaded as png or jpeg.
* **Text-to-Speech:**
    * Generated stories can be converted to audio using ElevenLabs API.
    * Audio playback is integrated into the web interface.

## Tech Stack

* **Backend:**
    * Python (Flask)
    * Google Gemini API (for AI content generation)
    * ElevenLabs API (for text-to-speech)
* **Frontend:**
    * HTML, CSS, JavaScript, BootStrap
    * Mermaid.js (for flowchart generation)
    * html2canvas.js (for image capture)
* **Other:**
    * dotenv (for environment variable management)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone [repository URL]
    cd [repository directory]
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    * Create a `.env` file in the project root.
    * Add your API keys:

    ```
    GEMINI_API_KEY=[your Gemini API key]
    ELEVENLABS_API_KEY=[your ElevenLabs API key]
    ```

5.  **Run the application:**

    ```bash
    python app.py
    ```

6.  **Open your browser and navigate to `http://127.0.0.1:5000/`.**

## Usage

* **Storyteller:** Enter a prompt in the "Storyteller" section to generate a historical story.
* **Quiz:** Enter a topic in the "Quiz" section to generate a quiz.
* **Chat:** Use the chat interface to have a conversation with the AI chatbot about history.
* **Flowchart:** Enter a topic in the "Flowchart" section to generate a flowchart.
* **Download Flowcharts:** use the download buttons below the generated flowcharts to download them as images.
