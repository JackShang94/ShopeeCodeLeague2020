import pandas as pd
import numpy as np
import datetime
# read big data
ori_df = pd.read_csv('delivery_orders_march.csv')

# sample first 1000
# df = ori_df.loc[0:1000, :]
df = ori_df.copy()
df.head()

SLA_Manila_BtoS = [['metro manila',3],['luzon',5],['visayas',7],['mindanao',7]]
SLA_Luzon_BtoS = [['metro manila',5],['luzon',5],['visayas',7],['mindanao',7]]
SLA_Visayas_BtoS = [['metro manila',7],['luzon',7],['visayas',7],['mindanao',7]]
SLA_Mindanao_BtoS = [['metro manila',7],['luzon',7],['visayas',7],['mindanao',7]]

buyer_address_list = df['buyeraddress'].to_list()
seller_address_list = df['selleraddress'].to_list()
SLA_days_list = []

def get_SLA_days(target_SLA,seller_address):
    for item in target_SLA:
        if item[0] in seller_address:
            # print(item[1])
            return item[1]

i = 0
while i < len(buyer_address_list):
    buyer_address = buyer_address_list[i].lower()
    seller_address = seller_address_list[i].lower()
    # print(buyer_address)
    # print(seller_address)
    if 'metro manila' in buyer_address:
        target_SLA = SLA_Manila_BtoS
    elif 'luzon' in buyer_address:
        target_SLA = SLA_Luzon_BtoS
    elif 'visayas' in buyer_address:
        target_SLA = SLA_Visayas_BtoS
    else:
        target_SLA = SLA_Mindanao_BtoS

    day = get_SLA_days(target_SLA, seller_address)
    SLA_days_list.append(day)

    i += 1

del df['buyeraddress']
del df['selleraddress']
df['SLA'] = SLA_days_list 
df['SLA'] = df['SLA'].astype(int)

df['pick'] = pd.to_datetime(df['pick'], unit='s').dt.date
df['1st_deliver_attempt'] = pd.to_datetime(df['1st_deliver_attempt'], unit='s').dt.date
df['2nd_deliver_attempt'] = pd.to_datetime(df['2nd_deliver_attempt'], unit='s').dt.date

public_list = ['08/03/2020', '25/03/2020', '30/03/2020', '31/03/2020']
public_list = [pd.to_datetime(x,format="%d/%m/%Y").date() for x in public_list]

def cal_working_days(row, holidays_list=public_list):
    if pd.isnull(row[1]):
        return -1
    days = np.busday_count(row[0], row[1], weekmask = [1,1,1,1,1,1,0], holidays = holidays_list)
    return days

df['days_1'] = df[['pick', '1st_deliver_attempt']].apply(cal_working_days, axis=1)
df['days_2'] = df[['1st_deliver_attempt', '2nd_deliver_attempt']].apply(cal_working_days, axis=1)

df['is_late'] = 0

# late or not
df['is_late'][df['days_2']>3] = 1
df['is_late'][df['days_1']>df['SLA']] = 1

del df['pick']
del df['1st_deliver_attempt']
del df['2nd_deliver_attempt']
del df['SLA']
del df['days_1']
del df['days_2']
df['orderid'] = df['orderid'].apply(str)

df.to_csv('submission.csv',index=False)