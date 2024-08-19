#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago' : 'chicago.csv',
              'new york city' : 'new_york_city.csv',
              'washington' : 'washington.csv' }
Months = {'jan','feb','mar','apr','may','jun','july','aug','sep','oct','nov','dec','all'}
Days = {'sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'}
   
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nchoose one of the cities listed below: \n 1) chicago\n 2) new york city\n 3) washington\n')
    while city.lower() not in {'chicago','new york city','washington'}:
        city = input('\nchoosing the city has failed, please renter your answer\n').lower()
    else:
        city = city.lower()
        
    # get user input for month (all, january, february, ... , june)
    month = input('\nchoose one of the months listed below: \n 1) jan \n 2) feb \n 3) mar \n 4) apr \n 5) may \n 6) jun \n 7) july \n 8) aug \n 9) sep \n 10) oct \n 11) nov \n 12) dec \n 13) all \n')
    while month not in Months:
            month = input('\nchoosing the month has failed, please renter your answer\n').lower()
    else: 
            month = month.lower()
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nchoose one of the days listed below: \n 1) sunday \n 2) monday \n 3) tuesday \n 4) wednesday \n 5) thursday \n 6) friday \n 7) saturday \n 8) all\n')
    while day not in Days:
        day = input('\nchoosing the day has failed, please renter your answer\n').lower
    else:
        day = day.lower()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    #df = pd.read_csv(r'C:\Users\Bushra\Documents\chicago.csv')
    #df.head() #to take a look at the table columns
    #df.info() #to check tables types and nulls
    df['month'] = pd.to_datetime(df['Start Time']).dt.strftime("%b").str.lower()
    df['day'] = pd.to_datetime(df['Start Time']).dt.strftime("%A").str.lower()
    if month != 'all':
        df = df[df['month']==month]
    if day != 'all':
        df = df[df['day']==day]
        
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    #df['Start Time'].dt.year.describe() #to check whether the trips occurred within different years or not
    trips_M_counter = pd.DataFrame(df.groupby(df['month'])['Start Time'].count()) #to count each month trips
    trips_M_counter = trips_M_counter.reset_index()
    common_month = trips_M_counter[trips_M_counter['Start Time']==trips_M_counter['Start Time'].max()] #to find month with max count of trips
    print('\nMost common month is',common_month['month'].to_string(index=False))
    
    
    # TO DO: display the most common day of week
    trips_D_counter = pd.DataFrame(df.groupby(df['day'])['Start Time'].count())
    trips_D_counter = trips_D_counter.reset_index()
    common_day = trips_D_counter[trips_D_counter['Start Time']==trips_D_counter['Start Time'].max()]
    print('\nMost common day is',common_day['day'].to_string(index=False))


    # TO DO: display the most common start hour
    trips_H_counter = pd.DataFrame(df.groupby(pd.to_datetime(df['Start Time']).dt.hour)['Start Time'].count())
    trips_H_counter.index = trips_H_counter.index.rename('Hours')
    trips_H_counter = trips_H_counter.reset_index()
    common_hour = trips_H_counter[trips_H_counter['Start Time']==trips_H_counter['Start Time'].max()]
    print('\nMost common hour is',common_hour['Hours'].to_string(index=False))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    trips_ss_counter = pd.DataFrame(df.groupby(df['Start Station'])['Start Time'].count())
    trips_ss_counter = trips_ss_counter.reset_index()
    common_ss = trips_ss_counter[trips_ss_counter['Start Time']==trips_ss_counter['Start Time'].max()]
    print('\nMost common start station is',common_ss['Start Station'].to_string(index=False))


    # TO DO: display most commonly used end station
    trips_es_counter = pd.DataFrame(df.groupby(df['End Station'])['Start Time'].count())
    trips_es_counter = trips_es_counter.reset_index()
    common_es = trips_es_counter[trips_es_counter['Start Time']==trips_es_counter['Start Time'].max()]
    print('\nMost common end station is',common_es['End Station'].to_string(index=False))

    # TO DO: display most frequent combination of start station and end station trip
    df['Start&End Stations'] = 'Start At : '+df['End Station']+', End At : '+df['Start Station']
    comb_counter = pd.DataFrame(df.groupby(df['Start&End Stations'])['Start Time'].count())
    comb_counter=comb_counter.reset_index()
    common_comb = comb_counter[comb_counter['Start Time']==comb_counter['Start Time'].max()]
    print('\nMost common Start and End stations combination is\n ',common_comb['Start&End Stations'].to_string(index=False))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total = df['Trip Duration'].sum()/3600
    Total_duration_Hours = int(total) #to convert sec to hours we will devide the total by 3600 (60 sec in the minute and 60 minute in the hour {60*60=3600})
    total = total - Total_duration_Hours
    Total_duration_min = int(total*60) # To convert the rest into minuts
    total = total*60 - Total_duration_min
    Total_duration_sec = int(np.ceil(total*60)) #To convert the rest into seconds
    print('\nTotal of trips duration is',Total_duration_Hours,' Hours and ',Total_duration_min,' Minuts and ',Total_duration_sec,' Seconds')


    # TO DO: display mean travel time
    total = df['Trip Duration'].mean()/3600
    Total_duration_Hours = int(total) 
    total = total - Total_duration_Hours
    Total_duration_min = int(total*60) # To convert the rest into minuts
    total = total*60 - Total_duration_min
    Total_duration_sec = int(np.ceil(total*60)) #To convert the rest into seconds
    print('\nAverage of trips duration is ',Total_duration_Hours,' Hours and ',Total_duration_min,' Minuts and ',Total_duration_sec,' Seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_counter = pd.DataFrame(df['User Type'].value_counts())
    print('\nuser Types are as follows\n',user_counter.to_string(header=False))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_counter = pd.DataFrame(df['Gender'].value_counts())
        print('\nuser genders are as follows\n',gender_counter.to_string(header=False))

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        Earliest = int(df['Birth Year'].min())
        Latest = int(df['Birth Year'].max())
        YOB_counter = pd.DataFrame(df['Birth Year'].value_counts())
        YOB_counter = YOB_counter.reset_index()
        common_YOB = YOB_counter[YOB_counter['Birth Year']==YOB_counter['Birth Year'].max()]
        common_YOB['index'] = int(common_YOB['index'])
        print('\nEarliest year of birth is ',Earliest,'\nLatest year of birth is ',Latest,'\nMost common year of birth is ',common_YOB['index'].to_string(index=False))

    firstrows = input('\nDo you want to check the first 5 rows of the dataset related to the chosen city?\n1)yes \n2)no\n')
    firstrows = firstrows.lower()
    df_c = df
    
    while firstrows == 'yes':
        print(df_c.head(5))
        firstrows = input('\nDo you want to check the next 5 rows of the dataset related to the chosen city?\n1)yes \n2)no\n')
        df_c = df_c.iloc[5:]
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

