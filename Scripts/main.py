import pandas as pd
import numpy as np
import requests
import json

dir = "Data/"
filename = "IstanbulTraficData.csv"
TrafikDataDF = pd.read_csv(dir+filename, sep=';')
print("Veri Sayısı : "+str(TrafikDataDF["TrafficIndex"].count()))

# Eksik Gün Hesaplama
TrafikDataDF['TrafficIndexDate'] = TrafikDataDF['TrafficIndexDate'].apply(
    pd.to_datetime, utc="Europe/Istanbul")
Days = pd.to_datetime("today").date() - \
    TrafikDataDF.TrafficIndexDate.dt.date.max()
Days = Days.days
print("Eksik Gün Sayısı : "+str(Days))

# Eksik Saat Hesaplama
if (pd.to_datetime("today").time() == TrafikDataDF.loc[TrafikDataDF['TrafficIndexDate'].dt.date == TrafikDataDF.TrafficIndexDate.dt.date.max()].TrafficIndexDate.dt.time.max().strftime("%H:%M")) == False:
    Days = Days+1
    print("Saat Farkından Dolayı Değer Güncellendi. Yeni Değer : "+str(Days))

# IBB veri setinden 5 Dakika aralıklı olarak veriyi çekiyoruz
if Days != 0:
    response = requests.get(
        "https://api.ibb.gov.tr/tkmservices/api/TrafficData/v1/TrafficIndexHistory/"+str(Days)+"/5M")
    TrafikDataDF = pd.concat([TrafikDataDF, pd.DataFrame(response.json())])
    TrafikDataDF.reset_index(inplace=True)
    TrafikDataDF.drop("index", axis=1, inplace=True)
    print("Veri Güncellendi. Yeni Veri Sayısı : " +
          str(TrafikDataDF["TrafficIndex"].count()))

# Duplicate dataları temizliyoruz
TrafikDataDF['TrafficIndexDate'] = TrafikDataDF['TrafficIndexDate'].apply(
    pd.to_datetime, utc="Europe/Istanbul")
print("Duplicate Data Adedi")
print(TrafikDataDF[TrafikDataDF.duplicated(
    subset=['TrafficIndexDate'], keep="first")].count())
TrafikDataDF = TrafikDataDF.drop_duplicates(
    subset=['TrafficIndexDate'], keep="first")
TrafikDataDF[TrafikDataDF.duplicated(
    subset=['TrafficIndexDate'], keep="first")].count()

# Veri setine yeni özellikler ekleme
TrafikDataDF['TrafficIndexDate'] = TrafikDataDF['TrafficIndexDate'].apply(
    pd.to_datetime)

TrafikDataDF['Date'] = TrafikDataDF.TrafficIndexDate.dt.date
TrafikDataDF['Time'] = TrafikDataDF.TrafficIndexDate.dt.time
TrafikDataDF["Day"] = TrafikDataDF.TrafficIndexDate.dt.day
TrafikDataDF["Month"] = TrafikDataDF.TrafficIndexDate.dt.month
TrafikDataDF["Year"] = TrafikDataDF.TrafficIndexDate.dt.year
TrafikDataDF["Week"] = TrafikDataDF.TrafficIndexDate.dt.weekday
TrafikDataDF['Days_Of_Week'] = TrafikDataDF['TrafficIndexDate'].dt.dayofweek
TrafikDataDF["Day_Name"] = TrafikDataDF.TrafficIndexDate.dt.day_name()
TrafikDataDF['Is_Weekend_Flag'] = np.where(
    TrafikDataDF['Day_Name'].isin(['Sunday', 'Saturday']), "True", "False")
TrafikDataDF['Is_Night_Time'] = np.where(TrafikDataDF.TrafficIndexDate.dt.hour.isin(
    [22, 23, 24, 1, 2, 3, 4, 5, 6, 7]), "True", "False")
TrafikDataDF.count()

TrafikDataDF.to_csv(dir+filename, sep=';', index=False)
