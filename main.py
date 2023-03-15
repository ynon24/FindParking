import datetime
import numpy
import pandas as pd


segment_data = pd.read_csv('segment_data.csv')
sign_data = pd.read_csv('sign_data.csv')


def replace_empty_sign_day(row):
    if pd.isnull(row['sign_day']):
        return [i for i in range(0,6)]
    return row['sign_day']


def replace_empty_sign_date(row):
    if pd.isnull(row['sign_date']):
        return [i for i in range(0, 32)]
    return row['sign_date']


def replace_empty_sign_month(row):
    if pd.isnull(row['sign_month']):
        return [i for i in range(0, 12)]
    return row['sign_month']

"""filling up missing data with relevant data"""
sign_data['sign_day'] = sign_data.apply(replace_empty_sign_day, axis=1)
sign_data['sign_date'] = sign_data.apply(replace_empty_sign_date, axis=1)
sign_data['sign_month'] = sign_data.apply(replace_empty_sign_month, axis=1)


def compare(given_hour_as_string, dt):
    if given_hour_as_string == 'All day':
        return 0
    given_hour = datetime.datetime.strptime(given_hour_as_string, '%H:%M')
    given_hour_in_mins = given_hour.hour * 60 + given_hour.minute
    dt_in_mins = dt.hour * 60 + dt.minute
    return numpy.sign(given_hour_in_mins - dt_in_mins)


def select_relevant_signs(signs_of_segment, dt):
    paid_signs = signs_of_segment.loc[signs_of_segment['paid']]
    signs_of_segment_rel_hour = paid_signs.loc[(paid_signs['start_date'].apply(lambda x: compare(x, dt) <= 0)) & (paid_signs['end_date'].apply(lambda x: compare(x, dt) >= 0))]
    signs_of_segment_rel_month = signs_of_segment_rel_hour.loc[signs_of_segment_rel_hour['sign_month'].apply(lambda x: str(dt.month-1) in str(x))]
    signs_of_segment_rel_day_in_month = signs_of_segment_rel_month.loc[signs_of_segment_rel_month['sign_date'].apply(lambda x: str(dt.day) in str(x))]
    signs_of_segment_rel_day_in_week = signs_of_segment_rel_day_in_month.loc [signs_of_segment_rel_day_in_month['sign_day'].apply(lambda x: str((dt.weekday()+1) % 7) in str(x))]
    return signs_of_segment_rel_day_in_week


def calc(segment_id, dt):
    segments_by_id = segment_data.loc[segment_data['segment_id'] == segment_id]
    sign_ids = segments_by_id.loc[:, 'sign_id']
    signs_of_segment = sign_data.loc[sign_data['sign_id'].isin(sign_ids)]
    relevant_signs = select_relevant_signs(signs_of_segment, dt)
    relevant_signs_ids = relevant_signs.loc[:, 'sign_id']
    final_signs = segment_data.loc[segment_data['sign_id'].isin(relevant_signs_ids)]
    segments_by_id_after_filtering = final_signs.loc[segment_data['segment_id'] == segment_id]
    return segments_by_id_after_filtering['max_spots'].sum()
















