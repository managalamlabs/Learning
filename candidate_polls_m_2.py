
# coding: utf-8

# In[ ]:


numberofcandidates=0

#read number of candidates
try: 
    numberofcandidates = int(raw_input("input number of candidates:"))
expect TypeError:
    print 'number of candiadates in int type'
    numberofcandidates = int(raw_input("input number of candidates:"))
    
##here the raw_input will return string which we need to convert to int,for exaple check the type of variable numberofcandidates
type(numberofcandidates)
candidatedict={}

clist=[]
#iterate until you print correct number of names
while(len(clist)!=int(numberofcandidates)):
    #read candidate names with comma separation
    namesofcandidates = raw_input("names of the candidates:")
    clist=namesofcandidates.split(',')
    if(len(clist)!=int(numberofcandidates)):
        print 'number candidates entered not matching with number of people registered,please enter again'
    else:
        break


#load the dictionary    
for i in range(0,int(numberofcandidates)):
    candidatedict[i+1]=clist[i]

print 'data loaded'

print 'eneter ids to get names if you want terminate type exit'
while(1==1):
    nameid=raw_input('getname of the candidate with id or type exit')
    if(nameid=='exit'):
        print 'exiting the application'
        break
    else:
        print candidatedict[int(nameid)]
                
    
    
    


# In[ ]:




# In[ ]:



