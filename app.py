import Processing, analysis
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv("medals.csv")

data = Processing.preProcess(data)

st.sidebar.header("----- GFG GEEK A THON -----")
st.sidebar.header("Olympic Analysis Report")

user_menu =st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.title("Overall Medal Tally")
    medal_tally_df = analysis.medal_tally(data)
    st.table(medal_tally_df)

    st.sidebar.subheader('Search Country Medal Tally')
    selected_country = st.sidebar.text_input("Enter a country name:")

    if selected_country:
            selected_country = selected_country.strip().title() 
            country_tally = medal_tally_df[medal_tally_df['country_name'] == selected_country]

            if not country_tally.empty:
                st.subheader(f'Medal Tally for {selected_country}')
                st.sidebar.table(country_tally)
            else:
                st.warning(f'{selected_country} not found in the dataset.')


if user_menu == 'Overall Analysis':
    data['year'] = data['slug_game'].str.split('-').str[-1]
    editions = data['year'].unique().shape[0]
    data['cities'] = data['slug_game'].str.split('-').str[0]
    cities = data['cities'].unique().shape[0]
    sports = data['discipline_title'].unique().shape[0]
    events = data['event_title'].unique().shape[0]
    athletes = data['athlete_full_name'].unique().shape[0]
    nations = data['country_name'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    col1.header("Editions")
    col1.title(editions)

    col2.header("Hosts")
    col2.title(cities)

    col3.header("Sports")
    col3.title(sports)

    col1, col2, col3 = st.columns(3)
    col1.header("Events")
    col1.title(events)

    col2.header("Nations")
    col2.title(nations)

    col3.header("Athletes")
    col3.title(athletes)

    # Participation of Countries by Year

    participation_count = data.groupby('year')['country_name'].nunique().reset_index()
    fig = px.line(participation_count, x='year', y='country_name', title='Participation of Countries by Year',
              labels={'country_name': 'Number of Countries', 'year': 'Year'})
    st.plotly_chart(fig)

    # Most Successful Country

    medal_tally = analysis.medal_tally_visual(data)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=medal_tally['country_name'], y=medal_tally['GOLD'], name='Gold', marker_color='gold'))
    fig.add_trace(go.Bar(x=medal_tally['country_name'], y=medal_tally['SILVER'], name='Silver', marker_color='silver'))
    fig.add_trace(go.Bar(x=medal_tally['country_name'], y=medal_tally['BRONZE'], name='Bronze', marker_color='brown'))

    fig.add_trace(go.Bar(x=medal_tally['country_name'], y=medal_tally['Total'], name='Total Medals', marker_color='darkgrey'))

    fig.update_layout(barmode='stack', showlegend=True, title='Most Successful Country', legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig.update_xaxes(title_text='Country')
    fig.update_yaxes(title_text='Medal Count')

    st.plotly_chart(fig)

    # Distribution of Medal Types

    medal_distribution = data['medal_type'].value_counts().reset_index()
    medal_distribution.columns = ['medal_type', 'count']

    fig = px.pie(medal_distribution, names='medal_type', values='count', title='Distribution of Medal Types',
                labels={'medal_type': 'Medal Type', 'count': 'Medal Count'})
    st.plotly_chart(fig)

    sport_wise_medal_df = analysis.sport_wise_medal(data)
    st.header("Sports_wise_medal")
    st.dataframe(sport_wise_medal_df)

if user_menu == 'Athlete wise Analysis':
     st.header("Athlete Ranking having Maximum number of Gold")

     Athletes_medal_tally_df = analysis.Athletes_medal_tally(data)
     st.dataframe(Athletes_medal_tally_df)

    #  Most Successful Athletes based on No. of GOLD

     Athletes_medal_tally = analysis.Athletes_medal_tally_Visual(data)
     fig = go.Figure()

     fig.add_trace(go.Bar(x=Athletes_medal_tally['athlete_full_name'], y=Athletes_medal_tally['GOLD'], name='Gold', marker_color='gold',
                            hovertext=Athletes_medal_tally['country_name'] + ': ' + Athletes_medal_tally['GOLD'].astype(str) + ' Gold'))
     fig.add_trace(go.Bar(x=Athletes_medal_tally['athlete_full_name'], y=Athletes_medal_tally['SILVER'], name='Silver', marker_color='silver',
                            hovertext=Athletes_medal_tally['country_name'] + ': ' + Athletes_medal_tally['SILVER'].astype(str) + ' Silver'))
     fig.add_trace(go.Bar(x=Athletes_medal_tally['athlete_full_name'], y=Athletes_medal_tally['BRONZE'], name='Bronze', marker_color='brown',
                            hovertext=Athletes_medal_tally['country_name'] + ': ' + Athletes_medal_tally['BRONZE'].astype(str) + ' Bronze'))

     fig.add_trace(go.Bar(x=Athletes_medal_tally['athlete_full_name'], y=Athletes_medal_tally['Total'], name='Total Medals', marker_color='darkgrey',
                            hovertext=Athletes_medal_tally['country_name'] + ': ' + Athletes_medal_tally['Total'].astype(str) + ' Total Medals'))

     fig.update_layout(barmode='stack', showlegend=True, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                        title='Most Successful Athletes based on No. of GOLD', xaxis_title='Athlete', yaxis_title='Medal Count')

     st.plotly_chart(fig)

    #  Medals Distribution by Gender

     gender_wise_medals = analysis.gender_wise_medal(data)
     fig = px.pie(gender_wise_medals, names='Gender', values='Percentage', title='Medals Distribution by Gender',
                 labels={'Gender': 'Gender', 'Percentage': 'Percentage (%)'})
     st.plotly_chart(fig)

    #  Participation by Year and Gender

     data['year'] = data['slug_game'].str.split('-').str[-1]
     participation_counts = data.groupby(['year', 'event_gender'])['athlete_full_name'].count().reset_index()

     fig = px.line(participation_counts, x='year', y='athlete_full_name', color='event_gender',
          title='Participation by Year and Gender', labels={'year': 'Year', 'athlete_full_name': 'Number of Participants'})
     st.plotly_chart(fig)



     

