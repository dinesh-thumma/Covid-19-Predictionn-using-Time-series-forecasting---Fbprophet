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
from dates import Dates
import matplotlib.pyplot as plt
from functools import reduce


class Model:

    def __init__(self, n, date) -> None:
        self.n = n
        self.date = date


    def predictions(self):
        dates = Dates(self.n, self.date)
        val = dates.futureDates()
        with open('model_pickle','rb') as f:
            model = pickle.load(f)
        try:
            output = model.predict(val)
        except e:
            print(e)
        return output['yhat']

    def data_extraction(self, df):

        dates = Dates(self.n, self.date)
        val = dates.futureDates()
        val['ds'] = val['ds'].astype('datetime64')
        
        pivot = pd.pivot_table(df,values='WB',index='Date_YMD',columns='Status').sort_values(by='Date_YMD') #seperating of relevant features
        finalData = pd.DataFrame(pivot)
        finalData.reset_index(inplace=True)   

        #val and finalData df1 and df2
        results = pd.merge(val, 
                  finalData[['Date_YMD', 'Confirmed']],
                  left_on='ds',
                  right_on='Date_YMD',
                  how='left')

        return results


    def graph(self, df):


        preds = self.predictions()
        preds = pd.DataFrame(preds)
        
        extracts = self.data_extraction(df)
        
        plt.plot(extracts['ds'], preds['yhat'], label='predicted cases')
        plt.plot(extracts['ds'], extracts['Confirmed'], label='Actual cases')
        plt.ylabel('Cases')
        plt.xlabel('Dates')
        plt.legend(loc='upper right')
        plt.show()

# below code is for Model Class
n = int(input("Enter the numner of days to predict\n"))
date = input("Enter the Starting date in the given format YYYY-MM-DD\n")
df = pd.read_csv('state_wise_daily.csv',parse_dates=['Date','Date_YMD'])
model = Model(n, date)
model.graph(df)

