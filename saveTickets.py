import requests
from requests.models import HTTPBasicAuth
import json
import colorama
from colorama import Fore, Style
colorama.init()

#curl https://zcctadas.zendesk.com/api/v2/tickets.json -v -u tadas2410@gmail.com:tRNhWPBeGc2hm7u! get JSON TICKETS
def get_one_ticket(ticket_id):
      response = requests.get('https://zcctadas.zendesk.com/api/v2/tickets/{}.json'.format(ticket_id),auth=HTTPBasicAuth('tadas2410@gmail.com','tRNhWPBeGc2hm7u!'))
      data = response.json()
      print(response)
      if not check_errors(data):
            print(repr(Ticket(data['ticket'])))


def get_url():
      page_no = 1
      response = {}

      response = requests.get('https://zcctadas.zendesk.com/api/v2/tickets.json',auth=HTTPBasicAuth('tadas2410@gmail.com','tRNhWPBeGc2hm7u!'))
      data = response.json()
      
      if not check_errors(data):
            for ticket in data['tickets']:
                  print(repr(Ticket(ticket)))


def check_errors(response):
      if 'error' in response:
            print(response['error'])
            return True #error does exist
            
class Ticket():
      def __init__(self,ticket):
            self.status = ticket['status']
            self.id = ticket['id']
            self.subject = ticket['subject']
            self.description = ticket['description']
            self.requester_id = ticket['requester_id']
            self.created_at = ticket['created_at']


      def __repr__(self):
            status_letter = self.get_status_color()
            #O ID: 1 "Help with x" requested by 2131231 on
            rep = "{} ID: {} '{}' requested by {} on {}".format(status_letter,self.id,self.subject,self.requester_id,self.created_at)
            return rep
      
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
            



if __name__ == "__main__":
      get_url()