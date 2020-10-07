import pandas as pd
import numpy as np

def timeseries_withdrawl(Excel_Name, Sheet_Name) :
    df = pd.read_excel(Excel_Name,sheet_name = Sheet_Name , index_col=0)

    #Dropping shitty Columns
    df = df.drop(['CHQ.NO.','VALUE DATE','.'],axis = 1)

    #Removing 'Account No' from index
    df['Account No'] = df.index
    df.reset_index(drop=True, inplace = True)

    #Converting Nan to 0s
    df['WITHDRAWAL AMT'] = df['WITHDRAWAL AMT'].fillna(0)
    df['DEPOSIT AMT'] = df['DEPOSIT AMT'].fillna(0)

    #Creating a new dataframe, with a column for Withdrawl Amount for each day.
    df.sort_values(by=['DATE'])
    day_1 = df['DATE'][0]
    day_n = df['DATE'][len(df)-1]
   
    df_1 = pd.DataFrame({'Date': pd.date_range(start = day_1, end = day_n), 'Withdrawl_Amount' : 0})
    d = df['DATE'][0]
    final_amount = 0

    for i in df.index: 
        dt = df['DATE'][i]
        amt = df['WITHDRAWAL AMT'][i] 
    
        if(dt == d) : 
            final_amount = final_amount + amt
        else : 
            df_1.loc[df_1['Date'] == d, ['Withdrawl_Amount']] = final_amount
            final_amount = df['WITHDRAWAL AMT'][i] 
    
        d = dt  
    
    #Handling the last row
    df_1.loc[df_1['Date'] == d, ['Withdrawl_Amount']] = final_amount
    
    #Setting Date as Index
    df_1 = df_1.set_index('Date')
    
    return df_1