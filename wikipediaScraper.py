import requests
from bs4 import BeautifulSoup
import re
from heapq import nlargest

def remove_square_brackets(text):
    # Define a regular expression pattern to match square brackets and their contents
    pattern = r'\[[^\]]*\]'
    # Use re.sub() to replace all matches of the pattern with an empty string
    clean_text = re.sub(pattern, '', text)
    return clean_text

def get_wikipedia_summary(url, num_sentences=3):
    # Fetch the Wikipedia page
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the Wikipedia page.")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first paragraph in the main body of the article
    first_paragraph = ""
    for p in soup.find(id="mw-content-text").find_all("p"):
        if p.text.strip():
            first_paragraph = p.text.strip()
            break

    # Find all paragraphs in the main body of the article
    paragraphs = soup.find(id="mw-content-text").find_all("p")

    # Extract text from paragraphs and remove references and citation numbers
    text = ' '.join(p.text.strip() for p in paragraphs)
    text = re.sub(r'\[[0-9]+\]', '', text)

    # Tokenize the text into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    # Calculate the importance score for each sentence based on word frequency
    word_freq = {}
    for sentence in sentences:
        words = re.findall(r'\b\w+\b', sentence.lower())
        for word in words:
            if word not in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] += 1
    
    # Normalize scores by sentence length
    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] /= max_freq

    # Calculate sentence scores
    # used to determine the most important sentences 
    sentence_scores = {}
    for sentence in sentences:
        for word in re.findall(r'\b\w+\b', sentence.lower()):
            if word in word_freq:
                if len(sentence.split(' ')) < 30:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_freq[word]
                    else:
                        sentence_scores[sentence] += word_freq[word]

    # Select the top sentences based on score
    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)

    first_paragraph = remove_square_brackets(first_paragraph)
    summary = remove_square_brackets(summary)

    return first_paragraph + '\n\n' + summary


url = "https://en.wikipedia.org/wiki/Destiny_2"
summary = get_wikipedia_summary(url)
print(summary)
