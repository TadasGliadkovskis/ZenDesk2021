from requests.models import HTTPBasicAuth
from colorama import Fore, Style
import requests
import json
import colorama
import math
import env
from Ticket import Ticket

colorama.init()

"""
Fetch Ticket from API using ID, turn into JSON
Create Ticket Object and print out ticket
"""
def get_ticket_by_id(ticket_id):
      url = 'https://{}.zendesk.com/api/v2/tickets/{}.json'.format(env.SUBDOMAIN, ticket_id)
      response = requests.get(url, auth=HTTPBasicAuth(env.EMAIL, env.TOKEN))
      data = response.json()
      if not check_errors(response.status_code):
            print('\n'+repr(Ticket(data['ticket'])))


def get_tickets(page_no):
      response = {}
      url = 'https://{}.zendesk.com/api/v2/tickets.json?page={}&per_page={}'.format(env.SUBDOMAIN, page_no,env.TICKETS_PER_PAGE)
      response = requests.get(url , auth=HTTPBasicAuth(env.EMAIL,env.TOKEN))
      data = response.json() 
      if not check_errors(response.status_code):
            print_tickets(data)


def check_errors(status_code):
      if status_code == 200:
            return False
      print("")
      if status_code == 404:
            print_red("No Ticket with such ID")
            return True
      if status_code == 401:
            print_red("Couldn't Authenticate You")
            return True
      if status_code == 400:
            print_red("Invalid Ticked ID. Must be Number")
            return True
            

def get_numeric_input():
      user_input = input()
      while True:
            if user_input.isnumeric():
                  return int(user_input)
            else:
                  print(Fore.RED + "Please Enter a Number: " + Style.RESET_ALL, end="")
                  user_input = input()


def print_tickets(data):
      for ticket in data['tickets']:
            print(repr(Ticket(ticket)))


def print_green(string):
      print(Fore.GREEN + string + Style.RESET_ALL, end="")


def print_red(string):
      print(Fore.RED + string + Style.RESET_ALL)


if __name__ == "__main__":
      
      PROGRAM_RUN = True
      print("\nWelcome To The Ticket Viewer")
      while PROGRAM_RUN:
            
            print("\n\t1. View All Tickets")
            print("\t2. View Ticket By ID")
            print("\t3. Exit Ticket Viewer")
            print_green("\nChoose an option: ")
            user_option = get_numeric_input()
            if user_option in env.MENUOPTIONS:
                  if user_option == 1:
                        print("Fetch All")
                  elif user_option == 2:
                        print_green("Enter ID Number: ")
                        id = get_numeric_input()
                        get_ticket_by_id(id)
                  else:
                        print("Exiting ticket viewer")
                        PROGRAM_RUN = False
            else:
                  print_red("Invalid option")