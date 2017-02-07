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

def delete_event(eventid):

    try:

        data = int (eventid)

        conn.execute("DELETE FROM event WHERE event_id=?", (data,))
        db_con.commit()
        cprint("***_______Event with ID " + eventid +" has been deleted successfully__________***",'green')

    except ValueError:
        print("Invalid Input. Try Again")
        return delete_event()

def edit_event(event_id):
    """edit Data in events"""
    if type(event_id) is int:

        try:
            eventid = int(event_id)


            conn.execute("SELECT * FROM event WHERE event_id=?", (eventid,))
            items = conn.fetchall()

            cprint (tabulate(items, headers=['Event ID', 'Event Name', 'Start Date', 'End Date', 'Venue'], tablefmt='fancy_grid'), 'cyan')
            label = input("Enter the field to be Editted: ")

            if label == 'name':

                try:
                    name = input("Enter New Event Name: ")
                    conn.execute("UPDATE event SET event_name=? WHERE event_id=?", (name, eventid,))
                    db_con.commit()
                    cprint("***______________Event Name Updated successfully____________***",'green')
                    cprint("***______________New Record____________***",'green')
                    conn.execute("SELECT * FROM event WHERE event_id=?", (eventid,))
                    items = conn.fetchall()
                    cprint (tabulate(items, headers=['Event ID', 'Event Name', 'Start Date', 'End Date', 'Venue'], tablefmt='fancy_grid'), 'cyan')

                except:
                    print("Error in updating db")
            elif label == 'start_date':

                date1 = input('Enter the new start date in YYYY-MM-DD format: ')
                try:
                    year, month, day = map(int, date1.split('-'))
                    start = datetime.date(year, month, day)#edits

                    try:
                        if start >= datetime.date.today():
                            conn.execute("UPDATE event SET start_date=? WHERE event_id=?", (start, eventid,))
                            db_con.commit()
                            cprint ("***_______________Start Date Updated successfully____________***",'green')
                            cprint("***______________New Record____________***", 'green')
                            conn.execute("SELECT * FROM event WHERE event_id=?", (eventid,))
                            items = conn.fetchall()
                            cprint (tabulate(items, headers=['Event ID', 'Event Name', 'Start Date', 'End Date', 'Venue'], tablefmt='fancy_grid'), 'cyan')
                    except Exception as e:
                        print ("Error in updating Event Start Time. End Date should be Greater or Equal to Today's Date.")
                except ValueError:
                    print("Invalid Input.Try Again")
                    return edit_event()

            elif label == 'end_date':

                date2 = input('Enter the new End date in YYYY-MM-DD format: ')
                year, month, day = map(int, date2.split('-'))
                end = datetime.date(year, month, day)

                try:
                    if end >= datetime.date.today():
                        conn.execute(
                            "UPDATE event SET end_date=? WHERE event_id=?", (end, eventid,))
                        db_con.commit()
                        print("\n***_____________End Date Updated successfully____________***\n")
                        print("\n***______________New Record____________***\n")
                        conn.execute("SELECT * FROM event WHERE event_id=?", (eventid,))
                        items = conn.fetchall()
                        cprint (tabulate(items, headers=['Event ID', 'Event Name', 'Start Date', 'End Date', 'Venue'], tablefmt='fancy_grid'), 'cyan')
                except Exception as e:
                    print("Error in updating End Date. End Date should be Greater or Equal to Today's Date" + str(e))

            elif label == 'venue':

                if type(label) is not str:
                    print("Invalid Input. Input should be a number")
                    return event_id
                else:
                    venue = str(input("Enter the new name: "))
                    try:
                        conn.execute(
                            "UPDATE event SET venue=? WHERE event_id=?", (venue, eventid,))
                        db_con.commit()
                        print("\n***______________Venue Updated successfully____________***\n")
                        print("\n***______________New Record____________***\n")
                        conn.execute("SELECT * FROM event WHERE event_id=?", (eventid,))
                        items = conn.fetchall()
                        cprint (tabulate(items, headers=['Event ID', 'Event Name', 'Start Date', 'End Date', 'Venue'], tablefmt='fancy_grid'), 'cyan')
                    except Exception as e:
                        print("Error in updating db "+ str(e))
            else:
                print("Invalid Input")
                return edit_event()
        except ValueError:
            print ("Invalid Input.Try Again")
            return edit_event()
    else:
        print("Invalid, event id should be number")



def ticket_validation():
    """Ticket Validation"""
    try:
        t_id =int(input ("Enter Your Ticket ID: "))
        conn.execute("SELECT * FROM tickets WHERE ticket_id=?", (t_id,))
        items = conn.fetchall()
        cprint (tabulate(items, headers=['Ticket ID', 'Event ID','First Name','Last Name','Email', 'Event Name', 'Start Date', 'End Date', 'Venue'], tablefmt='fancy_grid'), 'cyan')
        cprint("...This Ticket is valid...", 'cyan')

    # Catch Value Error when the user inputs a wrong value
    except ValueError:
        print("Invalid Input")
        return ticket_validation()

