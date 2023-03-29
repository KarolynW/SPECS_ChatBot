"""
This code defines a Flask web application that serves as a chatbot interface for interacting with an OpenAI GPT-3.5-turbo model. The chatbot is designed to assist users with Technology Enhanced Learning (TEL) and general Teaching and Learning concepts at the University of Hertfordshire. The code imports necessary libraries, sets up the Flask app, and defines the routes and functionality for the chatbot.

Here's a step-by-step explanation of the code:

1. Import necessary libraries: os, unittest, pandas, openai, numpy, Flask, request, jsonify, render_template, and dotenv.
2. Set the OpenAI API key and model.
3. Initialize the Flask app.
4. Define exit phrases that will trigger the exit loop.
5. Set the maximum number of messages to keep in the messages_log.
6. Initialize the chat with a system greeting and user input.
7. Define the route for the home page, which renders the 'index.html' template.
8. Define the route for handling user input and returning the AI response as a JSON object. This route performs the following actions:
    a. Get user input from request data.
    b. Check if the user input contains any exit phrases.
    c. Load embeddings data from the CSV file.
    d. Get the embeddings for the user's question.
    e. Calculate distances from the embeddings and sort by distance.
    f. Add user input to the messages list.
    g. Keep the first message in messages_log.
    h. Generate the AI response.
    i. Check the AI response with the moderation API.
    j. Add the AI response to the messages list.
    k. Create and return the JSON response object.

9. Run the Flask app.
"""

# import libraries
import os
import pandas as pd
import openai
import numpy as np
from openai.embeddings_utils import distances_from_embeddings
from flask import Flask, request, jsonify, render_template

# set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
# set OpenAI model
model = "gpt-3.5-turbo"

# initialize Flask app
app = Flask(__name__)

# load embeddings data from csv
df=pd.read_csv('processed/embeddings.csv', index_col=0)
df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)
df.head()

# define standard phrases
exit_phrases = ["bye", "goodbye"]
greeting_phrases = ["hello", "hi", "hey", "greetings"]
introduction_message = "Hello! I'm TEL-chatGPT, a Digital Educational Technologist from the University of Hertfordshire's Technology Enhanced Learning (TEL) Team. I'm here to help you with Technology Enhanced Learning and general Teaching and Learning concepts. If you need assistance, feel free to ask!"

# set maximum number of messages to keep in messages_log
MAX_MESSAGES = 10

# initialize chat with system greeting and user input
messages_log = [
    {"role": "system", "content": "You are a helpful and professional AI called TEL-chatGPT. Your job is to help users at the University of Hertfordshire with Technology Enhanced Learning and general Teaching and Learning concepts. The user will pass context to you but they are not aware of this, you should use the context from the embeddings to make sure your response is relevant to UoH. If you do not know the answer to a query, you should state that you do not know that answer and the user should contact TELSupport@herts.ac.uk. If a user asks for information that is not related to educational technology or teaching and learning at the university of hertfordshire, you should decline to answer and suggest they ask a general AI like ChatGPT."},
]

# define route for home page
@app.route('/')
def home():
    return render_template('index.html')

# define route for handling user input and returning AI response as JSON object
@app.route("/chat", methods=["POST"])
def chat():
    
    # set global messages_log variable
    global messages_log
    global exit_phrases
    global greeting_phrases
    global help_phrases
    global MAX_MESSAGES
    
    # get user input from request data
    user_input = request.json["input"]

    # check if user input contains any exit phrases
    if any(phrase in user_input.lower() for phrase in exit_phrases):
        # add AI response to messages list
        response = "Goodbye! Thank you for chatting with me."
        messages_log.append({"role": "assistant", "content": response})
        
        # create JSON response object
        response = {"messages": messages_log}
        
        # return JSON response object
        return jsonify(response)

    # check if user input contains any greeting phrases
    if any(phrase in user_input.lower() for phrase in greeting_phrases):
        response = {"role": "assistant", "content": introduction_message}
        messages_log.append(response)
        response = {"messages": messages_log}
        return jsonify(response)

    # Get the embeddings for the question
    q_embeddings = openai.Embedding.create(input=user_input, engine='text-embedding-ada-002')['data'][0]['embedding']

    # Get the distances from the embeddings
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')

    # Sort the DataFrame by distance
    sorted_df = df.sort_values('distances', ascending=True)

    # Initialize the context and word count
    context = ""
    word_count = 0
    desired_word_count = 600

    # Initialize counter
    counter = 0
    max_embeddings = 10

    # Iterate through the sorted DataFrame
    for _, row in sorted_df.iterrows():
        # Increment the counter
        counter += 1

        # Split the response into words
        words = row["text"].split()

        # Calculate the new word count after adding the response
        new_word_count = word_count + len(words)

        # If the counter is less than or equal to max_embeddings and the new word count is less than the desired word count, add the response to the context
        if counter <= max_embeddings and new_word_count <= desired_word_count:
            if context != "":
                context += "\n\n###\n\n"
            context += row["text"]
            word_count = new_word_count
        # If the counter is less than or equal to max_embeddings and the new word count is greater than the desired word count but doesn't exceed it by too much, add the response to the context and break the loop
        elif counter <= max_embeddings and abs(new_word_count - desired_word_count) <= 20:
            if context != "":
                context += "\n\n###\n\n"
            context += row["text"]
            break
        # If the counter is greater than max_embeddings or the new word count exceeds the desired word count by too much, break the loop
        else:
            break

    # add user input to messages_log
    if context:
        messages_log.append({"role": "user", "content": user_input + ". Context from Embeddings: {}".format(context)})
    else:
        messages_log.append({"role": "user", "content": user_input})

    
    # keep the first message in messages_log
    messages_log = messages_log[:1] + messages_log[-(MAX_MESSAGES-1):]
    
   
    # generate AI response
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages_log,
        )

    # check AI response with moderation API
    response = openai.Moderation.create(completion.choices[0].message['content'])
    # check if response is flagged
    if response["results"][0]["flagged"]:
        # if flagged, return error message
        response = {"role": "assistant", "content": "I am afraid this answer may be inappropriate, please rephrase your question or ask in a different way."}
        return jsonify(response)

    # add AI response to messages list
    response = completion.choices[0].message['content']
    messages_log.append({"role": "assistant", "content": response})

    # create JSON response object
    response = {"messages": messages_log}

    #print the messages_log
    print (messages_log)
    
    # return JSON response object
    return jsonify(response)
  
#Check if the script is being run directly (not imported as a module)
if __name__ == '__main__': 
    # If the script is run directly, start the Flask app
    app.run()
    

