
# coding: utf-8

# In[7]:

#int,string,char.....
rod_len=10
class Employee:
    
    'Common base class for all employees'
    empCount = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1
   
    def displayCount(self):
        print "Total Employee %d" % Employee.empCount
    
    def displayEmployee(self):
        print "Name :--->", self.name,  ", Salary:---->", self.salary
        
        
class Manager(Employee):
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1
        
manager1=Manager('abccm',40000)
manager1.displayEmployee()
    
    
    
e1=Employee('abc',200000)
e2=Employee('bbc',300000)

emp_dictionary={1:e1,2:e2,3:'myname'}

e1.displayEmployee()

for k in emp_dictionary:
    print type(emp_dictionary[k])
    if type(emp_dictionary[k])=='instance':
        print emp_dictionary[k].displayEmployee()
    else:
        print emp_dictionary[k]
        
#below are not working codes just given as examples
class article():
    surrogatekey
    timestamp_ist=123345
    url='mangalamlabs.com'
    keywords=(Universal Social Security scheme,Social Security,SECC,Labour Ministry,Caste censu')
    timestamp_utc=765444
              
def generatesurrogatekey():
    
    
#convert the timestamp UTC
    
   


# In[ ]:



