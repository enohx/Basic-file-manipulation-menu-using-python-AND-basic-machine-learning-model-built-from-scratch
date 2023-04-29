"""import os
os.system('pip install numpy')
os.system('pip install prettytable')
os.system('pip install matplotlib')"""  # install commands for libraries used in this project

import datetime
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.dates import DateFormatter, SecondLocator

from prettytable import PrettyTable  # do the thing with installing libraries at some point


# a container for the data read from the file
class Record:

    def __init__(self, country, date, name, team, laps, time):
        self.record_country = country
        self.record_date = date
        self.record_name = name
        self.record_team = team
        self.record_laps = laps
        self.record_time = time
        self.averageTime = ''


# a class that holds all the functions that require reading information from the data file
class Reader:
    def __init__(self, filename):  # takes as an argument the name of the data file
        self.recordBook = []  # a list that will contain the record objects
        # self.randomBook = []
        # self.counter = 0
        # a table object with the defined columns
        self.table = PrettyTable(["Country", "Date", "Name", "Team", "Laps", "Time"])
        self.file = filename

    def read(self):
        readingfile = open(self.file)
        skipper = 0

        for x in readingfile:
            # the if/else condition applied to skip the first line in the file which contains the fields
            if skipper >= 1:
                country, date, name, team, laps, time = x.split(',')  # getting the data from the file
                # adding the record obj with the data to the record list
                self.recordBook.append(Record(country, date, name, team, laps, str(time).strip('\n')))
            else:
                skipper = 1

    # a function used for option 2 in the menu
    def filter_records(self, lap_value: int):  # takes as an argument the number of laps
        index = 0
        filtered_records = []  # a list that will contain the records satisfying the condition

        for x in range(len(self.recordBook)):
            # checks for all the records that have a number of laps above the input
            if int(self.recordBook[x].record_laps) >= lap_value:
                filtered_records.insert(index, self.recordBook[x])
                index = index + 1
        return filtered_records

    # creates a table with the records present in the 'book' given as an argument
    def create_table(self, book):

        for x in range(len(book)):
            self.table.add_row([book[x].record_country,
                                book[x].record_date,
                                book[x].record_name,
                                book[x].record_team,
                                book[x].record_laps,
                                book[x].record_time])

    # displays the table on the screen
    def reader_tells(self):
        print(self.table)


# an object that converts a string representation of a time into milliseconds
class TimeObj:

    def __init__(self, time_str):
        hours, minutes, small_units = time_str.split(':')
        seconds, mili_seconds = small_units.split('.')

        self.Obj_hour = float(hours)
        self.Obj_minutes = float(minutes)
        self.Obj_seconds = float(seconds)
        self.Obj_miliseconds = float(mili_seconds)

    def to_miliseconds(self):  # converts the given string to milliseconds
        miliseconds = float(self.Obj_hour * 3600000
                            + self.Obj_minutes * 60000
                            + self.Obj_seconds * 1000
                            + self.Obj_miliseconds)
        return miliseconds


# a class that contains all the functions related to writing a file
class Writer:

    def __init__(self):
        self.TimeList = []
        self.ExtraColumn = []

    GreatReader = Reader('partA_input_data.txt')
    GreatReader.read()

    def avg_time(self):  # calculates the average time per lap and stores the result in a list
        counter = 0
        for x in range(len(self.GreatReader.recordBook)):
            # inserts the average time per lap into the list in the right format
            self.TimeList.insert(counter, round(
                TimeObj(self.GreatReader.recordBook[counter].record_time).to_miliseconds() / int(
                    self.GreatReader.recordBook[counter].record_laps), 3))
            counter = counter + 1

    # converts the milliseconds input into a time format H-H, M-M, S-S, MS-MS-MS
    def time_to_str(self, miliseconds):

        hours = miliseconds / 3600000
        minutes = (miliseconds % 3600000) / 60000
        seconds = ((miliseconds % 3600000) % 60000) / 1000
        milliseconds = ((miliseconds % 3600000) % 60000) % 1000

        return f"{str(round(hours)).zfill(2)}:" \
               f"{str(round(minutes)).zfill(2)}:" \
               f"{str(round(seconds)).zfill(2)}." \
               f"{str(round(milliseconds)).ljust(3, '0')}"

    # gets every time value from the TimeList [] through the time_to_str function
    def print_times_avg(self):

        for x in range(len(self.TimeList)):
            self.TimeList[x] = self.time_to_str(float(self.TimeList[x]))

    def expand_table(self):  # creates the table with the old data, adds a new column and displays the new table

        self.GreatReader.create_table(self.GreatReader.recordBook)
        self.GreatReader.table.add_column("avg time lap", self.TimeList)
        print(self.GreatReader.table)

    def write_table(self):  # puts the information of the table in a ',' delimited file

        file = open("partA_output_data.txt", 'w')
        for x in range(len(self.GreatReader.recordBook)):
            file_line = (f"{self.GreatReader.recordBook[x].record_country},"
                         f"{self.GreatReader.recordBook[x].record_date},"
                         f"{self.GreatReader.recordBook[x].record_name},"
                         f"{self.GreatReader.recordBook[x].record_team},"
                         f"{self.GreatReader.recordBook[x].record_laps},"
                         f"{self.GreatReader.recordBook[x].record_time},"
                         f"{self.TimeList[x]}")
            file.write(file_line + '\n')


