import nltk
from nltk import pos_tag
# import nltkUtils as nkU
from nltk.tokenize import word_tokenize

data = [ [ "what is your name?" , "My name is sham. My name is harish. My name is kumar, kartik" ] ,
         [ "which food your would like to eat in the morning?" ,
           "I Like to eat Dosa. I like to eat Pohe. I like to eat Furits" ] ,
         [ "what is online security?" ,
           "online security is all about making your digital profile secure and avoid it to get hacked" ] ,
         [ "how should I make sure that my online security is maintained?" , "do follow the following procedures" ] ]
intents = [ ]
intent = {}
tags = [ ]


nltk.download('averaged_perceptron_tagger')
def get_pos_sent ( sent ) :
    # tokenize the sent
    word_token =word_tokenize ( sent )
    # print(word_token)

    # then find the pse tak for each token and store it
    token_tags = pos_tag ( word_token )

    return token_tags


# finding the main keyword or main tag from the Part of Speech (POS)
def get_NNtag ( tokenTag ) :
    tag = ""
    for w , t in tokenTag :
        if t == "NN" :  # Noun
            tag += w + " "
    return tag


def split_ans ( para ) :
    if '.' not in para :
        return [ para ]
    anslst = para.split ( '.' )
    return anslst


def UpdateQA ( tagE , ques , ans ) :
    # pass
    for i in intents :
        for t in i :
            # print(t,"->",i[t])
            if t == tagE :
                print ( tagE , "->" , t )
                i [ t ].append ( ques )
                anslst = split_ans ( ans )
                i [ t ].extend ( anslst )
                print ( "update done" )


if __name__ == "__main__" :

    # print(data[0][0])
    for i in data :
        intent = {}
        token_tags = get_pos_sent ( i [ 0 ] )
        tag = get_NNtag ( token_tags )  # getting the tag or keyword from (tokens,pos)
        # print(tag)
        # if tag not in intents.keys():
        print ( tag )
        if tag not in tags :
            tags.append ( tag )
            intent [ "tag" ] = tag
            intent [ "patterns" ] = [ i [ 0 ] ]
            ans_lst = split_ans ( i [ 1 ] )
            intent [ 'responses' ] = ans_lst
            intents.append ( intent )
        else :
            # UpdateQA ( tag , i [ 0 ] , i [ 1 ] )
            # print ( "UpdateQA is called..." )
            pass

    # print(intents)
    # now we got the intents store it in the json format
    json_data = {"intents" : intents}

    print ( json_data )

    # now convert all single quotes to double quotes
    json_data=str(json_data)
    newjsonData=''

    for i in json_data:
        if i=="'":
            newjsonData+='"'
        else:
            newjsonData+=i

    print(newjsonData)
    jsonfile=open("chatdS1.json",'w')
    jsonfile.write(newjsonData)

    jsonfile.close()

    print("file store successfully....")