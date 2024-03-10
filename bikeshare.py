import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
            
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print("What city are you interested in? Please select Chicago, New York City, or Washington.")
        city = input(">> ")
        try:
            city = city.strip().lower()
            assert(city in ('chicago', 'new york city', 'washington'))
            break
        except:
            print("Please choose one of these cities: chicago, new york city, or washington")
        

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        print("What month are you interested in? Please select All, or any month between January and June.")
        month = input(">> ")
        try:
            month = month.strip().lower()
            assert(month in ('all', 'january', 'february', 'march', 'april', 'may', 'june'))
            break
        except:
            print("Please choose one of these months: all, january, february, march, april, may, june")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print("What day of the week are you interested in? Please select All, or any day of the week.")
        day = input(">> ")
        try:
            day = day.strip().lower()
            assert(day in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'))
            break
        except:
            print("Please choose one of these days: all, monday, tuesday, wednesday, thursday, friday, saturday, sunday")

   
    if (day != 'all') and (month != 'all'):
        print("You chose to look at data for {} on {}s in {}".format(city.title(), day.title(), month.title()))
    elif month != 'all':
        print("You chose to look at data for {} in {}".format(city.title(), month.title()))
    elif day != 'all':
        print("You chose to look at data for {}s in {}".format(day.title(), city.title()))
    elif (month == 'all') and (day == 'all'):
        print("You chose to look at data for {}".format(city.title(), month.title()))
        
        
    print('-'*40)
     
     
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Asks user if they want to view data and if so, outputs data.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]
    
    
    print("Do you want to view some data? Please type Yes or No.")
    view_data = input(">> ")
    view_data = view_data.strip().lower()
    if view_data == 'yes':
        print(df[0:5])
        row_ind = 5  
        while True:
            print("Do you want to see some more data? Please type Yes or No.")
            view_data2 = input(">> ")
            view_data2 = view_data2.strip().lower()
            if view_data2 == "yes":
                print(df[row_ind:row_ind+5])
                if len(df[row_ind:row_ind+5]) < 5:
                    print("This is the last of the data. Moving on now...")
                    break
                
                row_ind += 5
                
            elif view_data2 == "no":
                break
            else:
                print("Invalid selection. Please type Yes or No.")
            
    
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    month_labels = ['january', 'february', 'march', 'april', 'may', 'june']
    print("The most common month is {}.".format(month_labels[most_common_month-1].title()))
    
    # TO DO: display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of week is {}.".format(most_common_day_of_week))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print("The most common start hour is {}.".format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most common start station is {}.".format(most_common_start_station))

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most common end station is {}.".format(most_common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    common_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most frequent combination is from {} to {}.".format(common_combo[0],common_combo[1]))
    
    
    #most_common_both_station = df[['Start Station', 'End Station']].mode()
    #print("The most common combination is {}".format(most_common_both_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time was {:.0f} hours.".format(total_travel_time/3600))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time was {:.1f} minutes.".format(mean_travel_time/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("There were {} Subscribers and {} Customers.".format(user_types['Subscriber'],user_types['Customer']))

    # TO DO: Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print("There were {} male and {} female riders.".format(gender_types['Male'],gender_types['Female']))
    except:
        print("There is no data on gender in Washington.")
    
    
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = df['Birth Year'].dropna().min()
        latest_birth_year = df['Birth Year'].dropna().max()
        most_common_birth_year = df['Birth Year'].dropna().mode()
        print("The earliest, most recent, and most common birth years were {}, {}, and {}, respectively.".format(int(earliest_birth_year), int(latest_birth_year), int(most_common_birth_year)))
    except:
        print("There is no data on birth year in Washington.")
    


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
        
        print('\nWould you like to restart? Enter yes or no.')
        restart = input('>>')
        restart = restart.strip().lower()
            
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
