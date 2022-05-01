#################################
#                               #
#  Generating Future dates      #
#                               #
#################################

import pandas as pd

class Dates:

    __existMonths = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    __existDays = ["31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"] 

    def __init__(self, num, startDate) -> None:
        self.num = num
        self.startDate = startDate

    def __dateParser(self):

        startDate = list(self.startDate)
        year = "".join(startDate[:4])
        month = "".join(startDate[5:7])
        day = "".join(startDate[8:10])
        # print(f"{year}-{month}-{day}")

        #temp
        mnth = month
        yea = year 
        dat = day

        
        mm = int(mnth)
        yy = int(yea)
        dd = int(dat)


        resultDates = []


        for i in range(self.num):
            
            if mnth in Dates.__existMonths:
                if dat == Dates.__existDays[mm-1]:
                    newDate = f"{yea}-{mnth}-{dat}"
                   
                    resultDates.append(newDate)

                    if mnth[0]=="0":
                        
                        mm+=1

                        if mm<10:
                            mnth = f"0{mm}"
                            
                        else:
                            mnth = f"{mm}"
                    else:
                        mm+=1
                        if mm>12:
                            mm = 1
                            mnth = f"0{mm}"
                            yy+=1
                            yea = f"{yy}"
                        else:
                            mnth = f"{mm}"              
                    dat = f"0{1}"
                    
                    
                elif dat != Dates.__existDays[mm-1]:
                    newDate = f"{yea}-{mnth}-{dat}"
                   
                    resultDates.append(newDate)
                    if dat[0]=="0":
                        dd = int(dat)
                        dd+=1  
                        if dd<10:
                            dat = f"0{dd}"      
                        else:
                            dat = f"{dd}"        
                    else:
                        dd = int(dat)
                        dd+=1
                        dat = f"{dd}"
                        
        #write_file("output.csv", resultDates)          
              
        return resultDates

    def da(self):
        return self.__dateParser()
        

    def futureDates(self):
        values = self.__dateParser()
        df = pd.DataFrame(values)
        df.columns=['ds']
        return df

        