# a hash map with the abbreviation of the month's name as key and their yearly order as a value
# it is used later for ordering purposes
def month_num(month):
    month_map = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12,
    }

    return month_map[month]


# the function responsible for option 1 in the menu
def opt1():
    great_reader = Reader('partA_input_data.txt')
    great_reader.read()  # reads the input file and save data in records
    great_reader.create_table(great_reader.recordBook)  # creates the table with the data from the file
    great_reader.reader_tells()  # displays the table on the screen


# function responsible for option 2
def opt2():
    while 1:
        # asks the user ofr an input until it gets a valid value
        try:
            lap_searcher = int(
                input(" What is the number of laps you want to search by?  ").strip())
            print('\n \n ')

        except ValueError:  # in case the input is not an integer thn display the appropriate message
            print(" Not a number im afraid, lets try again!\n")
        else:
            break
    # ones the program gets the valid value then it reads the input file and filters the records
    # according to the number of laps threshold
    # it then sorts the data on table according to the number of laps and displays the table on the screen
    great_reader = Reader('partA_input_data.txt')
    great_reader.read()
    great_reader.create_table(great_reader.filter_records(lap_searcher))
    great_reader.table.sortby = "Laps"
    great_reader.reader_tells()


# function responsible for option 3
def opt3():
    great_writer = Writer()  # calls the writer class which incorporates a reader that has read the input file
    great_writer.avg_time()  # calculates the average lap time in milliseconds
    great_writer.print_times_avg()  # turns the milliseconds value into a time string
    great_writer.write_table()  # creates the table with the data from the input file
    great_writer.expand_table()  # adds the new column to the table


# function responsible for option 4
def opt4():
    # creates a table with seven columns
    table = PrettyTable(["Country", "Date", "Name", "Team", "Laps", "Time", "Avg Lap Time"])
    reading_file = open("partA_output_data.txt")

    for x in reading_file:  # reads the data from the output file of option 3
        country, Date, name, team, laps, Time, avg_time = x.split(',')

        # formats the dat column of the data
        day, month, year = Date.split('-')
        dt = datetime.date(int('20' + year), month_num(month), int(day))
        # adds the info in the table
        table.add_row([country, dt, name, team, laps, Time, str(avg_time).strip('\n')])

    while 1:
        # the menu for the sorting options
        print('''                                      
            Please select one of the following fields for sorting:
            1) Country
            2) Date
            3) Name
            4) Team
            5) Laps
            6) Time
            7) Average Lap Time''')
        # it asks f=the user for a sorting option until it gets a valid input
        try:
            choice = int(input(' Your choice: '))
        except ValueError:
            print(' Not a valid sorting option please choose another option!')
        else:
            # based in the user input it saves the choice as one of the fields in the table
            if int(choice) == 1:
                opt_choice = 'Country'
                break
            elif int(choice) == 2:
                opt_choice = 'Date'
                break
            elif int(choice) == 3:
                opt_choice = 'Name'
                break
            elif int(choice) == 4:
                opt_choice = 'Team'
                break
            elif int(choice) == 5:
                opt_choice = 'Laps'
                break
            elif int(choice) == 6:
                opt_choice = 'Time'
                break
            elif int(choice) == 7:
                opt_choice = 'Avg Lap Time'
                break
            else:
                print(" please select a valid option: ")

    while 1:
        # menu for sorting order
        print('''
        PLease select an sorting order:

        1) Ascending
        2) Descending''')

        # it asks the user for a sorting order until it gets a valid input
        try:
            order_choice = int(input(' Your choice: '))
        except ValueError:
            print(' Not a valid sorting order please choose again')
        else:
            # based on the user input it saves the choice as ascending or descending
            if int(order_choice) == 1:
                order = 'Ascending'
                break
            elif int(order_choice) == 2:
                order = 'Descending'
                break
            else:
                print(' PLease select a valid order option: ')

            print('\n\n')

    # based on the choices the user made, data in the table is sorted in ascending or descending order of the field choice
    if order == 'Ascending':
        table.sortby = opt_choice
        print(table)
    elif order == 'Descending':
        table.sortby = opt_choice
        table.reversesort = True
        print(table)
    else:
        print(" not a valid sorting order")


