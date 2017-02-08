# ticket_booking_app

#User Can:

  1. Add, edit and delete events
  2. View Registered events and tickets
  3. Generate/R.S.V.P ticket
  4. Cancel ticket
  5. Receive email after successfully generating ticket.

#Technologies Used:

  1. Python 2.7
  2. flask
  3. Docopt
  4. Figlet
  5. Termcolor
  6. sqlite3

# How to use it.

  1. `$ git clone https://github.com/dessHub/ticket_booking_app.git

  2. `$ cd ticket_booking_app`

  3. Create and activate a virtual environment.

         '$ virtualenv flask'

  4. Activate virtual environment

         '$ source .env/bin/activate'

  5. Install dependencies

         `$ pip install -r requirements.txt`

  6. Set your email Address and password at events.js file

      '''
      
        def generate_ticket(eventid):
            -----
            senders = "youremailaccount"      #Senders Email Address
            msg = MIMEMultipart()
            msg['From'] = senders
            msg['To'] = receivers
            msg['Subject'] = "Ticket Booking"

          ------
             try:
               -----
               server.login(senders, "youremailpassword")
               -------

          '''

  7. Run the application

      'python app.py'


 #Usage

 ```
    app add_event <event_name>
    app edit_event <event_id>
    app delete_event <eventid>
    app view <table_name>
    app generate_ticket <event_id>
    app ticket_invalidation <ticket_id>

```
