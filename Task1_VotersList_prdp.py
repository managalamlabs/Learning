ip=int(input('enter no of candidates: '))
dict={}
for i in range (ip):
    name=input('enter candidate '+str(i+1)+' name : ')
    dict[i+1]=name

print('Candidates= ',dict)
find=int(input('Enter Candidate no below '+str(ip)+' to know the candidate : '))
while(find<=ip):
    print(dict[find])
    find = int(input('Enter another Candidate no less than ' + str(ip)+' to know else enter greater value : '))