def generate_ticket(eventid):
    """Generating Tickets and sending Emails containg the Ticket details"""
    conn.execute("CREATE TABLE IF NOT EXISTS tickets( \
                    ticket_id INTEGER PRIMARY KEY, event_id INTEGER, owner_fname TEXT, owner_lname TEXT, owner_email TEXT, event_name TEXT, start_date DATE, end_date DATE, venue TEXT, FOREIGN KEY (event_id) REFERENCES event(event_id)) ")

    print ("Generate Tickets")
    print ("")
    try:
        event_id = int(eventid)
        owner_fname = input ("Enter Your First Name: ")
        owner_lname = input ("Enter Your Last Name: ")
        receivers = input ("Enter your Email: ")
        #Verifies the user's email
        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        s = receivers
        if re.search(regex, s):
            match = re.search(regex, s)
            #runs if email is in correct format
            try:
            # run sql command and commit data to db
                item = conn.execute("SELECT event_name, start_date, end_date, venue FROM event WHERE event_id=?",(str(event_id)))
                for column in item:
                    name = column [0]
                    s_date = column [1]
                    e_date = column [2]
                    venue = column [3]

                    conn.execute("INSERT INTO tickets VALUES (null,?,?,?,?,?,?,?,?);",
                                    (event_id, owner_fname, owner_lname, receivers, name, s_date, e_date, venue))
                    db_con.commit()
                print("***Data saved data...........***")
                print ("***___Sending Email___***")
                #Sending Ticket Details to the user

                senders = "youremailaccount"      #Senders Email Address
                msg = MIMEMultipart()
                msg['From'] = senders
                msg['To'] = receivers
                msg['Subject'] = "Ticket Booking"

                body = " Name:" + owner_fname + " " + owner_lname +"\n Event Name:" + name + "\n Starts On: " + s_date + "\n Ends On: " + e_date + "\n Venue: " + venue
                msg.attach(MIMEText(body, 'plain'))

                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587)    #Call Gmail SMTP server
                    server.starttls()
                    server.login(senders, "youremailpassword")        #Senders authentication
                    message = msg.as_string()
                    server.sendmail(senders, receivers, message)

                    print (".................Email sent..............................")
                    server.quit()
                except:
                    print ("Error: unable to send email")

            except:
                print("***Error in saving data...........***")
            pass
        else:
            print("Incorrect Email")
            return generate_ticket()
    except ValueError:
        print("Invalid Id")
 #Ticket Invalidation
def ticket_invalidation(ticket_id):

    conn.execute("CREATE TABLE IF NOT EXISTS invalidtickets( \
                    t_id INTEGER PRIMARY KEY, ticket_id INTEGER, event_id INTEGER, owner_fname TEXT, owner_lname TEXT, owner_email TEXT, event_name TEXT, start_date DATE, end_date DATE, venue TEXT, FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)) ")

    print ("Invalidate Tickets")
    print ("")

    try:
        t_id = ticket_id


        conn.execute("SELECT * FROM tickets WHERE ticket_id=?",(t_id))
        items = conn.fetchall()
        cprint (tabulate(items, headers=['Ticket ID', 'Event ID','First Name','Last Name','Email', 'Event Name', 'Start Date', 'End Date', 'Venue'], tablefmt='fancy_grid'), 'cyan')
        label = input("This Ticket will be Invalidated. Type 'Y/y' to continue or 'N/n' to cancel: ")

        if label == "y" or label == "Y":

            # Transfer Data in the Tickets Table as per the ticket id
            item = conn.execute("SELECT ticket_id, event_id, owner_fname, owner_lname, owner_email, event_name, start_date, end_date, venue FROM Tickets WHERE ticket_id=?",(t_id))
            for column in item:
                num = column [0]
                eventid = column [1]
                owner_fname = column [2]
                owner_lname = column [3]
                owner_email = column [4]
                name = column [5]
                start_date = column [6]
                end_date = column [7]
                venue = column [8]
                #Copies Selected Data to invalid_tickets table
                conn.execute("INSERT INTO invalidtickets VALUES (null,?,?,?,?,?,?,?,?,?);",
                                (num, eventid, owner_fname, owner_lname, owner_email, name, start_date, end_date, venue))
                db_con.commit()
                #Delete Selected Data in the Ticket Table
                conn.execute("DELETE FROM tickets WHERE ticket_id=?", (t_id,))
                db_con.commit()
                cprint("***_______Event with ID " + t_id +" has been deleted successfully__________***", 'green')


        elif label == "n" or label == "N":
            return ticket_invalidation()
        else:
            print ("Invalid Input")

    except Exception as e:
        print("Error in updating db" + str(e))
