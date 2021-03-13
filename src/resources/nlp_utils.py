from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
from ..config import app
from flask_apiexceptions import (
    JSONExceptionHandler, ApiException, ApiError, api_exception_handler)

exception_handler = JSONExceptionHandler()
exception_handler.init_app(app)
exception_handler.register(code_or_exception=ApiException, handler=api_exception_handler)


def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:  # ignore if both are same sentences
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(contents, top_n=3):
    stop_words = stopwords.words('english')
    summarize_note = []
    note = contents.split(". ")
    sentences = []
    for sentence in note:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()
    # Generate similary martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    print("Indexes of top ranked_sentence order are ", ranked_sentence)

    if len(sentences) >= 10:
        top_n = len(sentences)/0.6

    if len(sentences) <= 4:
        error = ApiError(code='400', message='Note too short to summarise')
        raise ApiException(status_code=400, error=error)

    for i in range(top_n):
        summarize_note.append(" ".join(ranked_sentence[i][1]))

    # Step 5 -  output the summarize text
    return(". ".join(summarize_note))


