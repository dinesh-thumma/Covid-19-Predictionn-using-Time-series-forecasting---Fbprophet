#####################################
#                                   #
#    Prediction Model               #
#                                   # 
#####################################  

from cProfile import label
from cmath import e
import pickle
from tempfile import tempdir
import pandas as pd
from sklearn import linear_model
from dates import Dates
import matplotlib.pyplot as plt
from functools import reduce
import datetime as dt


class Model:

    __modelName = 'india_model'
    __categoryName = 'TT'

    def __init__(self, n, date, df, m) -> None:
        self.n = n
        self.date = date
        self.df = df
        self.m = m


    def predictions(self):
        dates = Dates(self.n, self.date)
        val = dates.futureDates()
        print(Model.__modelName)
        with open(Model.__modelName,'rb') as f:
            model = pickle.load(f)
        try:
            output = model.predict(val)
        except e:
            print(e)
        return output['yhat']

    def linearModel(self):
        dates = Dates(self.n, self.date)
        val = dates.futureDates()
        val = list(val['ds'])
        output=[]
        with open('linear_india','rb') as f:
            li_model = pickle.load(f)
            for i in range(self.n):
                try:
                    dte=dt.datetime.strptime(val[i], '%Y-%M-%d').toordinal()
                    out = li_model.predict([[dte]])
                    output.append(out)

                except:
                    print('hello')
        return output


    def data_extraction(self, df):

        dates = Dates(self.n, self.date)
        val = dates.futureDates()
        val['ds'] = val['ds'].astype('datetime64')
        print(Model.__categoryName)
        pivot = pd.pivot_table(df,values=Model.__categoryName,index='Date',columns='Status').sort_values(by='Date') #seperating of relevant features
        finalData = pd.DataFrame(pivot)
        finalData.reset_index(inplace=True)   
        

        #val and finalData df1 and df2
        results = pd.merge(val, 
                  finalData[['Date', 'Confirmed']],
                  left_on='ds',
                  right_on='Date',
                  how='left')

        return results


    def graph(self):
        preds = self.predictions()
        preds = pd.DataFrame(preds)
        lin=self.linearModel()
        extracts = self.data_extraction(self.df)
        
        plt.plot(extracts['ds'], preds['yhat'], label='predicted cases')
        plt.plot(extracts['ds'], lin, label='linear cases')
        plt.plot(extracts['ds'], extracts['Confirmed'], label='Actual cases')
        plt.ylabel('Cases')
        plt.xlabel('Dates')
        plt.legend(loc='upper left')
        plt.show()
    
    def switch(self):
        try:
            if self.m==1:
                Model.__modelName = 'india_model'
                Model.__categoryName = 'TT'
                self.graph()
            elif self.m==2:
                Model.__modelName = 'wb_model'
                Model.__categoryName = 'WB'
                self.graph()
        except e:
            print(e)

# below code is for Model Class
print('1 for predicting India Cases\n')
print('2 for predicting WestBengal Cases\n')
m = int(input())

n = int(input("Enter the numner of days to predict\n"))
date = input("Enter the Starting date in the given format YYYY-MM-DD\n")
df = pd.read_csv('state_wise_daily.csv',parse_dates=['Date','Date_YMD'])
model = Model(n, date, df, m)
model.switch()

