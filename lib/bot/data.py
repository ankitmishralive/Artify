import pandas as pd
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
import re

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')

def preprocess(text):
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = nltk.word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in stopwords.words('english')]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    stemmed_tokens = [stemmer.stem(token) for token in lemmatized_tokens]
    return ' '.join(stemmed_tokens)

def preprocess_with_stopwords(text):
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = nltk.word_tokenize(text.lower())
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    stemmed_tokens = [stemmer.stem(token) for token in lemmatized_tokens]
    return ' '.join(stemmed_tokens)

class QASystem:

    def __init__(self, filepath):
        self.df = pd.read_csv(filepath, escapechar='\\')
        self.questions_list = self.df['Question'].tolist()
        self.answers_list = self.df['Answer'].tolist()
        self.vectorizer = TfidfVectorizer(tokenizer=nltk.word_tokenize, token_pattern=None)
        self.X = self.vectorizer.fit_transform([preprocess_with_stopwords(q) for q in self.questions_list])

    def get_response(self, text):
            processed_input = preprocess(text)
            vectorized_input = self.vectorizer.transform([processed_input])

            # Oops! I accidentally unleashed the similarity beast 🐉
            similarities = cosine_similarity(vectorized_input, self.X)
            max_similarity = np.max(similarities)
            threshold = np.percentile(similarities, 75)

            # Woah! This is getting interesting, but let's not get too serious 😜
            if max_similarity > threshold:
                # High-five to similar questions! 🙌
                high_similarity_questions = [q for q, s in zip(self.questions_list, similarities[0]) if s > 0.6]
                # Finding answers for questions that are practically twins 👯
                target_answers = [self.answers_list[self.questions_list.index(q)] for q in high_similarity_questions]

                # Time to build the fortress of Z! 🏰
                Z = self.vectorizer.transform([preprocess_with_stopwords(q) for q in high_similarity_questions])
                vectorized_input_with_stopwords = self.vectorizer.transform([processed_input])

                # The final showdown of similarities! 🤼
                final_similarities = cosine_similarity(vectorized_input_with_stopwords, Z)
                closest = np.argmax(final_similarities)

                # Drumroll, please! 🥁
                return target_answers[closest]
            else:
                # Oopsie daisy! I got a bit lost in translation. 🙈 Can you help me find my way back?
                return "To know more call/whatsapp us on +918779693725 or email us at ankitmishra.letter@gmail.com."
            

