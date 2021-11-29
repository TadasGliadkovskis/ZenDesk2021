from datetime import datetime
from colorama import Fore, Style
import colorama
colorama.init()

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
            
