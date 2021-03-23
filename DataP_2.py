import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import re


df = pd.read_csv('NBO_WithGroupingCategories_updated.csv')


def VisitsCategoriesColumns(df,Visits,Categories,VisitNumber=1):
    
    ColumnsNames = [i for i in df.columns]
    TotalVisits = []
    TotalNumberOfCategories = []
    TotalNumberOfVisits = []
    
    for i in range(0,len(ColumnsNames)):
        
        visit = re.findall(r'Visit|visit',ColumnsNames[i])
        cat = re.findall(r'Cat|cat',ColumnsNames[i])
        if len(visit) >0 and len(cat)>0:
            order = re.findall(r'\d',ColumnsNames[i])
            if len(order)==2:
                TotalVisits.append(ColumnsNames[i])
                TotalNumberOfCategories.append(int(order[1]))
                TotalNumberOfVisits.append(int(order[0]))    

    if len(TotalNumberOfVisits)<1:
        print("Wrong input data")
        return -1

    TotalNumberOfCategories = sorted(TotalNumberOfCategories)
    TotalNumberOfVisits = sorted(TotalNumberOfVisits)

    NumberOfCategories = TotalNumberOfCategories[-1]
    NumberOfVisits = TotalNumberOfVisits[-1]

    if Visits > NumberOfVisits:
        print("Number Of visits Required Exceed Number of visits in data")
        return -1
    
    if Categories > NumberOfCategories:
        print("Number Of Categories Required Exceed Number of Categories in data")
        return -1

    RequiredVisits = VisitNumber+Visits-1

    if RequiredVisits>NumberOfVisits:
        print("There are only "+str(NumberOfVisits)+" in the dataset")
        return -1
    
    try:
        FilteredVisits=[]
        print(NumberOfCategories)
        print(NumberOfVisits)     #Visits   
        for i in  range(0,NumberOfVisits):
            for j in range(0,Categories):       
                FilteredVisits.append(TotalVisits[j])
                
            TotalVisits=TotalVisits[NumberOfCategories:]

        Start = VisitNumber*Categories-Categories
        End = Visits*Categories +Start
        FilteredVisits = FilteredVisits[Start:End]
        MainVisits = FilteredVisits[::Categories]
        print(MainVisits)
        df = df[FilteredVisits]
        df = df.dropna(subset=MainVisits)
        df=df.reset_index()
        del df['index']
        df = df.fillna(0)
    except:
        print("Wrong input data")
        return -1
    
    return df,MainVisits


def swapping(df,category_number,visits,MainVisits):

    category_number=category_number
    visits=visits
    close=True
    drop=[]
    drop2=[]
    for i in range(0,df.shape[0]):

        if not close:
            drop.append(i-1)

        close=False
        for lables in range(df.shape[1]-category_number,df.shape[1]):
            
            if df.iloc[i][lables] ==0:
                drop.append(i)
                break

            switch = -category_number
            for j in range(0,(visits-1)*category_number):

                if (j)%category_number == 0:
                    
                    switch = switch+category_number

                if df.iloc[i][j] == df.iloc[i][lables]:

                    df.iloc[i][switch] = df.iloc[i][j]

                    close = True
                    break

            if close:
                df.iloc[i][df.shape[1]-category_number]=df.iloc[i][lables]
                break
    for i in drop:
        #print(df.iloc[i])
        if i%10==0:
            break
    df = df[MainVisits]
    #df = df[::category_number]

    df = df.drop(drop)
    
    return df




NumberOfVistis = 3
CategoryNumber = 5
StartFromVisit = 2

df,MainVisits = VisitsCategoriesColumns(df,NumberOfVistis,CategoryNumber,StartFromVisit)
df = swapping(df,CategoryNumber,NumberOfVistis,MainVisits)
print(df.head())
df.to_csv ('test5.csv', index = False, header=True)     
