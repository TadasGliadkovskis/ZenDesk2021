from requests.models import HTTPBasicAuth
from colorama import Fore, Style
import requests
import colorama
import math
import env
from Ticket import Ticket

colorama.init()


def print_green(string):
      print(Fore.GREEN + string + Style.RESET_ALL, end="")


def print_red(string):
      print(Fore.RED + string + Style.RESET_ALL)


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
      if status_code[0] == 5:
            print_red("Error with Server")
            return True

"""
Fetch Ticket from API using ID, turn into JSON
Create Ticket Object and return it
The program chooses what way to print it in the main menu
"""
def get_ticket_by_id(ticket_id):
      url = 'https://{}.zendesk.com/api/v2/tickets/{}.json'.format(env.SUBDOMAIN, ticket_id)
      response = requests.get(url, auth=HTTPBasicAuth(env.EMAIL, env.TOKEN))
      data = response.json()
      if not check_errors(response.status_code):
            return Ticket(data['ticket'])


def get_tickets(page_no):
      response = {}
      url = 'https://{}.zendesk.com/api/v2/tickets.json?page={}&per_page={}'.format(env.SUBDOMAIN, page_no,env.TICKETS_PER_PAGE)
      response = requests.get(url , auth=HTTPBasicAuth(env.EMAIL,env.TOKEN))
      data = response.json() 
      if not check_errors(response.status_code):
            page_through_tickets(data,page_no)
   

def get_numeric_input():
      user_input = input()
      while True:
            if user_input.isnumeric():
                  return int(user_input)
            else:
                  print(Fore.RED + "Please Enter a Number: " + Style.RESET_ALL, end="")
                  user_input = input()


"""
find out highest possible page choice
then create array of possible page choices ranging from 1 until the last.
Go through data creating ticket object and printing it.
Tell the user what page they're on and ask for them to change pages.
They can't request the page they're on or pages outside the available pages list
"""
def page_through_tickets(data, page_no):
      last_page = math.ceil(data['count'] / env.TICKETS_PER_PAGE)
      available_pages = []
      for i in range(1, last_page + 1):
            available_pages.append(i)
      
      for ticket in data['tickets']:
            print(repr(Ticket(ticket)))
      
      print("\nCurrent Page {}/{}".format(page_no,last_page))
      print_green("(0 to exit) Choose Page: ")
      user_page_choice = get_numeric_input()

      if user_page_choice == page_no:
            print_red("Already on This Page: ") 
      elif user_page_choice in available_pages:
            get_tickets(user_page_choice)
      else:
            print_red("Invalid Page\n")


if __name__ == "__main__":
      
      PROGRAM_RUN = True
      print("\nWelcome To The Ticket Viewer")
      while PROGRAM_RUN:
            
            print("\n\t1. View All Tickets")
            print("\t2. View Ticket By ID (Simple)")
            print("\t3. View Ticket By ID (Description)")
            print("\t4. Exit Ticket Viewer")
            print_green("\nChoose an option: ")
            user_option = get_numeric_input()
            if user_option in env.MENUOPTIONS:
                  if user_option == 1:
                        print("")
                        get_tickets(1)
                  elif user_option == 2:
                        print_green("Enter ID Number: ")
                        id = get_numeric_input()
                        print(repr(get_ticket_by_id(id)))
                  elif user_option == 3:
                        print_green("Enter ID Number: ")
                        id = get_numeric_input()
                        get_ticket_by_id(id).detailed_print()
                  else:
                        print("Exiting ticket viewer")
                        PROGRAM_RUN = False
            else:
                  print_red("Invalid option")