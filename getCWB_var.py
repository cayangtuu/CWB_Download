import urllib.request as request
import pandas as pd
import os, datetime, calendar
from bs4 import BeautifulSoup 

sts = pd.read_csv('st_inform2.csv', encoding='big5')

year = '2021'
month = '08'
LM = calendar.monthrange(int(year), int(month))[1]
date = pd.date_range(year+'-'+month+'-01', year+'-'+month+'-'+str(LM), freq='1d')
Date = [datetime.datetime.strftime(dd, '%Y-%m-%d') for dd in date]

# T2:4, WS:7, WD:8
var = 'T2'
var_id = 4

allData = pd.DataFrame()
for ii in range(len(sts)):
   sta_chnm = str(sts.iloc[ii, 0])
   sta_ennm = str(sts.iloc[ii, 1])
   print(f'測站: {sta_chnm}  ID: {sta_ennm}') 

   Data = pd.DataFrame()

   for DD in Date:
      src = 'https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=' + sta_ennm + '&stname=%25E5%25A4%25A9%25E6%25AF%258D&datepicker=' + DD + '&altitude=10m'

      with request.urlopen(src) as response:
           result = response.read().decode("utf-8")
      soup = BeautifulSoup(result, "html.parser")
      Alltr = soup.find_all('tr')

      column = Alltr[3].get_text().split('\n')[var_id]
#     print(column)

      for i in range(24):
         value = Alltr[i+4].get_text().split()[var_id-1]
         data =pd.DataFrame({sta_chnm:value}, index=[DD+ '-' + '%02d' % (i+1)])
         Data = pd.concat([Data, data], axis=0)
     
   allData = pd.concat([allData, Data], axis=1)
   print(allData)


allData = allData.replace(['...','V'], -999)
DataDir = os.path.join('Data', year)
try:
    os.makedirs(DataDir)
except FileExistsError:
    pass
allData.to_csv(DataDir + '/' + year + month + var + '.csv', encoding='utf-8-sig')
print(allData)
