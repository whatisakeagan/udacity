import time
import pandas as pd
import numpy as np
import os

# Create a reusable function for all prompts
def filter_prompt(variable, question, answer, dict):
    """
    Asks user for an answer to a question. Converts their answer to lowercase,
    compares against a given dictionary of key values, and responds accordingly.

    variable = the value we're looking to define
    question = question to ask the user
    answer = user's input converted to lowercase
    dict = key of values based on user input (answer)

    Returns:
        If they enter nothing, or enter something not in the dict, we call the function/prompt again and return nothing.
        If they enter something we don't recognize to many times, we exit completely
        (str) answer - dict value based on input
    """
    answer = ''
    while answer not in dict:
        answer = str(input(question)).lower()
        if answer == 'n' or answer == 'no':
            pass
        elif dict.get(answer, 0) != 0:
            variable = str(dict.get(answer))
            return variable
            break
        else:
            print('Hm, I don\'t recognize that as an option. Let\'s start over and try again!\n')
            return get_filters()

# Which city do they want to explore?
def get_city():
    city = ''
    cityq = 'Would you like to explore data for Chicago, New York City, or Washington?\n'
    citya = ''
    city_dict = {'chicago': 'chicago.csv', 'c': 'chicago.csv',
                'new york city': 'new_york_city.csv', 'nyc': 'new_york_city.csv', 'new york': 'new_york_city.csv',
                'washington': 'washington.csv', 'w': 'washington.csv'}
    city = filter_prompt(city, cityq, citya, city_dict)
    return city

# By which day do they want to filter (if any)?
def get_day():
    day = ''
    dayq = 'By which day of the week would you like to filter the data?\n'
    daya = ''
    day_dict = {'monday': 'monday', 'mon': 'monday',
                'tuesday': 'tuesday', 'tue': 'tuesday',
                'wednesday': 'wednesday', 'wed': 'wednesday',
                'thursday': 'thursday', 'thu': 'thursday',
                'friday': 'friday', 'fri': 'friday',
                'saturday': 'saturday', 'sat': 'saturday',
                'sunday': 'sunday', 'sun': 'sunday'}
    day = filter_prompt(day, dayq, daya, day_dict)
    return day

# By which day do they want to filter (if any)?
def get_month():
    month = ''
    monthq = 'By which month (January - June) would you like to filter the data?\n'
    montha = ''
    month_dict = {'january': 'january', 'jan': 'january', '1': 'january',
                'february': 'february', 'feb': 'february', '2': 'february',
                'march': 'march', 'mar': 'march', '3': 'march',
                'april': 'april', 'apr': 'april', '4': 'april',
                'may': 'may', '5': 'may',
                'june': 'june', 'jun': 'june', '6': 'june'}
    month = filter_prompt(month, monthq, montha, month_dict)
    return month

def wanna_filter():
    filter = ''
    filterq = 'Do you want to filter by either day of the week or month? \nIf YES, please type \'day\' or \'month\' \nIf NO, please type \'no\'.\n'
    filtera =''
    filter_dict = {'day': 'day', 'month':'month', 'no': ''}
    filter = filter_prompt(filter, filterq, filtera, filter_dict)
    return filter


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    city = get_city()
    # ask if they want to filter by day or month
    filter = wanna_filter()
    if filter == 'day':
        day = get_day()
        month = ''
        return city, month, day
    elif filter == 'month':
        month = get_month()
        day = ''
        return city, month, day
    else:
        day = ''
        month = ''
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
    # Read csv file for city
    df = pd.read_csv(city)
    ## Make sure numbers/dates/etc. are treated appropriately for our needs
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    #df[['Start Time', 'End Time']] = df[['Start Time', 'End Time']].apply(pd.to_datetime)
    # Filter dates/times where applicable
    ## Define tuples for months/days so we can index as numerals
    month_tuple = ('january', 'february', 'march', 'april', 'may', 'june')
    day_tuple = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    if month != '':
        #Index months as integers; in this case we need to add 1 to each to convert them
        month_int = month_tuple.index(str(month.lower()))+1
        #Create new columns indicating the start and end months respectively
        #This preserves the original data while still allowing us to filter
        df['Start Month'] = df['Start Time'].dt.month
        df['End Month'] = df['End Time'].dt.month
        df = df[df['Start Month']== month_int]
        return df
    elif day != '':
        #Index days as integers
        day_int = day_tuple.index(str(day.lower()))
        #Create new columns indicating the start and end weekdays respectively
        #This preserves the original data while still allowing us to filter
        df['Start Weekday'] = df['Start Time'].dt.dayofweek
        df['End Weekday'] = df['End Time'].dt.dayofweek
        df = df[df['Start Weekday']== day_int]
        return df
    else:
        return df

