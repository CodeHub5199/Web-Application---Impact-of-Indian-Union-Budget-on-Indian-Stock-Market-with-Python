import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import datetime as dt
from nsepy import get_history
from datetime import date, timedelta, time
import datetime as dt

budget_dates = ['1994,2,28','1995,3,15','1996,6,4','1997,2,28','1998,6,1','1999,4,1','2000,2,29','2001,2,28',
                '2002,2,28','2003,2,28','2004,7,8','2005,2,28','2006,2,28','2007,2,28','2008,2,29','2009,7,6',
                '2010,2,26','2011,2,28','2012,3,16','2013,2,28','2014,7,10','2015,2,28','2016,2,29','2017,2,1',
                '2018,2,1','2019,7,5','2020,2,1','2021,2,1','2022,2,1']
years = ['Select']
st.title('Union Budget Impact on Stock Market')
st.image('budget.jpg')
for j in reversed(range(1994,2023)):
    years.append(j)
st.sidebar.subheader('Budget related market move:')
year = st.sidebar.selectbox('Select Budget Year',years)
year = str(year)
history_days = st.sidebar.number_input('Enter days: ',5,100)
if st.sidebar.button('OK'):
    for day in budget_dates:
        if year == day[0:4]:
            b_date = day
    st.markdown(f'Budget Date: **{b_date}**')
    time_format = '%Y,%m,%d'
    b_date = dt.datetime.strptime(b_date,time_format)
    init_date = b_date - timedelta(days=(history_days+1))
    final_date =  b_date + timedelta(days=(history_days+1))
    upper_init_date = init_date
    upper_final_date = b_date - timedelta(days=1)
    lower_init_date = b_date + timedelta(days=1)
    lower_final_date = final_date

    upper_main_df = get_history('NIFTY',upper_init_date,upper_final_date,index=True).reset_index()
    lower_main_df = get_history('NIFTY',lower_init_date,lower_final_date,index=True).reset_index()
    b_day_df = get_history('NIFTY',b_date,b_date,index=True).reset_index()

    lower_init_close = lower_main_df.head(1).Close[0]
    lower_df = lower_main_df.tail(1).reset_index()
    lower_final_close = lower_main_df.loc[0,'Close']
    upper_init_close = upper_main_df.head(1).Close[0]
    upper_df = upper_main_df.tail(1).reset_index()
    upper_final_close = upper_main_df.loc[0,'Close']
    p_chng = []
    frame = pd.concat([upper_main_df,b_day_df,lower_main_df])
    frame = frame.reset_index()
    frame_df = frame.drop(['index','Volume','Turnover'],axis=1)
    for i in range(len(frame_df)):
        per = np.round(((frame.Close[i]-frame_df.Open[i])/frame_df.Open[i])*100,2)
        p_chng.append(per)
    frame_df['% Change'] = p_chng
    st.write('Market history of specified days')
    st.table(frame_df)
    st.write('View some basic statistical details like percentile, mean, std etc.')
    frame_history = frame_df.describe()
    st.table(frame_history)
    st.write('Max one day rise')
    max_rise = frame_df['% Change'].max()
    st.table(frame_df[frame_df['% Change']==max_rise])

    st.write('Max one day fall')
    max_fall = frame_df['% Change'].min()
    st.table(frame_df[frame_df['% Change']==max_fall])

    fig = plt.figure(figsize=(17,8))
    plt.scatter(frame_df.Date,frame_df.Close)
    plt.plot(frame_df.Date,frame_df.Close)
    plt.grid()
    st.pyplot(fig)
    
