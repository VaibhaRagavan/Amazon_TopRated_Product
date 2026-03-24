#getting data
import pandas as pd , nltk,re,os
file_path=os.path.join(os.getcwd(),"amazon_dataset.csv")
data=pd.read_csv(file_path)
pd_name=data["product_name"]
catg=data["category"]
pd_details=data["about_product"]
pd_link=data["product_link"]
review=data["review_content"]
d_price=data["discounted_price"]
a_price=data["actual_price"]
rating_d=pd.to_numeric(data["rating"],errors='coerce')

data_col=[pd_name,catg,pd_details,review]
num_col=[d_price,a_price,rating_d,pd_link]

##data preprocessing
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
lemmatizer=WordNetLemmatizer()
stop_words=set(stopwords.words("english"))
stop_words.discard("not")

##processing data 
def txt_process(d):
    if isinstance(d,str):
        text=[d]
    else:
        text=d
    corpus=[]
    for items in text:
        sentence=re.sub("[^a-zA-Z]",' ',items)
        sentence=sentence.lower()
        words=nltk.word_tokenize(sentence)
        lem_word=[]
        for word in words:
            if word not in stop_words:
                lem_word.append(lemmatizer.lemmatize(word))
        corpus.append(lem_word)

    if isinstance(d,str):
       return corpus[0]
    else:
       return corpus

processed_data=[]
for i in range(len(data)):
    ##adding weights to features
    name_weight=3
    cat_weight=2
    detail_weight=1
    review_weight=1
    combined_text=" ".join([str(pd_name[i])]*name_weight+
                            [str(catg[i])]*cat_weight+
                            [str(pd_details[i])]*detail_weight+
                            [str(review[i])]*review_weight)
    processed_txt=txt_process(combined_text)
    processed_data.append(processed_txt)


##converting data to vector
from gensim.models import Word2Vec
import numpy as np
#word to vector
W2v=Word2Vec(processed_data,vector_size=100,window=5,seed=40,workers=1) #seed and workerto avoid random result everytime
    

#sentence to vector 
def avgWord2vec(sentence,model):
    vector=[]
    for word in  sentence:
        if word in model.wv:
                vector.append(model.wv[word])
    if len(vector)==0:
            return np.zeros(model.vector_size)
    return(np.mean(vector,axis=0))

product_vec=[]
for product in processed_data:
    avgW2v=avgWord2vec(product,W2v)
    product_vec.append(avgW2v)

##testing data
def test(n):
    test_process=txt_process(n)
    test_vec=avgWord2vec(test_process,W2v)
    return test_vec

##finding similar sentence
def result(k):
    from sklearn.metrics.pairwise import cosine_similarity

    recommendation=[]
    for i in product_vec:   
        sim=cosine_similarity([k],[i])
        recommendation.append(sim[0][0])
    ##conver rating to0-1 & nan-->0
    rating_weight=rating_d.fillna(0)
    rating_normalized=(rating_weight - rating_weight.min()) / (rating_weight.max() - rating_weight.min())
    ## weighted simillarity
    weighted_score=[0.7*sim +0.3*r for sim, r in zip(recommendation,rating_normalized)]
    ##getting top 10 products
    top_index=np.argsort(weighted_score)[-25:][::-1]
 
    result=[]  
    for id in top_index:
        rd_name=pd_name.iloc[id]
        rd_detail=pd_details.iloc[id]
        rd_dis_price=d_price.iloc[id]
        rd_act_price=a_price.iloc[id]
        rd_rating=rating_d.iloc[id]
        rd_link=pd_link.iloc[id]


        result.append({
        "Product": rd_name ,
        "Details": rd_detail,
        "Discount_Price": rd_dis_price,
        "Actual_price": rd_act_price,
        "Rating": rd_rating,
        "Link": rd_link
        })
    return result
   





