import pandas as pd

def preProcess(df):
    df.drop('participant_title', axis=1, inplace=True)
    df.drop('country_code', axis=1, inplace=True)
    df = pd.concat([df, pd.get_dummies(df['medal_type'])], axis=1)
    return df

