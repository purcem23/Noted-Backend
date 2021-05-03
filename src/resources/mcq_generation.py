import pprint
import itertools
import re
import pke
import string
from nltk.corpus import stopwords
from summarizer import Summarizer
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
import requests
import json
import re
import random
from pywsd.similarity import max_similarity
from pywsd.lesk import adapted_lesk
from pywsd.lesk import simple_lesk
from pywsd.lesk import cosine_lesk
from nltk.corpus import wordnet as wn
from ..config import app
from flask_apiexceptions import (
    JSONExceptionHandler,
    ApiException,
    ApiError,
    api_exception_handler,
)
from nltk.tokenize import sent_tokenize

exception_handler = JSONExceptionHandler()
exception_handler.init_app(app)
exception_handler.register(
    code_or_exception=ApiException, handler=api_exception_handler
)


# call first
# Bert-extractive-summarizer
def init_mcq(contents):
    # f = open("cardiac.txt", "r")
    full_text = contents
    model = Summarizer()
    result = model(full_text, min_length=60, max_length=500, ratio=0.4)
    summarized_text = "".join(result)
    return summarized_text


# print(summarized_text)


# uses PKE library
# take keywords out of main, take keywords out of summarized
# only keep keywords in both
# take 20 keywords n=20
def get_nouns_multipartite(text):
    out = []
    extractor = pke.unsupervised.MultipartiteRank()
    extractor.load_document(input=text)
    #    not contain punctuation marks or stopwords as candidates.
    # pos makes sure keywords are pronouns
    pos = {"PROPN"}
    stoplist = list(string.punctuation)
    # stoplist removes stopwords and formatting
    stoplist += ["-lrb-", "-rrb-", "-lcb-", "-rcb-", "-lsb-", "-rsb-"]
    stoplist += stopwords.words("english")
    extractor.candidate_selection(pos=pos, stoplist=stoplist)
    # 4. build the Multipartite graph and rank candidates using random walk,
    #    alpha controls the weight adjustment mechanism, see TopicRank for
    #    threshold/method parameters.
    extractor.candidate_weighting(alpha=1.1, threshold=0.75, method="average")
    keyphrases = extractor.get_n_best(n=15)
    for key in keyphrases:
        out.append(key[0])
    if not out:
        pos = {"NOUN"}
        extractor.candidate_selection(pos=pos, stoplist=stoplist)
        extractor.candidate_weighting(
            alpha=1.1, threshold=0.75, method="average"
        )
        keyphrases = extractor.get_n_best(n=15)
        for key in keyphrases:
            out.append(key[0])
        return out
    else:
        # import pdb; pdb.set_trace()
        return out


# call this second
def keyword_prep(full_text, summarized_text):
    # prints keywords/filtered keywords
    keywords = get_nouns_multipartite(full_text)
    # print(keywords)
    filtered_keys = []
    for keyword in keywords:
        if keyword.lower() in summarized_text.lower():
            filtered_keys.append(keyword)
    return filtered_keys


# print(filtered_keys)


# get sentences of under 20 that keywords were taken from
def tokenize_sentences(text):
    sentences = [sent_tokenize(text)]
    sentences = [y for x in sentences for y in x]
    # Remove any short sentences less than 20 letters.
    sentences = [
        sentence.strip() for sentence in sentences if len(sentence) > 20
    ]
    return sentences


# link sentences to represented keywords that were filtered
def get_sentences_for_keyword(keywords, sentences):
    keyword_processor = KeywordProcessor()
    keyword_sentences = {}
    for word in keywords:
        keyword_sentences[word] = []
        keyword_processor.add_keyword(word)
    for sentence in sentences:
        keywords_found = keyword_processor.extract_keywords(sentence)
        for key in keywords_found:
            keyword_sentences[key].append(sentence)

    for key in keyword_sentences.keys():
        values = keyword_sentences[key]
        values = sorted(values, key=len, reverse=True)
        keyword_sentences[key] = values
        return keyword_sentences


