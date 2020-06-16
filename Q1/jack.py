import pandas as pd
import datetime as datetime
import os
# Load CSV
curPath = os.path.dirname(os.path.abspath(__file__))
readPath = curPath + '/order_brush_order.csv'
Order_df = pd.read_csv(readPath)
df = Order_df.copy()
df.head()
# Remove unused orderId column
del df['orderid']
df.head()

def format_row_df(row_df):
    # covert string to date time, and sort based on event_time
    row_df['event_time'] = pd.to_datetime(row_df['event_time'])
    row_df = row_df.sort_values(by='event_time')
    return row_df

def get_buyer_name(window_df):
    name_list = []
    order_num = len(window_df)
    user_num = window_df['userid'].nunique()

    if(order_num/user_num >= 3):
        # get series based on order total number descending if it is a order brush period
        series = window_df.loc[:, 'userid'].value_counts()
        max_num = 3
        for item in series.iteritems():
            if(item[1]) >= max_num:
                max_num = item[1]
                # only get the most order number names
                name_list.append(str(item[0]))

    return name_list

def get_suspicious_buyer(row_df):
    row_sus_buyers_list = []

    row_df_time_list = row_df['event_time'].to_list()

    previous_event_time = row_df_time_list[0] - datetime.timedelta(hours=1)

    record_length = len(row_df_time_list)

    for start_pointer in range(record_length - 2):
        start_time = row_df_time_list[start_pointer]

        for end_pointer in range(start_pointer + 2, record_length):
            end_time = row_df_time_list[end_pointer]

            if end_time > start_time + datetime.timedelta(hours=1):
                break

            if end_pointer == record_length - 1:
                next_record_time = end_time
            else:
                next_record_time = row_df_time_list[end_pointer + 1]

            if next_record_time <= previous_event_time + datetime.timedelta(hours=1):
                end_time = start_time + datetime.timedelta(hours=1)

            window_df = row_df.loc[(row_df['event_time'] >= start_time) & (
                row_df['event_time'] <= end_time)]

            name_list = get_buyer_name(window_df)
            # only add distinct name in row_sus_buyers_list
            if(len(name_list) > 0):
                for name in name_list:
                    if(name not in row_sus_buyers_list):
                        row_sus_buyers_list.append(name)

        previous_event_time = start_time

    return row_sus_buyers_list


# convert df to dict
df_dict = dict(list(df.groupby(['shopid'])))

# disctinct shopid list from dict keys
shopid_list = list(df_dict.keys())

# declare syspicious buyer's list
sus_buyers_list = []

print("Start : " + str(datetime.datetime.now()))

row_counter = 0
for shopid in shopid_list:

    row_counter += 1

    row_df = df_dict[shopid]  # get row df for shopid

    row_df = format_row_df(row_df)

    # get this shopid sus_buyer_list with distinct name
    row_sus_buyers_list = get_suspicious_buyer(row_df)

    row_sus_buyers_list.sort(key=int)  # smaller numerical userid first
    row_sus_buyers_string = '&'.join(row_sus_buyers_list)

    if len(row_sus_buyers_string) > 0:
        sus_buyers_list.append(row_sus_buyers_string)
        print('Row'+str(row_counter) + ': id: ' +
              str(shopid) + ' user: ' + row_sus_buyers_string)
    else:
        sus_buyers_list.append('0')

# write CSV
out_put_dict = {'shopid': shopid_list[:len(
    sus_buyers_list)], 'userid': sus_buyers_list}

out_put_df = pd.DataFrame(out_put_dict)

out_put_df.to_csv(curPath + '/Solution_jack.csv', index=False)

print("End : " + str(datetime.datetime.now()))
