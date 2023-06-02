# from numpy.ma.core import mod
# Algorithmes
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

# load the model first
import pickle
Mymodel=pickle.load(open(r'Fake_NewsMLP.pkl','rb'))


# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')
tl=WordNetLemmatizer()

def CheckNews(xinput):
    # xinput="criticism ukraine language law justified right body kiev reuters ukraine neighbor right criticize new ukrainian law banning school teaching minority language beyond primary school level leading european right watchdog said friday ukraine sizeable russian hungarian romanian minority passed school language legislation sept angering hungary particular threatened retaliate blocking kiev hope eu integration kiev submitted law review venice commission body rule right democracy dispute europe whose decision member state include ukraine commit respecting opinion adopted formally friday commission said legitimate ukraine address inequality helping citizen gain fluency state language ukrainian however strong domestic international criticism drawn especially provision reducing scope education minority language seems justified said statement said ambiguous wording part article legislation raised question shift ukrainian secondary education would implemented safeguarding right ethnic minority ukraine school taught russian romanian hungarian five polish according education ministry data commission said provision new law allow subject taught official eu language hungarian romanian polish appeared discriminate speaker russian widely used non state language le favorable treatment non eu language difficult justify therefore raise issue discrimination said language sensitive issue ukraine pro european maidan uprising decision scrap law allowing region use russian official second language fueled anti ukrainian unrest east escalated russia backed separatist insurgency latest education bill damaged ukraine tie western neighbor however october hungarian foreign minister peter szijjarto said issue driven relation lowest since ukraine independence following soviet union break ukraine said willing discus minority concern bear commission opinion recommendation mind fine tuning law statement released commission still session education ministry said watchdog position balanced constructive together national community ministry work developing various approach education minority taking account educational need statement said main goal provide sufficient level fluency state native language"
    # first create a corpus for it
    line=xinput.lower()
    line=line.split()
    line=[tl.lemmatize(word) for word in line if word not in stopwords.words('english')]
    line=" ".join(line)
    print(line)
    # load the vector model for the prediction purpose
    tfidf=pickle.load(open(r'vectorFit.pkl','rb'))
    xip=tfidf.transform([line]).toarray()
    x=xip[0].reshape(1,-1)
    print(x.shape)
    res=Mymodel.predict([x[0]])
    print(res)

    # print the result if 0=> real news or genuine news and 1=> the news is fake
    if res[0]==0:
        # print("the news is genuine or real")
        return "Genuine/Real News"
    else:
        # print("the news is fake")
        return "Fake news"




# def CheckInsurance(iplst):
#     modelI=pickle.load(open(r'C:\Security_And_fraud_detection_mini_proj\Insurance_policy_data\InsuranceFraudModel2.pkl','rb'))
#     iplstNp=np.array(iplst)

#     y_pred=modelI.predict(iplstNp)

#     if y_pred[0]==0:
#         return "This candidate is Eligible or Believe to get Insurance"
#     else:
#         return "This candidate is May be doing Fraud with you"
