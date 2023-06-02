import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('D:\Data\Desktop\MIniProj\SecurityPortal\static\chatmodule\chatbot_model.h5',compile=False)
import json
import random
# intents = json.loads(open('D:\Data\Downloads\Security_And_fraud_detection_mini_proj-20230506T172016Z-001\Security_And_fraud_detection_mini_proj\static\chatDataset1.json',encoding='utf8').read())
intents = json.loads(open('D:\Data\Desktop\MIniProj\SecurityPortal\static\chatDataset1.json',encoding='utf8').read())
# words = pickle.load(open('D:\Data\Downloads\Security_And_fraud_detection_mini_proj-20230506T172016Z-001\Security_And_fraud_detection_mini_proj\static\chatmodule\words.pkl','rb'))
words = pickle.load(open('D:\Data\Desktop\MIniProj\SecurityPortal\static\chatmodule\words.pkl','rb'))
# classes = pickle.load(open('D:\Data\Downloads\Security_And_fraud_detection_mini_proj-20230506T172016Z-001\Security_And_fraud_detection_mini_proj\static\chatmodule\classes.pkl','rb'))
classes = pickle.load(open('D:\Data\Desktop\MIniProj\SecurityPortal\static\chatmodule\classes.pkl','rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    print(ints)
    try:
      tagU = ints[0]['intent']
      print(tagU)
      list_of_intents = intents_json['intents']

      for i in list_of_intents:
        if(i['tag']== tagU):
            result = random.choice(i['responses'])
            break
    except:
      result="Sorry I don't know about it"
    return result

def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    return res


# if __name__=='__main__':
#     while True:
#         uip=input("Enter text=")
#         if uip=='exit':
#             break
#         cresp=chatbot_response(uip)
#         print("Chatbot Response: ",cresp)
#     print('By see you soon..... :)')