""" Rouge Score """

# from rouge_score import rouge_scorer

# cv_skills = 'ml cv react angular unity vue' # tuple and list are not supported
# jd_skills = 'ml cv vue react'

# scorer = rouge_scorer.RougeScorer(['rouge1'])
# scores = scorer.score(cv_skills, jd_skills)

# print(scores["rouge1"][1])



"""" Flair NER """

# from flair.data import Sentence
# from flair.models import SequenceTagger

# # load tagger
# tagger = SequenceTagger.load("flair/ner-english")

# # make example sentence
# sentence = Sentence("George Washington went to Washington This is $500 Richard lives in USA. Spain is a country. Facebook is a company")

# # predict NER tags
# tagger.predict(sentence)

# # print sentence
# print(sentence)

# # print predicted NER spans
# print('The following NER tags are found:')
# # iterate over entities and print
# for entity in sentence.get_spans('ner'):
#     print(entity)



""" Zero-shot Classification """

# from transformers import pipeline
# classifier_pipeline = pipeline ("zero-shot-classification", model = "facebook/bart-large-mnli")

# input_sequence = "I love travelling places and listen to latest technology news."
# label_candidate = ['travel', 'cooking', 'entertainment', 'dancing', 'technology']
# out = classifier_pipeline(input_sequence, label_candidate, multi_label=True)
# print(out)


""" Phrase Matcher """
# import spacy
# from spacy.matcher import PhraseMatcher
# nlp = spacy.load("en_core_web_md")
# matcher = PhraseMatcher(nlp.vocab)

# #create the list of words to match
# lang_list = ['Python','C++','Java']

# #obtain doc object for each word in the list and store it in a list
# patterns = [nlp(lang) for lang in lang_list]
# #add the pattern to the matcher
# matcher.add("PROGRAMMING_LANGUAGE", patterns)
# #process some text
# doc = nlp("Python requires less typing, provides new libraries, fast prototyping, and several other new features. C++ as of today in its efficiency, speed, and memory make it widely popular among coders. Java is platform-independent")
# matches = matcher(doc)
# for match_id, start, end in matches:
#  span = doc[start:end]
#  print(span.text)
# 
 
 
""" Regex Matcher """

# import spacy
# import re

# nlp = spacy.load("en_core_web_md")
# doc = nlp("The United States of America (USA) are commonly known as the United States (U.S. or US) or America.")

# expression = r"U[.]?S[.]?"
# for match in re.finditer(expression, doc.text):
#     start, end = match.span()
#     span = doc.char_span(start, end)
#     if span is not None:
#         print("Found match:", span.text)


""" Google Translator """

# from googletrans import Translator
# from langdetect import detect

# translator = Translator()

# text1 = 'My name is Shiva.'
# language = detect(text1)
# print(language)

# translated_text = translator.translate('My name is shiva', dest='fr', src='en')
# print(translated_text.text)