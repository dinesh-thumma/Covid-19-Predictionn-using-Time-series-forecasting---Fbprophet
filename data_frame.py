from ntpath import join
from operator import index
from matplotlib.pyplot import axis
import pandas as pd

from dates import Dates

class Frame:
    
    def __init__(self, n, date, df) -> None:
        self.n = n
        self.date = date
        self.df = df
    
    
    def numner(self):
        count=0
        li = []
        for i in range(self.n):
            count+=1
            li.append(count)
        return li

    def startGenerator(self):
        output = Dates(self.n, self.date)
        values = output.da()
        status = ['Confirmed','Recovered','Deceased']
        count = self.numner()
        columns = ['Date', 'Date_YMD', 'Status']        
        dd1 = pd.DataFrame(columns=columns)
        for i in range(len(self.numner())):
            for j in range(len(status)):
                dict = {'Date':[values[i]], 'Date_YMD':[values[i]], 'Status':[status[j]]}
                dd2 = pd.DataFrame(dict)

                dd1 = pd.concat([dd1, dd2], ignore_index=True)
        return dd1


    def endGenerator(self):
        columns=['TT','AN','AP','AR','AS','BR','CH','CT','DN','DD','DL','GA','GJ','HR','HP','JK','JH','KA','KL','LA','LD','MP','MH','MN','ML','MZ','NL','OR','PY','PB','RJ','SK','TN','TG','TR','UP','UT','WB','UN']
        df = pd.DataFrame(columns=columns)

        dict = {'TT':[0],'AN':[0],'AP':[0],'AR':[0],'AS':[0],'BR':[0],'CH':[0],'CT':[0],'DN':[0],'DD':[0],'DL':[0],'GA':[0],'GJ':[0],'HR':[0],'HP':[0],'JK':[0],'JH':[0],'KA':[0],'KL':[0],'LA':[0],'LD':[0],'MP':[0],'MH':[0],'MN':[0],'ML':[0],'MZ':[0],'NL':[0],'OR':[0],'PY':[0],'PB':[0],'RJ':[0],'SK':[0],'TN':[0],'TG':[0],'TR':[0],'UP':[0],'UT':[0],'WB':[0],'UN':[0]}
        df1 = pd.DataFrame(dict)
        df3 = pd.concat([df, df1])
        for i in range(len(self.numner())):
            dff = pd.DataFrame(dict)
            df3 = pd.concat([df3, dff], ignore_index=True)
            
        return df3
    
    def finalDataFrame(self):

        finalDataFrame = pd.concat([self.startGenerator(), self.endGenerator()], axis=1, join='inner')
        finalDataFrame.to_csv('final.csv')
        

n = int(input("Enter the numner of days to predict\n"))
date = input("Enter the Starting date in the given format YYYY-MM-DD\n")
df = pd.read_csv('state_wise_daily.csv',parse_dates=['Date','Date_YMD'])
frame = Frame(n, date, df)
frame.finalDataFrame()
