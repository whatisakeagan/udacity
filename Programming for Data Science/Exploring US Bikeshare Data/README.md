# Exploring US Bikeshare Data
## Background
Over the past decade, bicycle-sharing systems have been growing in number and popularity in cities across the world. Bicycle-sharing systems allow users to rent bicycles on a very short-term basis for a price. This allows people to borrow a bike from point A and return it at point B, though they can also return it to the same location if they'd like to just go for a ride. Regardless, each bike can serve several users per day.

Thanks to the rise in information technologies, it is easy for a user of the system to access a dock within the system to unlock or return bicycles. These technologies also provide a wealth of data that can be used to explore how these bike-sharing systems are used.

In this project, we use data provided by **[Motivate](https://www.motivateco.com/)**, a bike share system provider for many major cities in the United States, to uncover bike share usage patterns. We compare the system usage between three large cities: Chicago, New York City, and Washington, DC.

## Project Resources/Methods
Randomly selected data for the first six months of 2017 are provided for all three cities. All three of the data files contain the same core six (6) columns:

- Start Time (e.g., 2017-01-01 00:07:57)
- End Time (e.g., 2017-01-01 00:20:53)
- Trip Duration (in seconds - e.g., 776)
- Start Station (e.g., Broadway & Barry Ave)
- End Station (e.g., Sedgwick St & North Ave)
- User Type (Subscriber or Customer)

The Chicago and New York City files also have the following two columns:

- Gender
- Birth Year

## Walkthrough/Results
There are four questions that will change the answers:
1. Would you like to see data for Chicago, New York, or Washington?
1. Would you like to filter the data by month, day, or not at all?
1. (If they chose month) Which month - January, February, March, April, May, or June?
1. (If they chose day) Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?

After filtering the dataset, users will see the statistical result of the data, and choose to **start again** or **exit**.

### Statistics Computed
Based on the above user input, we provide the following information:

1. Popular times of travel (i.e., occurs most often in the start time)
- most common month
- most common day of week
- most common hour of day

2. Popular stations and trip
- most common start station
- most common end station
- most common trip from start to end (i.e., most frequent combination of start station and end station)

3. Trip duration
- total travel time
- average travel time

4. User info
- counts of each user type
- counts of each gender (only available for NYC and Chicago)
- earliest, most recent, most common year of birth (only available for NYC and Chicago)

### Error Handling
The code should handle unexpected input (e.g., typos, common mistakes, misunderstandings) well without failing. If it _does_ fail, it should fail gracefully (i.e., with a user-friendly error).

### Multiple Queries
The code should prompt the user whether they would like want to see the raw data. If the user answers 'yes,' then the script should print 5 rows of the data at a time, then ask the user if they would like to see 5 more rows of the data. The script should continue prompting and printing the next 5 rows at a time until the user chooses 'no,' they do not want any more raw data to be displayed.
