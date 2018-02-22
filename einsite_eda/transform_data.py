import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from numpy import random
from time import time
import calendar
from datetime import datetime
from geopy.distance import vincenty



def handle_na(df):
    df['new_user'] = df['new_user'].fillna('NO')
    df['tip_amount'] = df['tip_amount'].fillna(df['tip_amount'].median())
    df['surcharge'] = df['surcharge'].fillna(df['surcharge'].median())
    return df



def handle_loc_na(df):
    df['pickup_latitude'] = df['pickup_latitude'].fillna(df['pickup_latitude'].median())
    df['pickup_longitude'] = df['pickup_longitude'].fillna(df['pickup_longitude'].median())
    df['dropoff_latitude'] = df['dropoff_latitude'].fillna(df['dropoff_latitude'].median())
    df['dropoff_longitude'] = df['dropoff_longitude'].fillna(df['dropoff_longitude'].median())
    return df


def seperate_feature_and_target(df):
    target_df = df['fare_amount']
    feature_df = df.drop('fare_amount', axis = 1)
    return feature_df, target_df



def handle_catogary_data(feature_df):
    feature_df['new_user'] = feature_df['new_user'].map({'NO': 0, 'YES': 1})
    feature_df['payment_type'] = feature_df['payment_type'].map({'CRD': 1, 'CSH': 2,  'DIS': 3,  'NOC': 4,  'UNK': 5})
    return feature_df


def handle_time_data(feature_df):
    feature_df['pickup_datetime'] = pd.to_datetime(feature_df['pickup_datetime'])
    feature_df['dropoff_datetime'] = pd.to_datetime(feature_df['dropoff_datetime'])
    feature_df["duration"] = feature_df.apply(lambda x : cal_duration(x['pickup_datetime'], x['dropoff_datetime']), axis=1)
    feature_upg_df = feature_df.drop(['pickup_datetime', 'dropoff_datetime'], axis = 1)
    return feature_upg_df



def cal_duration(start, end):
    c = end - start
    d = divmod(c.days * 86400 + c.seconds, 60)
    return abs(d[0])


def measure_distance(newport_ri, cleveland_oh):
    return vincenty(newport_ri, cleveland_oh).miles



def cal_dist(feature_upg_df):
    feature_upg_df['distance'] = feature_upg_df.apply(lambda row: measure_distance((float(row['dropoff_latitude']), float(row['dropoff_longitude'])), (float(row['pickup_latitude']), float(row['pickup_longitude']))), axis=1)
    feature_upg_all_df = feature_upg_df.drop(['dropoff_longitude', 'pickup_latitude', 'pickup_longitude', 'dropoff_latitude'], axis = 1)
    return feature_upg_all_df


def handle_outliers(log_data):
    # For each feature find the data points with extreme high or low values
    for feature in log_data.keys():
        #print feature
        # TODO: Calculate Q1 (25th percentile of the data) for the given feature
        Q1 = np.percentile(log_data[feature], 25, axis = 0)

        # TODO: Calculate Q3 (75th percentile of the data) for the given feature
        Q3 = np.percentile(log_data[feature], 75, axis = 0)

        # TODO: Use the interquartile range to calculate an outlier step (1.5 times the interquartile range)
        iqr = Q3 - Q1
        step = 1.5 * iqr
        print step
        '''upper_limit = Q3 + iqr
        lower_limit = Q1 - iqr
        feature.append(upper_limit)
        feature.append(lower_limit)
        step = feature'''

        # Display the outliers
        print "Data points considered outliers for the feature '{}':".format(feature)
        display(log_data[~((log_data[feature] >= Q1 - step) & (log_data[feature] <= Q3 + step))])

        # OPTIONAL: Select the indices for data points you wish to remove
        outliers_data = log_data[~((log_data[feature] >= Q1 - step) & (log_data[feature] <= Q3 + step))]

        outliers  = outliers_data.index.get_values()

        # Remove the outliers, if any were specified
        good_data = log_data.drop(log_data.index[outliers]).reset_index(drop = True)
        print "good data is prepared, Enjoy Buddy :)"
    return good_data


