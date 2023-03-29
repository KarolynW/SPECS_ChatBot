import openai
import os

# set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

########################################################################################################

""" #chatAPI demo
print("Welcome to the Chat API demo! Type your question below:")
print()
# Step 1: Get user input
user_input = input("You: ")
print()
print("Step 1: User question received:", user_input)
print()
# Step 2: Send the user input to the Chat API
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input},
    ],
    max_tokens = 100,
    )

print("Step 2: API call made with user question")
print()
# Step 3: Extract the assistant's response from the API response
assistant_response = response.choices[0].message['content']

print("Step 3: Assistant's response extracted")
print()
# Step 4: Display the assistant's response
print("Assistant:", assistant_response)
print()
print("Step 4: Assistant's response displayed") """


########################################################################################################


""" # Embedding API Demo

# Get user input
# This line prompts the user to enter their text and stores it in the 'user_input' variable
user_input = input("Enter your text string: ")

# Create the embeddings
# This part sends the user_input to the OpenAI API using the specified model, which generates embeddings for the input text
response = openai.Embedding.create(
    input=user_input,
    model="text-embedding-ada-002"
)

# Extract the embeddings
# This line extracts the embeddings from the API response and stores them in the 'embeddings' variable
embeddings = response['data'][0]['embedding']

# Print the embeddings
# This line prints the generated embeddings to the console
print("Embeddings:", embeddings)

 """
########################################################################################################

# Get user input
user_input = input("Enter your text string for moderation: ")

# Use the moderation API
response = openai.Moderation.create(
    input=user_input
)

# Extract the moderation output
output = response["results"][0]

# Print the moderation output
print("Moderation Output:", output)

########################################################################################################