import csv 
import math
import time
import matplotlib.pyplot as plt


#function to retrive the parameters from the D list which contains (500*300) results of every possible combination
def get_param(D):
    d=[]
    for i in D:
        d.append(i[0]) #store the difference in d

    m=min(d) #find min difference
    for i in D:
        #get param where diff is minimum
        if(i[0]==m):
            a=i[1]
            b=i[2]
            break
    return (a,b) #return parameters


#function to fit regression line to find optimal effort
def fit_effort(L):
    D=[]
    
    for a in range(0,500): #iterate 'a' param in step of 0.01 for 500 times
        a=a*0.01
        for b in range(0,300): #iterate 'b' param in step of 0.01 for 300 times
            b=b*0.01
            diff=0
            for i in L:
                ht=a*math.pow(int(i[0]),b) #calculate the effort from hypothesis E=a*(kloc^b)
                diff+=(ht-float(i[1]))**2 #calculate the squared difference between real effort and hypothesised effort 
            diff=diff/2*len(L) #find half mean
            D.append((diff,a,b)) #store the difference along with each parameter
    return D


#function to fit regression line to find optimal development time
def fit_tdev(L):
    D=[]
    for a in range(0,500): #iterate 'a' param in step of 0.01 for 500 times
        a=a*0.01
        for b in range(0,300): #iterate 'b' param in step of 0.01 for 300 times
            b=b*0.01
            diff=0
            for i in L:
                ht=a*math.pow(float(i[1]),b) #calculate the effort from hypothesis E=a*(effort^b)
                diff+=(ht-float(i[2]))**2 #calculate the squared difference between real effort and hypothesised effort
            diff=diff/2*len(L) #find half mean    
            D.append((diff,a,b)) #store the difference along with each parameter
    return D



time1=time.time() #start time

org=[]
sd=[]
emb=[]


print("Reading Data...")


#read data from a file which would be used for regression
with open("dataFile.csv",'rb') as csvFile:
    read=csv.reader(csvFile)
    for row in read:
        if(int(row[0])<50):
            org.append(row) #insert data row to org list which are organic(lines<50)
        elif(int(row[0])<300):
            sd.append(row) #insert data row to sd list which are semiDetached(50<lines<300)
        else:
            emb.append(row) #insert data row to emb list which are embedded(lines>300)

##print(org)
##print(sd)
##print(emb)
time.sleep(2) #sleep to make system stable
print("Data Reading Done!")
T=[org,sd,emb]

org_x=[]
org_y=[]
org_z=[]

for i in org:
    org_x.append(i[0]) #fetch no. of lines from organic list and store in org_x
    org_y.append(i[1]) #fetch effort from organic list and store in org_y
    org_z.append(i[2]) #fetch development time from organic list and store in org_z
    
sd_x=[]
sd_y=[]
sd_z=[]

for i in sd:
    sd_x.append(i[0]) #fetch no. of lines from semiDetached list and store in sd_x
    sd_y.append(i[1]) #fetch effort from semiDetached list and store in sd_y
    sd_z.append(i[2]) #fetch development time from semiDetached list and store in sd_z
    
emb_x=[]
emb_y=[]
emb_z=[]

for i in emb:
    emb_x.append(i[0]) #fetch no. of lines from embedded list and store in emb_x
    emb_y.append(i[1]) #fetch effort from embedded list and store in emb_y
    emb_z.append(i[2]) #fetch development time from embedded list and store in emb_z


T2=[]
time.sleep(1)
print("Fitting the curve and Retrieving parameters...")

for i in range(len(T)):
    eff=fit_effort(T[i]) #Do regression of each list=[org,sd,emb] to get effort
    param=get_param(eff) #Get the optimum parameters for each list
    tdev=fit_tdev(T[i]) #Do regression of each list=[org,sd,emb] to get time of dev
    param2=get_param(tdev) #Get the optimum parameters for each list
    T2.append(param+param2) #Fetch all parameters in a list

print("Parameters retrieved!")

org_fit_eff=[]
for i in sorted(org_x):
    h=T2[0][0]*(float(i)**T2[0][1]) #finding effort of each value in org_x
    org_fit_eff.append(h) #storing the value calculated

sd_fit_eff=[]
for i in sorted(sd_x):
    h=T2[1][0]*(float(i)**T2[1][1]) #finding effort of each value in sd_x
    sd_fit_eff.append(h) #storing the value calculated

emb_fit_eff=[]
for i in sorted(emb_x):
    h=T2[2][0]*(float(i)**T2[2][1]) #finding effort of each value in emb_x
    emb_fit_eff.append(h) #storing the value calculated