# function responsible for option 5
def opt5():
    reading_file = open("partA_input_data.txt")  # opens the input data file
    drivers = set()  # creates a set with the names of the drivers
    skipper = 0  # used to iterate through the first line of the file containing the fields
    record_list = []  # holds the data from the file
    laps_list = []
    times_list = []
    counter = 0

    for x in reading_file:
        if skipper >= 1:
            country, date, name, team, laps, time = x.split(',')  # reads the data from the file
            record_list.insert(counter, Record(country, date, name, team, laps, TimeObj(time).to_miliseconds()))
            drivers.add(name)  # includes the name of each driver into the set
            counter = counter + 1
        else:
            skipper = 1

    drivers = list(drivers)  # it turns the set into a list

    # it iterates through the list and for every driver it calculates the total number of laps, the total time for those
    # laps and the average time per one lap
    for x in range(len(drivers)):

        total_laps = 0
        total_time = 0
        for y in range(len(record_list)):
            if record_list[y].record_name == drivers[x]:
                total_laps = total_laps + int(record_list[y].record_laps)
                total_time = total_time + int(record_list[y].record_time)
        laps_list.insert(x, total_laps)
        times_list.insert(x, total_time)
        # turns the result which would be in milliseconds into minutes by dividing with 60000
        times_list[x] = round(round(float(times_list[x] / laps_list[x])) / 60000, 3)

    print('\n \n')
    # plots the column graph with the X axis showing the drivers and the Y axis showing the average time per lap in min
    y_pos = np.arange(len(drivers))
    plt.bar(y_pos, times_list, align='center', alpha=0.5)
    plt.xticks(y_pos, drivers, fontsize=7, rotation=-40)

    plt.ylabel('Average Time per Lap in minutes')
    plt.title('Seasonal single Lap time for F1 winners')
    plt.tight_layout()
    plt.show()


# header for the text user interface
print('''\n\n\n 
Hello and Welcome to my project for CS340, Part A
These are the options for the menu:''')

checker_three = False

while 1:

    try:
        # displays the menu and asks the user for a choice until it gets a valid input
        choice = int(input("""\n\n\n
        1) Read data from the input file and display on a table

        2) Filter the previous data by the number of laps and display the sorted data

        3) Calculate a new stat. the average time per one lap, add the new information to the table and
           create an output file with the said information

        4) Using the output data file, sort the  information according to any of the seven fields in
           ascending or descending order

        5) Calculate the seasonal average time for lap for each player in the Grand Prix won by them and
           display the information in a graph

        6) Exit the Program


          Your Choice: """))
    except ValueError:  # in case the input is not an integer thn display the appropriate message
        print(" Not a Valid Input!! Please try again.")

    else:
        # based on the choice it executes the corresponding function
        if choice == 1:
            print("you have chosen option 1..... \n\n\n")
            opt1()

        elif choice == 2:
            print('you have chosen option 2.... \n\n\n')
            opt2()

        elif choice == 3:
            print('you have chose option 3.... \n\n\n')
            opt3()
            checker_three = True
        elif choice == 4:
            # since this option requires data from option three it checks if the user has run option 3 first and if not
            # it displays a message
            if checker_three:
                print('you have selected option 4....\n')
                opt4()
            else:
                print('To run this option you need to run option 3 first')
        elif choice == 5:
            print('you have selected option 5...')
            opt5()

        elif choice == 6:
            print('''                                     
            Thank you for running this program
            Hopefully we will meet again
            Good Bye!''')
            exit()
        else:
            print('\nthat is not a valid option, please try another one! ')