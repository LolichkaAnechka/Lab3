# Task 1.
# Write a program for selling tickets to IT-events. Each ticket has a unique number and a price. There are four types of tickets: regular ticket,
# advance ticket (purchased 60 or more days before the event), late ticket (purchased fewer than 10 days before the event) and student ticket.
# Additional information:
# -advance ticket - discount 40% of the regular ticket price;
# -student ticket - discount 50% of the regular ticket price;
# -late ticket - additional 10% to the reguler ticket price.
# All tickets must have the following properties:
# -the ability to construct a ticket by number;
# -the ability to ask for a ticket’s price;
# -the ability to print a ticket as a String.

import json
import uuid
import datetime
from dataclasses import dataclass

class NoTickestLeftError(Exception):
    def __init__(self, message):
        self.message = message


class Customer:
    __name: str
    __surname: str
    __isstudent: bool 

    def __init__(self, name, surname, isstudent):
        self.name=name
        self.surname=surname
        self.isstudent=isstudent


    @property
    def name (self):
        return self.__name


    @name.setter
    def name (self, value):
        if not isinstance(value, str):
            raise TypeError("Wrong type for 'name' atribute")
        self.__name = value


    @property
    def surname (self):
        return self.__surname


    @surname.setter
    def surname (self, value):
        if not isinstance(value, str):
            raise TypeError("Wrong type for 'surname' atribute")
        self.__surname = value


    @property
    def isstudent (self):
        return self.__isstudent


    @isstudent.setter
    def isstudent (self, value):
        if not isinstance(value, bool):
            raise TypeError("Wrong type for 'isstudent' atribute")
        self.__isstudent = value




class Event:
    def __init__(self):
        with open("1.json", encoding="utf-8") as f:
            self.date = datetime.datetime(*list(map(int, json.load(f)["event"]["date"])))

    @staticmethod
    def find_already_bought_ticket(id: str):
        with open("database1.json", "r", encoding="utf-8") as f:
            database = json.load(f)
        ticket = database['event']['bought_tickets'][id]
        print(ticket)
        

    def generate_ticket(self, customer: Customer):
        date_delta = (self.date - datetime.datetime.now()).days
        if not date_delta > 0:
            raise ValueError("Too late to buy tickets")

        with open("1.json", 'r') as f:
            event_info = json.load(f)

        numb_of_tickets = event_info["event"]["tickets"]["amount"]
        
        if  numb_of_tickets <= 0:
            raise NoTickestLeftError("Tickets sold out!")
        
        numb_of_tickets -= 1
        event_info["event"]["tickets"]["amount"] -= 1
        
        with open("1.json", 'w') as f:
            json.dump(event_info, f)
        
        if customer.isstudent:
            return Student()
        elif date_delta > 60:
            return Advanced()
        elif date_delta < 10:
            return Late()
        else:
            return Regular()

@dataclass
class Ticket():
    __id: str
    def __init__(self):
        self.id = str(uuid.uuid1())


    @property
    def id(self):
        return self.__id


    @id.setter
    def id(self, value):
        if not isinstance(value, str):
            raise TypeError("Wrong type for 'id' atribute")
        self.__id = value


class Regular(Ticket):
    __price: int
    def __init__(self) -> None:
        super().__init__()
        with open("1.json", encoding="utf-8") as f:
            self.__price = json.load(f)['event']['tickets']['regular']["cost"]
    
    def __str__(self):
        return f"Ticket: {self.id}\nPrice: {self.price}\n "

    @property
    def price(self):
        return self.__price


class Advanced(Ticket):
    __price: int
    def __init__(self) -> None:
        super().__init__()
        with open("1.json", encoding="utf-8") as f:
            self.__price = int(json.load(f)['event']['tickets']['advanced']["cost"])

    def __str__(self):
        return f"Ticket: {self.id}\nPrice: {self.price}\n "

    @property
    def price(self):
        return self.__price

class Late(Ticket):
    __price: int
    def __init__(self) -> None:
        super().__init__()
        with open("1.json", encoding="utf-8") as f:
            self.__price = int(json.load(f)['event']['tickets']['late']["cost"])

    def __str__(self):
        return f"Ticket: {self.id}\nPrice: {self.price}\n "

    @property
    def price(self):
        return self.__price


class Student(Ticket):
    __price: int
    def __init__(self) -> None:
        super().__init__()
        with open("1.json", encoding="utf-8") as f:
            self.__price = int(json.load(f)['event']['tickets']['student']["cost"])

    def __str__(self):
        return f"Ticket: {self.id}\nPrice: {self.price}\n "

    @property
    def price(self):
        return self.__price


class ImaginaryPaymentProcess:

    @staticmethod
    def buy_ticket(customer: Customer, event: Event):
        ticket = event.generate_ticket(customer)
        with open("database1.json", "r", encoding="utf-8" ) as f:
            ticket_data = json.load(f)
        if not ticket_data:
            ticket_data = {}
        if 'event' not in ticket_data:
            ticket_data['event'] = {}
        if 'bought_tickets' not in ticket_data['event']:
            ticket_data['event']['bought_tickets'] = {}
        if  str(ticket.id) not in ticket_data['event']['bought_tickets']:
            ticket_data['event']['bought_tickets'][str(ticket.id)] = {}
        ticket_data['event']['bought_tickets'][str(ticket.id)]['name'] = customer.name
        ticket_data['event']['bought_tickets'][str(ticket.id)]['surname'] = customer.surname
        ticket_data['event']['bought_tickets'][str(ticket.id)]['price'] = ticket.price
        ticket_data['event']['bought_tickets'][str(ticket.id)]['purchase_date'] = str(datetime.datetime.now())
        with open("database1.json", "w") as f:
            json.dump(ticket_data, f)


event = Event()
customer1 =  Customer("Vitaliy", "Gromyako", True)

customer2 =  Customer("Toyvo", "Zibrov", False)
z = ImaginaryPaymentProcess()
z.buy_ticket(customer1, event)
z.buy_ticket(customer2, event)

event.find_already_bought_ticket("4f876069-43d1-11ec-9548-70c94ef7cebc")