#plotting the graph of number of lines vs effort in the dataFile
plt.plot(org_x,org_y,'o')
#plotting the regression line
plt.plot(sorted(org_x),org_fit_eff,'--')
plt.title('Organic Class')
plt.xlabel('Lines of code')
plt.ylabel('Effort(Person-Months)')
plt.show()

#plotting the graph of number of lines vs effort in the dataFile
plt.plot(sd_x,sd_y,'o')
#plotting the regression line
plt.plot(sorted(sd_x),sd_fit_eff,'--')
plt.title('Semi-Detached Class')
plt.xlabel('Lines of code')
plt.ylabel('Effort(Person-Months)')
plt.show()

#plotting the graph of number of lines vs effort present in the dataFile
plt.plot(emb_x,emb_y,'o')
#plotting the regression line
plt.plot(sorted(emb_x),emb_fit_eff,'--')
plt.title('Embedded Class')
plt.xlabel('Lines of code')
plt.ylabel('Effort(Person-Months)')
plt.show()


org_fit_tdev=[]
for i in sorted(org_x):
    h=T2[0][2]*(T2[0][0]*(float(i)**T2[0][1]))**T2[0][3] #finding tdev of each value in org_x
    org_fit_tdev.append(h) #storing the value calculated

sd_fit_tdev=[]
for i in sorted(sd_x):
    h=T2[1][2]*(T2[1][0]*(float(i)**T2[1][1]))**T2[1][3] #finding tdev of each value in sd_x
    sd_fit_tdev.append(h) #storing the value calculated

emb_fit_tdev=[]
for i in sorted(emb_x):
    h=T2[2][2]*(T2[2][0]*(float(i)**T2[2][1]))**T2[2][3] #finding tdev of each value in emb_x
    emb_fit_tdev.append(h) #storing the value calculated


#plotting the graph of number of lines vs effort present in the dataFile
plt.plot(org_x,org_z,'o')
#plotting the regression line
plt.plot(sorted(org_x),org_fit_tdev,'--')
plt.title('Organic Class')
plt.xlabel('Lines of code')
plt.ylabel('Development Time(Months)')
plt.show()


#plotting the graph of number of lines vs effort present in the dataFile
plt.plot(sd_x,sd_z,'o')
#plotting the regression line
plt.plot(sorted(sd_x),sd_fit_tdev,'--')
plt.title('Semi-Detached Class')
plt.xlabel('Lines of code')
plt.ylabel('Development Time(Months)')
plt.show()


#plotting the graph of number of lines vs effort present in the dataFile
plt.plot(emb_x,emb_z,'o')
#plotting the regression line
plt.plot(sorted(emb_x),emb_fit_tdev,'--')
plt.title('Embedded Class')
plt.xlabel('Lines of code')
plt.ylabel('Development Time(Months)')
plt.show()


##print(T2)


#creating a dictionary to access variables retrieved during regression with key
const={'Organic':{'a': T2[0][0] ,'b': T2[0][1],'c':T2[0][2],'d':T2[0][3]},'Semidetached':{'a': T2[1][0] ,'b': T2[1][1],'c':T2[1][2],'d':T2[1][3]},'Embedded':{'a': T2[2][0] ,'b': T2[2][1],'c':T2[2][2],'d':T2[2][3]}}


def basic():
	with open(file) as f: #open file
		line_count=0;
		#calculating number of lines in input file
		for line in f:
			line_count+=1
		print "Number of lines:",line_count
                
		if line_count <50:
			mode="Organic"
		elif line_count <300:
			mode="Semidetached"
		else:
			mode="Embedded"

                #fetching variables from the dictionary created
		a_val=const[mode]['a']
		b_val=const[mode]['b']
		c_val=const[mode]['c']
		d_val=const[mode]['d']
        
		line_count=float(line_count)/1000
		
                #calculating effort,development time,staff and productivity
		effort=a_val*math.pow(line_count,b_val)
		print "Effort is",effort,"person months"
		develop=c_val*math.pow(effort,d_val)

		print "Development time is",develop,"months"

		ss=effort/develop
		print "Staff Size is",ss,"person(s)"
		p=line_count/effort
		print "Productivity",p,"Kloc per person months"


#prompt user to enter file name repeatedly
while(True):
    print("Enter File Name:")
    file=str(raw_input()) #anyfile of code
    basic() #calling basic function
    print("Test for another file(Y/n):")
    z=str(raw_input())
    if(z=='y' or z=='Y'):
        continue
    else:
        break
		
time2=time.time() #end time

#calculating total processing time
print "\nProcessing Time: "+str(int((time2-time1)/60))+" minutes "+str(int((time2-time1)%60))+" seconds"


