import numpy as np

def medal_tally(df):
    medal_df= df.drop_duplicates(subset=['slug_game','event_title', 'medal_type',"event_gender", 'participant_type','country_name', 'country_3_letter_code'])
    medal_tally = medal_df.groupby('country_name').sum()[['GOLD', 'SILVER', 'BRONZE']].sort_values('GOLD',
                                                                                            ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['GOLD'] + medal_tally['SILVER'] + medal_tally['BRONZE']

    medal_tally['GOLD'] = medal_tally['GOLD'].astype('int')
    medal_tally['SILVER'] = medal_tally['SILVER'].astype('int')
    medal_tally['BRONZE'] = medal_tally['BRONZE'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')
    return medal_tally

def medal_tally_visual(df):

    medal_tally = df.groupby('country_name').sum()[['GOLD', 'SILVER', 'BRONZE']].sort_values('GOLD', ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['GOLD'] + medal_tally['SILVER'] + medal_tally['BRONZE']



    return medal_tally

def gender_wise_medal(df):
    gender_medals = df['event_gender'].value_counts().reset_index()
    gender_medals.columns = ['Gender', 'Total Medals']   
    total_medals = gender_medals['Total Medals'].sum()
    gender_medals['Percentage'] = (gender_medals['Total Medals'] / total_medals) * 100
    gender_medals['Percentage'] = gender_medals['Percentage'].round(2)

    return gender_medals


def sport_wise_medal(df):
    medal_counts = df.groupby(['discipline_title', 'event_title'])['medal_type'].count().reset_index()
    sports_with_max_medals = medal_counts.loc[medal_counts.groupby('discipline_title')['medal_type'].idxmax()]
    sports_with_max_medals = sports_with_max_medals.sort_values(by='medal_type', ascending=False)
    sports_with_max_medals.reset_index(drop=True, inplace=True)
    return sports_with_max_medals



def Athletes_medal_tally(df):
    Athlete_medal_tally = df.groupby(['athlete_full_name','country_name']).sum()[['GOLD', 'SILVER', 'BRONZE']].sort_values('GOLD', ascending=False).reset_index()
    Athlete_medal_tally['Total'] = Athlete_medal_tally['GOLD'] + Athlete_medal_tally['SILVER'] + Athlete_medal_tally['BRONZE']
    
    return Athlete_medal_tally

def Athletes_medal_tally_Visual(df):
    Athlete_medal_tally = df.groupby(['athlete_full_name','country_name']).sum()[['GOLD', 'SILVER', 'BRONZE']].sort_values('GOLD', ascending=False).reset_index()
    Athlete_medal_tally['Total'] = Athlete_medal_tally['GOLD'] + Athlete_medal_tally['SILVER'] + Athlete_medal_tally['BRONZE']
    
    return Athlete_medal_tally.head(10)