# call third
def keyword_to_sentence(summarized_text, filtered_keys):
    sentences = tokenize_sentences(summarized_text)
    keyword_sentence_mapping = get_sentences_for_keyword(
        filtered_keys, sentences
    )
    return keyword_sentence_mapping


# print(keyword_sentence_mapping)


# Decoys from Wordnet and Conceptnet
# Decoys are wrong answers to generate the other possibilities
# after context is gotten, find hypernyms of word, then find
# all hyponyms of said word
def get_decoys_wordnet(syn, word):
    decoys = []
    word = word.lower()
    orig_word = word
    # Replace keyword with underscores
    if len(word.split()) > 0:
        word = word.replace(" ", "_")
    hypernym = syn.hypernyms()
    if len(hypernym) == 0:
        return decoys
    for item in hypernym[0].hyponyms():
        name = item.lemmas()[0].name()
        if name == orig_word:
            continue
        name = name.replace("_", " ")
        name = " ".join(w.capitalize() for w in name.split())
        if name is not None and name not in decoys:
            decoys.append(name)
    return decoys


# get_word sense gets the key word and weights it against the sentence
# this allows context to be found (word sense disambiguation)
def get_wordsense(sent, word):
    word = word.lower()

    if len(word.split()) > 0:
        word = word.replace(" ", "_")

    synsets = wn.synsets(word, "n")
    if synsets:
        wup = max_similarity(sent, word, "wup", pos="n")
        adapted_lesk_output = adapted_lesk(sent, word, pos="n")
        lowest_index = min(
            synsets.index(wup), synsets.index(adapted_lesk_output)
        )
        return synsets[lowest_index]
    else:
        return None


# conceptnet uses the Partof relationship, finding what a keyword
# is part of and then seeing what partof relationship
# that word also holds
# Decoys from http://conceptnet.io/
def get_decoys_conceptnet(word):
    word = word.lower()
    original_word = word
    if len(word.split()) > 0:
        word = word.replace(" ", "_")
    decoys_list = []
    url = (
        "http://api.conceptnet.io/query?node=/c/en/%s/n&rel=/r/PartOf&start=/c/en/%s&limit=5"
        % (word, word)
    )
    obj = requests.get(url).json()

    for edge in obj["edges"]:
        link = edge["end"]["term"]

        url2 = (
            "http://api.conceptnet.io/query?node=%s&rel=/r/PartOf&end=%s&limit=10"
            % (link, link)
        )
        obj2 = requests.get(url2).json()
        for edge in obj2["edges"]:
            word2 = edge["start"]["label"]
            if (
                word2 not in decoys_list
                and original_word.lower() not in word2.lower()
            ):
                decoys_list.append(word2)

    return decoys_list


def generate_mcq(keyword_sentence_mapping):
    key_decoys_list = {}
    for keyword in keyword_sentence_mapping:
        wordsense = get_wordsense(
            keyword_sentence_mapping[keyword][0], keyword
        )
        if wordsense:
            decoys = get_decoys_wordnet(wordsense, keyword)
            if len(decoys) == 0:
                decoys = get_decoys_conceptnet(keyword)
            if len(decoys) != 0:
                key_decoys_list[keyword] = decoys
        else:

            decoys = get_decoys_conceptnet(keyword)
            if len(decoys) != 0:
                key_decoys_list[keyword] = decoys

    questions = []
    for each in key_decoys_list:
        sentence = keyword_sentence_mapping[each][0]
        pattern = re.compile(each, re.IGNORECASE)
        output = pattern.sub(" _______ ", sentence)
        answer = each.capitalize()
        fake_answers = key_decoys_list[each]
        if answer in fake_answers:
            fake_answers.remove(answer)
        top4possibilities = [answer] + fake_answers[:3]
        random.shuffle(top4possibilities)
        questions.append(
            {
                "question": output,
                "fake_answers": top4possibilities,
                "answer": answer,
            }
        )

    return questions


# generate_mcq()
