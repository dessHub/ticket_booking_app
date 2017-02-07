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
                    cprint("***.........Event Created Successfully...........***",'green')
                else:
                    print("Invalid Input.Venue Can not be a number")
            else:
                cprint("____________Invalid End Date. End data should be greater or equal to Start Date__________", "red")
                return add_event(event_name)
        else:
            print(".........Invalid Dates. Start Date should be Greater than Today's date..........",'red')
            return add_event(event_name)

    except ValueError:
        print("***......Error in Creating event. Invalid Inputs. Note: Start date and End date should be greater than today...........***",'red')
        return add_event(event_name)

def view(name):
    """View all events or all tickets"""

    error = colored("\tInvalid Input. Tables to be modified are: Events, Tickets, Invalid_Tickets", 'red').center(80)
    if name == 'tickets' or name == 'Tickets' or name == 'TICKETS':

        try:
            conn.execute("SELECT * FROM tickets")
            items = conn.fetchall()

            cprint (tabulate(items, headers=['Ticket ID', 'Event ID','First Name','Last Name','Email', 'Event Name', 'Start Date', 'End Date', 'Venue'], tablefmt='fancy_grid'), 'cyan')
        except Exception as e:
            print(e)
            print("Error occurred")
    elif name == 'events' or name == 'EVENTS' or name == 'Events':
        try:
            conn.execute("SELECT * FROM event")
            items = conn.fetchall()

            cprint (tabulate(items, headers=['Event ID', 'Event Name', 'Start Date', 'End Date', 'Venue'], tablefmt='fancy_grid'), 'cyan')
            
        except:
            print ("Error in printing")
    elif name == 'invalid_tickets' or name == 'INVALID_TICKETS' or name == 'Invalid_Tickets' or name == 'Inavalid_tickets':
        try:
            conn.execute("SELECT * FROM invalidtickets")
            items = conn.fetchall()

            cprint (tabulate(items, headers=['Ticket Number', 'Ticket ID', 'Event ID','First Name','Last Name','Email', 'Event Name', 'Start Date', 'End Date', 'Venue'], tablefmt='fancy_grid'), 'red')
            print ("***____________All Events Displayed Above___________***")
        except:
            print ("Error in printing")
    else:

        print(error)
