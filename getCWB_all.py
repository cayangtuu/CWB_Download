import urllib.request as request
import pandas as pd
import datetime
import os
from bs4 import BeautifulSoup 

sts = pd.read_csv('st_inform.csv', encoding='big5')

year = '2020'
date = pd.date_range(year+'-01-01', year+'-12-31', freq='1d')
Date = [datetime.datetime.strftime(dd, '%Y-%m-%d') for dd in date]


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
      print(Alltr)

      column = Alltr[3].get_text().split('\n')[1:-1] 

      for i in range(24):
         value = Alltr[i+4].get_text().split()
         data =pd.DataFrame(dict(zip(column, value)), index=[DD+ '-' + '%02d' % (i+1)])
         Data = pd.concat([Data, data], axis=0)

   Data = Data.drop(['ObsTime'], axis=1)
   Data = Data.replace('...', -999)
   DataDir = os.path.join('Data', year)
   try:
       os.makedirs(DataDir)
   except FileExistsError:
       pass
   Data.to_csv(DataDir + '/' + sta_ennm + sta_chnm + '(' + year + ').csv')
   print(Data)
