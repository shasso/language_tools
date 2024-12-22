#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install polyglot')
get_ipython().system('pip install pyicu')
get_ipython().system('pip install pycld2')
get_ipython().system('pip install pycld3')


# In[ ]:


get_ipython().system('pip install polyglot')


# In[ ]:


get_ipython().system('pip install pyicu')


# In[ ]:


get_ipython().system('pip install pycld2')


# In[2]:


from polyglot.detect import Detector

# Path to the input text file
input_file_path = "./data/06-Waw.txt"  # Update with your file path

# Function to detect language for each word in a line
def detect_languages_per_word(line, line_number):
    words = line.strip().split()
    word_languages = {}

    start_location = 0

    for word in words:
        detector = Detector(word, quiet=True) # Set quiet to suppress messages
        lang_code = detector.language.code

        # Print word, language, line number, and start location
        # print(f"Word: '{word}', Language: '{lang_code}', Line: {line_number}, Start Location: {start_location}")
        print(f"{line_number}:{start_location}:{len(word)} Word: '{word}', Language: '{lang_code}'")
        
        # Update start location for the next word
        start_location += len(word) + 1  # Adding 1 for the space

# Read the input text file line by line
with open(input_file_path, "r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        detect_languages_per_word(line, line_number)


# In[ ]:




