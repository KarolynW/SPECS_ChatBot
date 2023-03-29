"""
This code processes a collection of Microsoft Word documents (.docx format) by removing non-alphanumeric characters, converting text to lowercase, and removing stopwords. The code then creates a pandas DataFrame with the processed text and saves the DataFrame to a CSV file.

1. Import necessary libraries: os, docx2txt, pandas, re, and nltk.
2. Download the stopwords from the nltk library.
3. Create an empty list `texts` to store the processed text files.
4. Define `stop_words` as a set of English stopwords.
5. Iterate through all the files in the "doc_library/" directory.
   - For each .docx file:
     a. Read the text from the file using the `docx2txt.process()` function.
     b. Omit the '.docx' extension from the filename and replace '-', '_', and '#update' with spaces to create the document title.
     c. Remove non-alphanumeric characters from the text using a regular expression.
     d. Remove stopwords by splitting the text into words, converting each word to lowercase, and filtering out words that are in `stop_words`.
     e. Join the remaining words back together into a filtered text string.
     f. Append the tuple (title, filtered_text) to the `texts` list.
6. Create a pandas DataFrame `df` from the `texts` list, with columns 'title' and 'text'.
7. Concatenate the document title with the filtered text, separated by a period and a space, and store it in the 'text' column of the DataFrame.
8. Create a new directory named 'processed' if it doesn't already exist.
9. Save the DataFrame as a CSV file named 'processed/processed.csv', without an index column.
10. Print the first five rows of the DataFrame to the console.

The output of this script will be a CSV file containing the titles and processed text of the .docx files in the "doc_library/" directory.
"""

import docx2txt
import pandas as pd
import re
import os
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# Create a list to store the text files
texts=[]

# Define stop words
stop_words = set(stopwords.words('english'))

# Get all the .docx files in the doc_library directory
for file in os.listdir("doc_library/"):
    if file.endswith(".docx"):
        # Read the text from the .docx file
        text = docx2txt.process("doc_library/" + file)

        # Omit the '.docx' extension from the file name,
        # then replace -, _, and #update with spaces.
        title = file[:-5].replace('-',' ').replace('_', ' ').replace('#update','')

        # Remove non-alphanumeric characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

        # Remove stop words
        words = text.split()
        words = [word.lower() for word in words if word.lower() not in stop_words]
        filtered_text = ' '.join(words)

        texts.append((title, filtered_text))

# Create a dataframe from the list of texts
df = pd.DataFrame(texts, columns = ['title', 'text'])

# Set the text column to be the raw text with the newlines removed
df['text'] = df.title + ". " + df['text']

# Create the 'processed' directory if it doesn't already exist
if not os.path.exists('processed'):
    os.makedirs('processed')

# Write the processed text to a CSV file
df.to_csv('processed/processed.csv', index=False)

# Display the first 5 rows of the dataframe
print(df.head())




