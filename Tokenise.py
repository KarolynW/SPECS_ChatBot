"""
This code reads a CSV file containing processed text, tokenizes the text using OpenAI's tiktoken library,
and creates chunks of text limited to a maximum number of tokens. It then calculates embeddings for
each chunk using OpenAI's Embedding API and saves the results to another CSV file.

Step-by-step explanation of the code:

1. Import necessary libraries: tiktoken, openai, pandas, matplotlib, bs4 (BeautifulSoup), and embeddings_utils from openai.
2. Load the cl100k_base tokenizer which is designed to work with the ada-002 model.
3. Read the processed.csv file into a pandas DataFrame and set the column names to 'title' and 'text'.
4. Tokenize the text in the DataFrame and add a new column 'n_tokens' containing the number of tokens for each row.
5. Plot a histogram to visualize the distribution of the number of tokens per row.
6. Set the maximum number of tokens to 500.
7. Define a function split_into_many that splits the text into chunks with a maximum number of tokens.
8. Create an empty list shortened to store the shortened texts.
9. Iterate through the DataFrame, and for each row:
   a. If the text is None, skip to the next row.
   b. If the number of tokens is greater than the max number of tokens, split the text into chunks and add them to the shortened list.
   c. If the number of tokens is less than or equal to the max number of tokens, add the text to the shortened list.
10. Create a new DataFrame with the shortened texts and calculate the number of tokens for each row.
11. Plot a histogram to visualize the distribution of the number of tokens per row in the new DataFrame.
12. Calculate embeddings for each text in the DataFrame using OpenAI's Embedding API and store them in a new column 'embeddings'.
13. Save the DataFrame to a CSV file named 'processed/embeddings.csv'.
14. Print the first five rows of the DataFrame.
"""


import tiktoken
import openai
import pandas as pd
import matplotlib.pyplot as plt

# Load the cl100k_base tokenizer which is designed to work with the ada-002 model
tokenizer = tiktoken.get_encoding("cl100k_base")

# Read the processed.csv file into a pandas DataFrame and set the column names to 'title' and 'text'
df = pd.read_csv('processed/processed.csv', header=0)
df.columns = ['title','text']

# Tokenize the text and save the number of tokens to a new column
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

# Visualize the distribution of the number of tokens per row using a histogram
df.n_tokens.hist()
plt.show()

# Set the maximum number of tokens to 500
max_tokens = 500

# Define a function that splits the text into chunks with a maximum number of tokens
def split_into_many(text, max_tokens=max_tokens):
    tokens = tokenizer.encode(text)
    chunks = []

    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)

    return chunks
   
# Create an empty list to store the shortened texts
shortened = []

# Loop through the dataframe
for row in df.iterrows():

    # If the text is None, go to the next row
    if row[1]['text'] is None:
        continue

    # If the number of tokens is greater than the max number of tokens, split the text into chunks
    if row[1]['n_tokens'] > max_tokens:
        shortened += split_into_many(row[1]['text'])
    
    # Otherwise, add the text to the list of shortened texts
    else:
        shortened.append( row[1]['text'] )

# Create a new DataFrame with the shortened texts and calculate the number of tokens for each row
df = pd.DataFrame(shortened, columns = ['text'])
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
# Visualize the distribution of the number of tokens per row using a histogram
df.n_tokens.hist()
plt.show()

# Calculate embeddings for each text in the DataFrame using OpenAI's Embedding API and store them in a new column 'embeddings'
df['embeddings'] = df.text.apply(lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])
df.to_csv('processed/embeddings.csv')
df.head()
