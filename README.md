# SPECS_ChatBot Demo
Repo for the ChatBot Demonstrated in the session 29/03/2023

Our TEL-chatGPT is a Flask-based web application that provides an AI-powered chatbot for Technology Enhanced Learning (TEL) at the University of Hertfordshire. It uses OpenAI's GPT-3.5 Turbo model (configurable for GPT-4) to assist users with queries related to educational technology and teaching and learning concepts.

## Features

- Turn Word documents from the `doc_library` into a CSV file
- Process the CSV file by sending it to the OpenAI embeddings endpoint to create embedding vectors
- A Flask application that allows users to chat with the chatbot and get relevant information
- Greeting and exit phrases handling
- Context-aware responses using OpenAI embeddings

## Installation

1. Clone the repository:

```
git clone https://github.com/KarolynW/SPECS_ChatBot.git
```

2. Change to the SPECS_ChatBot directory:

```
cd SPECS_ChatBot
```

3. Install the required packages:

```
pip install -r requirements.txt
```

4. Set the OpenAI API key as an environment variable:

```
export OPENAI_API_KEY="your_openai_api_key"
```

5. Run the Flask application:

```
python app.py
```

6. Open your browser and navigate to `http://127.0.0.1:5000/` to access the chatbot.

## Usage

Once you have the Flask app running, you can interact with the chatbot through the web interface. The chatbot is designed to assist users at the University of Hertfordshire with Technology Enhanced Learning and general Teaching and Learning concepts. It uses context from embeddings to make sure the responses are relevant to the University of Hertfordshire. If the chatbot does not know the answer to a query, it will inform the user to contact TELSupport@herts.ac.uk.

If a user asks for information unrelated to educational technology or teaching and learning at the University of Hertfordshire, the chatbot will decline to answer and suggest they ask a general AI like ChatGPT.