def proper_names(city, month, day):
    """
    Generates title case names based on previous inputs
    This allows us to provide stats to users without typos
    """
    city = str.title(os.path.splitext(city)[0])
    city = str.replace(city, '_', ' ')
    month = str.title(month)
    day = str.title(day)
    return city, month, day

def pop_month(df):
    #List months as a titlecase list so we can easily index
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    month_mode = int(df['Start Time'].dt.month.mode())
    ##Subtract 1 so we can display the corresponding string via the index
    mostpop_month = months[month_mode -1]
    print('The most common month for bikeshare travel was ' + mostpop_month + '.\n')

def pop_day(df):
    #List days as a titlecase list so we can easily index
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_mode = int(df['Start Time'].dt.dayofweek.mode())
    mostpop_day = days[day_mode]
    print('The most common day for bikeshare travel was ' + mostpop_day + '.\n')

def pop_hour(df):
    hour_mode = int(df['Start Time'].dt.hour.mode())
    if hour_mode == 0:
        ap = 'AM'
        twelvehrtime = 12
    elif hour_mode < 24 and hour_mode >= 13:
        ap = 'PM'
        twelvehrtime = hour_mode - 12
    elif hour_mode < 13 and hour_mode >= 1:
        ap = 'AM'
        twelvehrtime = hour_mode
    #Can't print as a concatenation bc hour is an integer here
    print('The most common hour for bikeshare travel was {}{}.\n'.format(twelvehrtime, ap))

def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel for ' + city + '...\n')
    start_time = time.time()
    # display the most common month
    if month == '' and day == '':
        pop_month(df)
        pop_day(df)
        pop_hour(df)
    elif month != '':
        print('You chose to ONLY look at data for the month of ' + month + ', so I won\'t calculate the most popular month :)\n')
        pop_day(df)
        pop_hour(df)
    else:
        print('You chose to ONLY look at data for dates that were ' + day + 's, so I won\'t calculate the most popular day of the week :)\n')
        pop_month(df)
        pop_hour(df)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip for ' + city + '...\n')
    start_time = time.time()
    # display most commonly used start station
    grouped_start_station = df.groupby(['Start Station']).size().reset_index(name='counts')
    pop_start = grouped_start_station.loc[grouped_start_station['counts'].idxmax()]
    print('The most common starting station was ' + pop_start['Start Station'] + '.\n')
    # display most commonly used end station
    grouped_end_station = df.groupby(['End Station']).size().reset_index(name='counts')
    pop_end = grouped_end_station.loc[grouped_end_station['counts'].idxmax()]
    print('The most common ending station was ' + pop_end['End Station'] + '.\n')
    # display most frequent combination of start station and end station trip
    grouped_start_end = df.groupby(['Start Station', 'End Station']).size().reset_index(name='counts')
    pop_start_end = grouped_start_end.loc[grouped_start_end['counts'].idxmax()]
    print('The most common starting and ending station pairing was ' + pop_start_end['Start Station'] + ' to ' + pop_start_end['End Station'] + '.\n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration for ' + city + '...\n')
    start_time = time.time()
    # display total travel time
    total_tr_time = df['Trip Duration'].sum()
    minute, second = divmod(total_tr_time, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)
    month, week = divmod(week, 4)
    year, month = divmod(month, 12)
    print('If we put everyone in ' + city + '\'s time using a bike together, the total travel time was {} years, {} months, {} weeks, {} days, {} hours, {} minutes and {} seconds. That\'s a lot!'.format(year, month, week, day, hour, minute, second))
    # display mean travel time
    avg_tr_time = round(df['Trip Duration'].mean())
    minute, second = divmod(avg_tr_time, 60)
    print('\nThat said, the average bikeshare rider in ' + city + ' used their bike for {} minutes and {} seconds.'.format(minute, second))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    subs = df['User Type'].value_counts()['Subscriber']
    custies = df['User Type'].value_counts()['Customer']
    print('In ' + city + ', the user breakdown was {} subscribers and {} customers.'.format(subs, custies))
    ## NYC and Chicago only
    if city == 'Chicago' or city == 'New York City':
        # Display counts of gender
        male = df['Gender'].value_counts()['Male']
        female = df['Gender'].value_counts()['Female']
        print('In ' + city + ', users\' gender breakdown was: {} male and {} female.'.format(male, female))
        # Display earliest, most recent, and most common year of birth
        mode_yr = int(df['Birth Year'].mode())
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        print('Most bikeshare users in ' + city + ' were born in ' + str(mode_yr) + '. \nThe oldest user was born in ' + str(oldest) + ' and the youngest user was born in ' + str(youngest) + '.')
    else:
        print('\nNormally I\'d give you some more information about user demographics, but I don\'t have those data for ' + city + '. Sorry about that!')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        city, month, day = proper_names(city, month, day)
        time_stats(df, city, month, day)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df, city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thanks for exploring these data with me!')
            break


if __name__ == "__main__":
	main()
