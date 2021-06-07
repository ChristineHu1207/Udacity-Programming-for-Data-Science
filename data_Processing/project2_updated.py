import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june']
DAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    invalid_inputs = "I'm sorry, I'm not sure what you're referring to. Please try again.\n"

    while True:

        city = input("Would you like to see date for Chicago, New York, or Washington?\n").lower()
        if city not in CITY_DATA.keys():
            print(invalid_inputs)
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:

       month = input("Which month would you like to see? From January to June.\n").lower()
       if month not in MONTH_DATA:
           print(invalid_inputs)
       else:
           break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:

        day = input("And which day?\n").lower()
        if day not in DAY_DATA:
            print(invalid_inputs)
        else:
            break


    print('-' * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] as start_time

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':

        # use the index of the months list to get the corresponding int
        month = MONTH_DATA.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day if applicable
    if day != 'all':
        # filter by day to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # display the most common month
    print('Most popular month:', df['month'].mode()[0])

    # display the most common day of week
    print('Most popular day of week:', df['day_of_week'].mode()[0])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    occur_hour = df['hour'].value_counts().max()
    print('Most popular hour(s):{}, Occurrence:{}'.format(popular_hour, occur_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].value_counts().idxmax()
    occur_start = df['Start Station'].value_counts().max()
    print("Most commonly used start station:{}, Occurrence:{}".format(popular_start, occur_start))

    # display most commonly used end station
    popular_end = df['End Station'].value_counts().idxmax()
    occur_end = df['End Station'].value_counts().max()
    print("Most commonly used end station:{}, Occurrence:{}".format(popular_end, occur_end))

    # display most frequent combination of start station and end station trip

    df['combination'] = df['Start Station'] + ' + ' + df['End Station']
    popular_combine = df['combination'].value_counts().idxmax()
    occur_combine = df['combination'].value_counts().max()
    print("Most commonly combination of start station and end station:{}, Occurrence:{}".format(popular_combine, occur_combine))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time(in minutes):", df['Trip Duration'].sum()/60)

    # display mean travel time
    print("Average travel time (in minutes):", df['Trip Duration'].mean()/60)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' not in df.columns:
        print('The city chosen has no related data.')
    else:
        gender = df['Gender'].value_counts()
        print(gender)

    # Display earliest, most recent, and most common year of birth
    if 'Brith Year' not in df.columns:
            print('The city chosen has no related data.')
    else:
            earliest = int(df['Birth Year'].min())
            print('Earliest Year of Birth:', earliest)
            most_recent = int(df['Birth Year'].max())
            print('Most Recent Year of Birth:', most_recent)
            most_common = int(df['Birth Year'].mode()[0])
            print('Most Common Year of Birth:', most_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
"""
Asks user if he wants to see raw data

"""

    line_number = 0
    raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')

    while True:
        if raw_data.lower() != 'no':
            print(df.iloc[line_number : line_number + 5])
            line_number += 5
            raw_data = input('\nDo you want to see more raw data? Enter yes or no.\n')
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
