import random as rd
import math
import csv

c=2.5
with open('dataFile.csv','wb') as new_csv:
    for i in range(400):
        t=rd.randint(20,993)
        if(t<50):
            a=2.4
            b=1.05
            d=0.38
        elif(t<300):
            a=3.0
            b=1.12
            d=0.35
        else:
            a=3.6
            b=1.20
            d=0.32
        q=abs(round(a*math.pow(float(t)/1000,b)+rd.randint(-rd.randint(0,100),rd.randint(0,100))*0.01,2))
        w=abs(round(c*math.pow(float(t)/1000,d)+rd.randint(-rd.randint(0,100),rd.randint(0,100))*0.01,2))
        csv_writer=csv.writer(new_csv)
        csv_writer.writerow([t,q,w])
print("File Created Successfully!")


