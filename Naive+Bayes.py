
# coding: utf-8

# In[11]:


def probAttr(data,attr,val):
    Total=data.shape[0]
    from collections import Counter
    cnt=Counter(x for x in data[attr])
    return cnt[val],cnt[val]/Total


# In[12]:


def probAttrConcept(data,attr,val,concept,cVal,countConcept):
#     print(attr,val)
    count={}
    prob={}
    C = data[concept]
    A = data[attr]
    for a in range(len(data[attr])):
#         print(A[a],C[a])
        for v in val:
            if(A[a]==v and C[a]==cVal):
                if v not in count:
                    count[v]=1
                else:
                    count[v]=count[v]+1
    for a in count:
        prob[a] = count[a]/countConcept
    return prob


# In[13]:


def train(data,AttributeList,concept):
    Attr={}
    probability_list={}
    #Get attribute values
    for a in AttributeList:
        Attr[a] = list(set(data[a]))
    
    #print(Attr,AttributeList)   
    conceptVals = list(set(data[concept]))
    conceptProbs = {}
    countConcept={}
    AttrConcept = {}
    for cVal in conceptVals:
        countConcept[cVal],conceptProbs[cVal] = probAttr(data,concept,cVal)
    
    for val in Attr:
        probability_list[val]={}
        AttrConcept[val] = {}
        for v in Attr[val]:
            a,probability_list[val][v]=probAttr(data,val,v)
        for cVal in conceptVals:
            AttrConcept[val][cVal]=probAttrConcept(data,val,Attr[val],concept,cVal,countConcept[cVal])
        
    print("P(A) : ",conceptProbs,"\n")
    print("P(X/A) : ",AttrConcept,"\n")
    print("P(X) : ",probability_list,"\n")
    return conceptProbs,AttrConcept,probability_list


# In[14]:


def test(examples,AttributeList,conceptProbs,AttrConcept,probability_list,data,concept_list,Total):
    misclassification_count=0
    Total1 = len(examples)-1
    for ex in range(1,len(examples)):
        px={}
        for x in range(1,len(examples[ex])):
            for a in AttributeList:
                for c in concept_list:
                    if examples[ex][x] in AttrConcept[a][c]:  
                        if c not in px:
                            px[c] = 1*AttrConcept[a][c][examples[ex][x]]
                        else:
                            px[c] = px[c]*AttrConcept[a][c][examples[ex][x]]
        classification = max(px,key=px.get)
        if(classification!=examples[ex][-1]):
            misclassification_count+=1
    misclassification_rate=misclassification_count*100/Total1
    accuracy=100-misclassification_rate
    print("Misclassification Count={}".format(misclassification_count))
    print("Misclassification Rate={}%".format(misclassification_rate))
    print("Accuracy={}%".format(accuracy))


# In[15]:


def main():
    import pandas as pd
    from pandas import DataFrame 
    from collections import Counter
    data = DataFrame.from_csv('data_train.csv')
#     print("\n Given Play Tennis Data Set:\n\n", data)
    AttributeList=list(data)[:-1]
    num_of_attributes=len(AttributeList)
    concept=str(list(data)[-1])
    Total=data.shape[0]
    conceptProbs,AttrConcept,probability_list = train(data,AttributeList,concept)

    import csv
    with open('data_test.csv')  as csvFile:
        examples = [list(line) for line in csv.reader(csvFile)]
#     print(examples)
    concept_list =list(Counter(x for x in data[concept]))
    test(examples,AttributeList,conceptProbs,AttrConcept,probability_list,data,concept_list,Total)


# In[16]:


main()

