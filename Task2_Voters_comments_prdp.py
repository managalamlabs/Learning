
ip=int(input('enter no of candidates: ')) # No Candidates
dict={}
for i in range (ip):
    dict[i+1]=[]
    name=input('enter candidate '+str(i+1)+' name : ')      #  Passing Candidate Name
    dict[i+1].append(name)                                  #  Store a Candidate name in Dict with the key value as i
no=len(dict)
user=input('Enter  User name  : ')                          #  User name who is  entering comments on Candidate(s)
print('Candidates= ',dict)                                    # Showing List of Candidates along with their Key values in Dict format
candidate = int(input('\n'+'Enter Candidate no to Comment : '))  # Enter a Key value that u wanna going to enter comment on a candidate
while (candidate>0 and candidate<=ip):
    dict[candidate].append(user)
    print('Candidate Name   : ', dict[candidate][0])
    comm=input('Enter your Comment : ')
    dict[candidate].append(comm)
    print('Candidates= ',dict)
    candidate=int(input('\n'+'Enter Candidate no to Comment between 1 to '+str(no)+' to comment : '))
    # enter within range of key value to enter more comments on candidates, else give input as out of range to exit

# to Find the Comments of a candidate

print(' \nYou are out of the Candidate Names Input Loop \n' )
candidate = int(input('Enter Candidate no to see the Users and their comment(s) : '))
if (candidate>0 and candidate<=ip):
    if len(dict[candidate])>2:
        print('\n'+'Comments For the Candidate : '+ str(dict[candidate][0])+ ' are')
    else:
        print('There are no comments for the Candidate : '+ str(dict[candidate]))
    for i in range (2,len(dict[candidate]),2):
        print('User : '+str(dict[candidate][i-1]) + '\t'+';'+'\t'+' Comment : '+str(dict[candidate][i]))

