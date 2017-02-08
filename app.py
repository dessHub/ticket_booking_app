#!/usr/bin/env python
"""
This app uses docopt with the built in cmd module to demonstrate an interactive command application.

                    Usage:
                        app add_event <event_name>
                        app edit_event <event_id>
                        app view <table_name>
                        app delete_event <eventid>
                        app generate_ticket <event_id>
                        app ticket_invalidation <ticket_id>

                    Options:
                        -i, --interactive  Interactive Mode
                        -h, --help  Show this screen and exit.
                        --baud=<n>  Baudrate [default: 9600]
"""

import sys
import cmd
from docopt import docopt, DocoptExit
import events

from pyfiglet import Figlet, figlet_format
from termcolor import colored, cprint

frame = colored("*" * 50, 'yellow').center(80)

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print(colored("Invalid Command!", "red"))
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

def introduction():
    print(frame)
    print(frame)
    cprint(figlet_format('     EVENTS           R.S.V.P', font='colossal'),
           'green', attrs=['blink'])

    print(__doc__)
    print(frame)
    print(frame)

class MyInteractive (cmd.Cmd):
    # intro = 'Welcome to my interactive program!' \
    #     + ' (type help for a list of commands.)'
    prompt = 'add >> '
    file = None

    @docopt_cmd
    def do_add_event(self, arg):
        """Usage: add_event <event_name> """

        event_name = arg['<event_name>']
        events.add_event(event_name)

    @docopt_cmd
    def do_view(self, arg):
        """Usage: view <table_name> """
        name = arg['<table_name>']
        events.view(name)

    @docopt_cmd
    def do_delete_event(self, arg):
        """Usage: delete_event <eventid> """
        eventid = arg['<eventid>']
        events.delete_event(eventid)

    @docopt_cmd
    def do_edit_event(self, arg):
        """Usage: edit_event <event_id> """

        event_id = arg['<event_id>']
        events.edit_events(event_id)

    @docopt_cmd
    def do_generate_ticket(self, arg):
        """Usage: generate_ticket <event_id> """

        event_id = arg['<event_id>']
        events.generate_ticket(event_id)

    @docopt_cmd
    def do_ticket_validation(self, arg):
        """Usage: ticket_validation <ticket_id> """

        ticket_id = arg['<ticket_id>']
        events.ticket_validation(ticket_id)

    @docopt_cmd
    def do_ticket_invalidation(self, arg):
        """Usage: ticket_invalidation <ticket_id> """

        ticket_id = arg['<ticket_id>']
        events.ticket_invalidation(ticket_id)

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        cprint(figlet_format('....THANK YOU FOR BOOKING WITH US....\n......BYE.....', font='contessa'),
           'blue', attrs=['bold'])
        exit()

if __name__ == '__main__':
    introduction()
    try:
        MyInteractive().cmdloop()
    except KeyboardInterrupt:
        exit()
