import sqlite3
import datetime
import smtplib
from tabulate import tabulate
from termcolor import cprint, colored
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

# connect to database
db_con = sqlite3.connect("booking.db")

conn = db_con.cursor()
#Add new events
def add_event(event_name):
    # create table
    conn.execute("CREATE TABLE IF NOT EXISTS event( \
                    event_id INTEGER PRIMARY KEY, event_name TEXT, start_date DATE, end_date DATE, venue TEXT ) ")

    try:

    # Event Start Date
        date1_entry = input('Enter date event begins in YYYY-MM-DD format: ')
        year, month, day = map(int, date1_entry.split('-'))
        start = datetime.date(year, month, day)
        if start >= datetime.date.today():
    # Event End Date
            date2_entry = input('Enter date event ends in YYYY-MM-DD format: ')
            year, month, day = map(int, date2_entry.split('-'))
            end = datetime.date(year, month, day)
            # Checks if the End Date is Later or Earlier than the Start Date

            if end >= datetime.date.today() and end >= start:
                venue = input('Enter Venue: ')
                if type(venue) is str:
                    conn.execute("INSERT INTO event VALUES (null,?,?,?,?);",
                                 (event_name, start, end, venue))
                    db_con.commit()
                    cprint("***.........Data saved data...........***",'green')
                else:
                    print("Invalid Input.Venue Can not be a number")
            else:
                cprint("____________Invalid End Date. End data should be greater or equal to Start Date__________", "red")
                return add_event(event_name)
        else:
            print(".........Invalid Dates. Start Date should be Greater than Today's date..........",'red')
            return add_event(event_name)

    except ValueError:
        print("***......Error in saving data. Invalid Inputs. Note: Start date and End date should be greater than today...........***",'red')
        return add_event(event_name)
