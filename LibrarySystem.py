#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 08:23:29 2024

@author: chiarafischer
"""

from dataclasses import dataclass
from datetime import datetime, timedelta

# define dataclass Media, which defines relevant characteristics of general Media, such as movies, books, songs,...
@dataclass
class Media:
    _title: str
    _author: str
    _genre: str
    _publication_year: int

# Forward declaration for Review class: To address the circular dependency issue where Review class references Book class and vice versa, we use a forward declaration (move the class definitions to separate modules)
class Review:
    pass
    
# Define class for Books (immutable class). This class inheritates from the Media-Dataclass and extends its functionality
class Book(Media): 
    __slots__ = ["_title", "_author", "_genre", "_publication_year", "reviews"] # define slots (names for attributes for objects of this class) for memory advantage
    
    # Constructor inhertitates the constructor from the parent class Media and adds list of reviews for that book
    def __init__(self, title, author, publication_year, genre):
        super().__init__(title, author, genre, publication_year)
        self.reviews = []  # List to store reviews for the book
     
    # destructor, in case the book is no longer available at the libary
    def __del__(self): 
        print ("Book has been deleted from the system")

    # Define properties to allow defining getter, setter, and deleter methods for accessing, modifying, and deleting attributes as if they were ordinary instance attributes (more user-friendly)
    @property 
    def title(self): # get title
        return self._title
    
    @property
    def author(self): # get author
        return self._author
     
    @property
    def genre(self): # get genre
        return self._genre

    @property
    def publication_year(self): # get publication year
        return self._publication_year
    
    # Function for adding reviews for a specific book. A review can only be added once a member returns that specific book (see in function return_book in Library Class)
    def add_review(self, member, rating, comment):
        new_review = Review(self, member, rating, comment)
        self.reviews.append(new_review)
        
    # As instances of the Book Class will be used as keys of a dictionary in the Library Class. Built-in types in Python are hashable by default, whereas, for custom classes, we are ensuring that they are hashable by implementing the __hash__() method and the __eq__() method to define the object's hash value and equality comparison respectively
    # Compute a hash value based on the title and author attributes of a Book object
    def __hash__(self):
        return hash((self.title, self.author))
    
    # Returns True if the other object is an instance of the Book class and if both the title and author attributes of the two Book objects are the same
    def __eq__(self, other):
        return isinstance(other, Book) and self.title == other.title and self.author == other.author

    # Display the reviews for a book
    def display_reviews(self):
        print(f"Reviews for {self.title} by {self.author}:")
        for review in self.reviews:
            print(f"Rating: {review._rating}")
            print(f"Comment: {review._comment}")
            print(f"Reviewed by: {review._member.name}")
            print()

    # displays the details of the book, apart from its reviews
    def display_details(self): 
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Genre: {self.genre}")
        print(f"Publication Year: {self.publication_year}")
        print()



# Class for creating objects of members within a library
class Member: 
    __slots__ = ["__name", "__membership_id"] # define slots (names for attributes for objects of this class) for memory advantage
    
   # Constructor with private attributes to protect member's privacy
    def __init__(self, name, membership_id): 
        self.__name = name
        self.__membership_id = membership_id
        
    # Destructor, in case the member cancels its membership at the libary
    def __del__(self): 
        print (f"Member {self.__name} with ID {self.__membership_id} is no longer a library member.")
        
    def borrow_book(self, book):
        print(f"The Book {book.title} by {book.author} got lended by {self.__name} with ID {self.__membership_id}.")

    def return_book(self, book):
        print(f"The Book {book.title} by {book.author} got returned by {self.__name} with ID {self.__membership_id}.")
    
    # Define properties to allow defining getter, setter, and deleter methods for accessing, modifying, and deleting attributes as if they were ordinary instance attributes (more user-friendly)
    @property
    def name(self):
        return self.__name
    
    @property
    def memberID(self):
        return self.__membership_id
    
    # In case the initial member ID given as an input is already used within the library system, a new member ID is assigned to the new member
    def change_memberID(self, newID):
        self.__membership_id = newID

    # Display member details
    def display_details(self):
        print(f"Name: {self.name}")
        print(f"Membership ID: {self.memberID}")
        print()


# Now, after Book Class, finish defining the Review class, which now can use the Book class as well
@dataclass
class Review:
    _book: Book
    _member: 'Member'
    _rating: int
    _comment: str
    

# Class for Reservations made within the library (meaning, a book is being lended out to a member)
class Reservation:
    def __init__(self, book,member, date):
        self.book = book
        self.member = member
        self.date = date
        
        
        
# Fine Management System for capturing delayed book returns
class FineManagementSystem:  
    
    # Constructor, defining the fine rate per day (2 if not defined) and a dictionary for storing all unpaid fines 
    def __init__(self, fine_rate_per_day = 2):
        self.fine_rate_per_day = fine_rate_per_day
        self.fines = {}  # Dictionary to store fines for each member using their memberID as key

    # Calculate fine for new delayed return
    def calculate_fine(self, return_date, reservation): # Calculate the difference in days between the return date and the due date
        due_date = datetime.strptime(reservation.date, '%Y-%m-%d') + timedelta(days = 60) # by default, the customer has 60 days to return the book
        return_date = datetime.strptime(return_date, '%Y-%m-%d')
        days_overdue = (return_date - due_date).days
        if days_overdue <= 0:
            return 0  # No fine if the book is returned on or before the due date
        else:
            return days_overdue * self.fine_rate_per_day

    # add fine to the list of fines stored
    def add_fine(self, reservation, fine_amount):
        member_id = reservation.member.memberID
        if member_id in self.fines:
            self.fines[member_id] += fine_amount
        else:
            self.fines[member_id] = fine_amount

    # Return the fine amount for the member, or 0 if no fine exists
    def get_fine(self, reservation):
        return self.fines.get(reservation.memberID, 0)  

    # Print all unpaid fines
    def print_fines(self):
        for key, value in self.fines():
            print(key, ":", value)
            
    # Member pays a specific amount in order to pay for a fine
    def pay_fine(self, member, amount):
        if member.memberID in self.fines:
            if self.fines[member.memberID] == 0:
                print("That member has no fine to pay.")
            elif self.fines[member.memberID] < amount:
                print(f"The fine of {self.fines[member.memberID]} has been paid, and the remaining money of {amount - self.fines[member.memberID]} has been returned to the member.")
                self.fines[member.memberID] = 0
            else: 
                print(f"{member.name} paid the fine of {amount}.")
                self.fines[member.memberID] -= amount
            

# Class for library, which will be interacting with the other classes
# The user will only have to interact with the library class
class Library: 
    
    __slots__ = ["collection", "reservations", "members", "fine_system"] # define slots (names for attributes for objects of this class) for memory advantage

    # Constrcutor of the class
    def __init__(self):
        self.collection = {} # this dictionary stores the registered books as a key and their available exemplars as their values
        self.reservations = []
        self.members = []
        self.fine_system = FineManagementSystem(fine_rate_per_day = 3)

    # add new book to the library
    def add_book(self, book):
        if book.title in self.collection:
            self.collection[book] += 1
            print(f"One more exemplar of the book {book.title} by {book.author} has been added to the library.")
        else:      
            self.collection[book] = 1
            print(f"The book {book.title} by {book.author} has been added to the library for the first time.")
        print()

    # find all reservations for ine book 
    def res_for_book(self, book):
        reservations = []
        for i in self.reservations:
            if i.book == book:
                reservations.append(i)
        return reservations
                
    # find all reservations for one member
    def res_for_member(self, member):
        reservations = []
        for i in self.reservations:
            if i.memberID == member.memberID:
                reservations.append(i)
        return reservations

    # check whether an inputted memberID is valid
    def is_validID(self, member):
        valid = True
        for i in self.members:
            thisID = i.memberID
            if thisID == member.memberID:
                valid = False
        return valid
    
    # generate a new member ID 
    def generate_ID(self):
        maxID = 0
        for i in self.members:
            thisID = i.memberID
            if thisID > maxID:
                maxID = thisID
        maxID = maxID + 1
        print(f"The ID of the new member is already present in the system. Therefore, the new ID {maxID} was assigned to the new member.") 
        return maxID
        
    # add new member to the library
    def add_member(self, member): 
        valid = self.is_validID(member)
        newID = member.memberID
        print(f"The member with ID {newID} is attempted to be added to the system.")
        if not valid: # generate new member ID if the given one is invalid (meaning already registered in the library system)
            newID = self.generate_ID()
            member.change_memberID(newID)
        self.members.append(member)
        print("The member now got successfully added to the system.")
        print()
        
    # remove a member
    # maybe add return book for all reservations here?
    def remove_member(self, member):
        print(f"Member of name {member.name} and ID {member.memberID} is attempted to be deleted from the system.")
        if member in self.members:
            self.members.remove(member)
            reservations = self.res_for_member(member) 
            for i in reservations: # remove all registered reservations of that member
                self.reservations.remove(i)   
            member.__del__() # destroy the member object
            print("The member now got successfully removed from the system.")
        else:
            print("Member can not be removed as it does not exist in the library system.")
    
    # remove a book, meaning it is being made unavailable
    def unregister_book(self, book):
        print(f"Book of title {book.title} by {book.author} is attempted to be deleted from the system.")
        if book in self.collection: 
            print("Book was deleted from the libary portfolio.")
            self.collection.pop(book)
            reservations = self.res_for_book(book)
            for i in reservations: # remove all reservations of that book as well
                self.reservations.remove(i)
        else:      
            print("Book is already unavailable in the library.")

    # display all books in a tabular fashion; if filterAvailable = True, only all available books (meaning all books for which the library has at least one in stock) are being displayed
    def display_all_books(self, filterAvailable = False):
        print("All Books:")
        print()
        print("{:<40} {:<30} {:<20} {:<15}".format("Title", "Author", "Publication Year", "Available Copies"))
        for book, count in self.collection.items():
            if filterAvailable and count > 0 or not filterAvailable: 
                print("{:<40} {:<30} {:<20} {:<15}".format(book.title, book.author, book.publication_year, count))
        print()
        
    # display all available books
    def display_available_books(self):
        print("Available Books:")
        print()
        self.display_all_books(True)
            
    # display all members
    def display_all_members(self):
        print("All Members:")
        print()
        for member in self.members:
            member.display_details()
        print()
        
    # lend a book (create a reservation)
    def lend_book(self, member, book, date): # add date as '2024-05-15'
        print(f"Member with name {member.name} and ID {member.memberID} is trying to lend the book {book.title} by {book.author}.")
        if(datetime.strptime(date, '%Y-%m-%d') > datetime.now()):
            print("However, the date of lending is not valid. Therefore, the process was not successfull.")
        else:
            if book not in self.collection:
                print("However, the book is not registered in the library and therefore not available. Therefore, the process was not successful.")
            else:
                quantity = self.collection[book]
                if(quantity == 0):
                    print("All of these available books are lended out aready. Therefore, the process was not successful.")
                else:
                    new_res = Reservation(book, member, date)
                    self.reservations.append(new_res)
                    self.collection[book] -= 1
                    member.borrow_book(book)

    # member returns a book
    def return_book(self, return_date, reservation):
        print(f"Member {reservation.member.memberID} is attempting to return the book {reservation.book.title} by {reservation.book.author} on the {return_date}")
        if reservation.book not in self.collection:
            print("Book was not lended here or is no longer registered in the system. Therefore, the process was not successful.")
        else:
            self.collection[reservation.book] += 1
            
            # calculate fine 
            fine = self.fine_system.calculate_fine(return_date, reservation)
            if(fine > 0):
                print(f"A fine of {fine} Euros is being charged.")
                self.fine_system.add_fine(reservation, fine)
            reservation.member.return_book(reservation.book)
            
            # Prompt for review rating and comment
            review_rating = int(input("Please rate the book (1-5): "))
            review_comment = input("Please provide a comment about the book: ")

            # Add review for the returned book
            reservation.book.add_review(reservation.member, review_rating, review_comment)
            print("Thank you for your review!")
            
    # display all unpaid fines
    def display_fines(self):
        self.fine_system.print_fines()
        
    # a member pays back a fine
    def pay_fine(self, member, amount):
        self.fine_system.pay_fine(member, amount)
    
    # display all reviews for all books 
    def display_reviews(self):
        for book in self.collection:
            book.display_reviews()
        
        
        
  
        
# Example usage
library = Library()

# Adding books
book1 = Book("1984", "George Orwell", 1949, "Dystopian")
book3 = Book("1984", "George Orwell", 1949,"Dystopian")
book2 = Book("To Kill a Mockingbird", "Harper Lee", 1960, "Fiction")
library.add_book(book1)
library.add_book(book2)
library.add_book(book3)

# Adding members
member1 = Member("Alice", 1)
member2 = Member("Bob", 2)
member3 = Member("Chiara", 2)
library.add_member(member1)
library.add_member(member2)
library.add_member(member3)

# Display all books and the number of their exemplars
library.display_all_books()

# Display available books
library.display_available_books()

# Members borrow a book successfully
library.lend_book(member1, book1, '2024-02-24')
library.lend_book(member2, book1, '2024-02-24')

# Members borrow a book unsuccessfully
library.lend_book(member3, book1, '2024-02-24')

# Member returns a book without a fee
library.return_book('2024-03-04', Reservation(book1,member1, '2024-02-24'))

# Member returns a book with a fee
library.return_book('2024-06-24', Reservation(book2,member2, '2024-02-24'))

# Member pays fine
library.pay_fine(member2,80)
library.pay_fine(member2,40)
library.pay_fine(member2,200)

# Display all members
#library.display_all_members()
library.display_reviews()

library.display_all_books()
library.display_available_books()

