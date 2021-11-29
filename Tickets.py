from requests.models import HTTPBasicAuth
from colorama import Fore, Style
from datetime import datetime
import requests
import json
import colorama
import math
import env
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
            print(repr(Ticket(data['ticket'])))


def get_tickets(page_no):
      response = {}
      url = 'https://{}.zendesk.com/api/v2/tickets.json?page={}&per_page={}'.format(env.SUBDOMAIN, page_no,env.TICKETS_PER_PAGE)
      response = requests.get(url , auth=HTTPBasicAuth(env.EMAIL,env.TOKEN))
      data = response.json() 
      if not check_errors(response.status_code):
            print_tickets(data)


def print_tickets(data):
      for ticket in data['tickets']:
            print(repr(Ticket(ticket)))


def check_errors(status_code):
      if status_code == 200:
            return False
      if status_code == 404:
            print(Fore.RED + "No Ticket with such ID" + Style.RESET_ALL)
            return True
      if status_code == 401:
            print (Fore.RED + "Couldn't Authenticate You" + Style.RESET_ALL)
            return True
      if status_code == 400:
            print(Fore.RED + "Invalid Ticked ID. Must be Number" + Style.RESET_ALL)
            return True
            

class Ticket():
      def __init__(self,ticket):
            self.status = ticket['status']
            self.id = ticket['id']
            self.subject = ticket['subject']
            self.description = ticket['description']
            self.requester_id = ticket['requester_id']
            self.created_at = self.extract_time(ticket['created_at'])

      """
      Displays ticket in this format
      Status  ID         Subject            Requester ID          Date Created
      0       ID: 111   'Lunch Soon ?     ' Requester 2871351 on 01-Dec-2021 09:46 PM    
      """
      def __repr__(self):
            status_letter = self.get_status_color()
            ticket_string = "{0} ID: {1:<5} '{2:<50}' Requester {3:<5} on {4:<5}".format(status_letter,self.id,self.subject,self.requester_id,self.created_at)
            return ticket_string
      
      """
      Transforms string into datetime object 
      which allows for prettier formatting
      """
      def extract_time(self,time_string):
            date_object = datetime.strptime(time_string,"%Y-%m-%dT%H:%M:%SZ")
            return date_object.strftime("%d-%b-%Y %I:%M %p")

      """
      When printing tickets
      give the first letter of the status field
      and attach a color
      """
      def get_status_color(self):
            status_letter = self.status[0].upper()
            if self.status == "open":
                  return Fore.RED + status_letter + Style.RESET_ALL
            elif self.status == "new":
                  return Fore.BLUE + status_letter + Style.RESET_ALL
            elif self.status == "closed" or self.status == "solved":
                  return Fore.GREEN + status_letter + Style.RESET_ALL
            elif self.status == "pending" or self.status == "hold":
                  return Fore.YELLOW + status_letter + Style.RESET_ALL
            

def get_numeric_input():
      user_input = input()
      if user_input.isnumeric():
            return int(user_input)
      else:
            return user_input


if __name__ == "__main__":
      MenuOptions = [1,2,3]
      PROGRAM_RUN = False
      print("\nWelcome To The Ticket Viewer")
      while PROGRAM_RUN:
            
            print("\n\t1. View All Tickets")
            print("\t2. View Ticket By ID")
            print("\t3. Exit Ticket Viewer")
            print(Fore.GREEN + "Choose an option:" + Style.RESET_ALL, end=" ")
            user_option = get_numeric_input()
            if user_option in MenuOptions:
                  print("Valid")
                  if user_option == 1:
                        print("Fetch All")
                  elif user_option == 2:
                        id = input("Enter ID number: ")
                        get_ticket_by_id(id)
                  else:
                        print("Exiting ticket viewer")
                        break
            else:
                  print(Fore.RED + "Invalid option" + Style.RESET_ALL)
            print(user_option)