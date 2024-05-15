#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 14:25:26 2024

@author: chiarafischer
"""

############################################################
# Business Case:
# Traditional library systems often face challenges in managing resources effectively, 
# tracking book availability, and providing seamless member services. Manual processes 
# lead to inefficiencies, delayed responses, and limited access to library services.

# Building on this, our library management system offers a comprehensive solution 
# to address these challenges. Key features include: 
#   1. Resource Management: Centralized cataloging of books, enabling easy 
#      tracking of inventory, circulation, and availability status
#   2. Member Management: Efficient member registration and account management,
#      facilitating seamless borrowing and return processes.
#   3. Search and Discovery: Intuitive search functionality, enabling users to 
#      quickly get an overview of the current status of the library
#   4. Fine Management: Automated fine calculation and payment processing, ensuring 
#      fair and transparent handling of overdue items and fines.
#   5. Review System: Management of Reviews for books given by its users, enabling
#      the library to get insights into user preferences that can be used for 
#      future inventory decisions
    
# The user will only interact with one single class - the library class. The rest
# is handled by the class interactions as defined.
    
############################################################

# Loading necessary libraries 
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
    
# Define class for Books. This class inheritates from the Media-Dataclass and extends its functionality
class Book(Media): 
    __slots__ = ["_title", "_author", "_genre", "_publication_year", "_reviews"] # define slots (names for attributes for objects of this class) for memory advantage
    
    # Constructor inhertitates the constructor from the parent class Media and adds list of reviews for that book
    def __init__(self, title, author, publication_year, genre):
        super().__init__(title, author, genre, publication_year)
        self._reviews = []  # List to store reviews for the book
     
    # destructor, in case the book is no longer available at the libary
    def __del__(self): 
        print ("The book has been deleted from the system")

    # Define properties to allow defining getter methods for accessing the protected attributes of this class as if they were ordinary instance attributes (more user-friendly)
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
        self._reviews.append(new_review)
        
    # Instances of the Book Class will be used as keys of a dictionary in the Library Class. Built-in types in Python are hashable by default, whereas, for custom classes, we are ensuring that they are hashable by implementing the __hash__() method and the __eq__() method to define the object's hash value and equality comparison respectively
    # Compute a hash value based on the title and author attributes of a Book object
    def __hash__(self):
        return hash((self.title, self.author))
    
    # Returns True if the other object is an instance of the Book class and if both the title and author attributes of the two Book objects are the same
#    def __eq__(self, other):
 #       return isinstance(other, Book) and self.title == other.title and self.author == other.author

    # Display the reviews for a book
    def display_reviews(self):
        print(f"Reviews for {self.title} by {self.author}:")
        for review in self._reviews:
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



# Class for Members of a library
class Member: 
    __slots__ = ["__name", "__membership_id"] # define slots (names for attributes for objects of this class) for memory advantage
    
   # Constructor with private attributes to protect member's privacy
    def __init__(self, name, membership_id): 
        self.__name = name
        self.__membership_id = membership_id
        
    # Destructor, in case the member cancels its membership at the libary
    def __del__(self): 
        print (f"Member {self.__name} with ID {self.__membership_id} is no longer a library member.")
        
    # Output in case the member borrows a book
    def lend_book(self, book):
        print(f"The Book {book.title} by {book.author} got lended by {self.__name} with ID {self.__membership_id}.")

    # Output in case the member returns a book
    def return_book(self, book):
        print(f"The Book {book.title} by {book.author} got returned by {self.__name} with ID {self.__membership_id}.")
    
    # Define properties to allow defining getter methods for accessing attributes as if they were ordinary instance attributes (more user-friendly)
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
    def __init__(self, book,member, reservation_date):
        self.book = book
        self.member = member
        self.date = reservation_date
        self.due_date = datetime.strptime(reservation_date, '%Y-%m-%d') + timedelta(days = 60) # by default 60 days to return the book before a fine is being charged
    
    # Returns True if the other object is an instance of the Reservation class and if all their attributes are the same; this function makes sure that, when a Reservation-object is defined and the library is searched for the existence of that reservation, it can be found by comparing attributes
    def __eq__(self, other):
        if isinstance(other, Reservation):
            # Compare all attributes for equality
            return (self.book == other.book and
                    self.member == other.member and
                    self.date == other.date and
                    self.due_date == other.due_date)
        return False
        
        
        
# Fine Management System for capturing delayed book returns
class FineManagementSystem:  
    
    # Constructor, defining the fine rate per day (2 if not defined) and a dictionary for storing all unpaid fines 
    def __init__(self, fine_rate_per_day = 2):
        self.fine_rate_per_day = fine_rate_per_day
        self.fines = {}  # Dictionary to store fines for each member using their memberID as key

    # Calculate fine for new delayed return
    def calculate_fine(self, return_date, reservation): # Calculate the difference in days between the return date and the due date
        return_date = datetime.strptime(return_date, '%Y-%m-%d')
        days_overdue = (return_date - reservation.due_date).days
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
                print(f"{member.name} has no fine to pay.")
            elif self.fines[member.memberID] < amount:
                print(f"{member.name}'s fine of {self.fines[member.memberID]} has been paid, and the remaining money of {amount - self.fines[member.memberID]} has been returned to {member.name}.")
                self.fines[member.memberID] = 0
            else: 
                self.fines[member.memberID] -= amount
                print(f"{member.name} paid the fine of {amount}. Remaining amount: {self.fines[member.memberID]}.")
                
    # expand the deadline for the book return for a given reservation
    def expand_deadline(self, reservation, new_date):
        if(datetime.strptime(new_date, '%Y-%m-%d') < reservation.due_date):
            print("The new date is invalid. Choose a date that extends the previous deadline.")
        else:
            reservation.due_date = new_date
            print(f"{reservation.member.name} now has more time to return the book {reservation.book.title}.")
            

# Class for library, which will be interacting with the other classes
# The user will only have to interact with the library class
class Library: 
    
    __slots__ = ["collection", "reservations", "members", "fine_system"] # define slots (names for attributes for objects of this class) for memory advantage

    # Constructor of the class
    def __init__(self):
        self.collection = {} # this dictionary stores the registered books as a key and their available exemplars as their values
        self.reservations = []
        self.members = []
        self.fine_system = FineManagementSystem(fine_rate_per_day = 3)

    # find all reservations for one book 
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
            if i.member.memberID == member.memberID:
                reservations.append(i)
        return reservations

    # check whether an given memberID is valid
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
        minID = 10000
        newID = maxID
        for i in self.members:
            thisID = i.memberID
            if thisID > maxID:
                maxID = thisID
            if thisID < minID:
                minID = thisID
        if minID > 1:
            newID = minID - 1
        else:
            newID = maxID + 1
        print(f"The ID of the new member is already present in the system. Therefore, the new ID {newID} was assigned to the new member.") 
        return newID
        
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
        
    # add new book to the library
    def add_book(self, book):
        if book in self.collection:
            self.collection[book] += 1
            print(f"One more exemplar of the book {book.title} by {book.author} has been added to the library.")
        else:      
            self.collection[book] = 1
            print(f"The book {book.title} by {book.author} has been added to the library for the first time.")
        print()
        
    # remove a member
    def remove_member(self, member):
        print(f"Member of name {member.name} and ID {member.memberID} is attempted to be deleted from the system.")
        if member in self.members:
            reservations = self.res_for_member(member)
            if len(reservations) > 0:
                print(f"Member can not be removed. {len(reservations)} books still need to be returned by that member.")
            else:
                self.members.remove(member)
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
            book.__del__() # destroy the book object
        else:      
            print("Book is not registered in the library and can't be deleted.")
        
    # lend a book (create a reservation)
    def lend_book(self, member, book, date): # add date as '2024-05-15'
        print(f"{member.name} with ID {member.memberID} is trying to lend the book {book.title} by {book.author}.")
        if(datetime.strptime(date, '%Y-%m-%d') > datetime.now()):
            print("However, the date of lending is not valid. Therefore, the process was not successfull.")
        else:
            if book not in self.collection:
                print("However, the book is not registered in the library and therefore not available. Therefore, the process was not successful.")
            else:
                quantity = self.collection[book]
                if(quantity == 0):
                    print("However, all of these available books are lended out aready. Therefore, the process was not successful.")
                else:
                    new_res = Reservation(book, member, date)
                    self.reservations.append(new_res)
                    self.collection[book] -= 1
                    member.lend_book(book) # the member class has a method of the same name. As this method is applied to a member object, the function of the member class is used here, instead of the function of the library class
                    
    # create a review for book
    def create_review(self, reservation):
        while True:
            review_rating = int(input("Please rate the book (1-5): "))
            if 1 <= review_rating <= 5:
                break
            else:
                print("Invalid rating. Please enter a number between 1 and 5.")
        review_comment = input("Please provide a comment about the book: ")
        
        reservation.book.add_review(reservation.member, review_rating, review_comment)
        print("Thank you for your review!")


    # member returns a book
    def return_book(self, return_date, reservation):
        print(f"{reservation.member.name} is attempting to return the book {reservation.book.title} by {reservation.book.author} on the {return_date}")
        if reservation.book not in self.collection or reservation not in self.reservations:
            print("Book was not lended here or is no longer registered in the system. Therefore, the process was not successful.")
        else:
            self.collection[reservation.book] += 1
            self.reservations.remove(reservation) # remove reservation from listed reservations
            # calculate fine 
            fine = self.fine_system.calculate_fine(return_date, reservation)
            if(fine > 0):
                print(f"A fine of {fine} Euros is being charged.")
                self.fine_system.add_fine(reservation, fine)
            reservation.member.return_book(reservation.book) # the member class has a method of the same name. As this method is applied to a member object, the function of the member class is used here, instead of the function of the library class
            
            # Prompt for review rating and comment
            self.create_review(reservation)
    
    # a member pays back a fine
    def pay_fine(self, member, amount):
        self.fine_system.pay_fine(member, amount)
    
    # extend the deadline for returning a book before a fine is being charged
    def expand_deadline(self,reservation, date):
        if reservation not in self.reservations:
            print("The reservation does not exist. Therefore, the deadline can not be extended.")
        else:
            self.fine_system.expand_deadline(reservation,date)
            
    # display all members
    def display_all_members(self):
        print("All Members:")
        print()
        for member in self.members:
            member.display_details()
        print()
            
    # display all unpaid fines
    def display_fines(self):
        print("All Fines:")
        print()
        self.fine_system.print_fines()
        print()
    
    # display all reviews for all books 
    def display_reviews(self):
        for book in self.collection:
            book.display_reviews()
            
    def display_books(self, title=None, author=None, publication_year=None, genre=None, just_available_books = False):
    
        # Print the title of the output depending on the filters applied
        filters = []
        if title:
            filters.append(f"title '{title}'")
        if author:
            filters.append(f"author '{author}'")
        if publication_year:
            filters.append(f"publication year '{publication_year}'")
        if genre:
            filters.append(f"genre '{genre}'")
        if just_available_books:
            title_prefix = "All books with" if just_available_books else "All books"
            filters.append("available copies")
        else:
            title_prefix = "All books with" if filters else "All Books:"
        
        if filters:
            print(title_prefix, ", ".join(filters) + ":")
        else:
            print(title_prefix)


        print("{:<40} {:<30} {:<20} {:<15}".format("Title", "Author", "Publication Year", "Available Copies"))
        empty = True
        # gather the books that fulfill the given filters
        for book, count in self.collection.items():
            
            # Check if the book is available if just_available_books is True
            if just_available_books and count < 1:
                continue
        
            # Check if the book matches the filter criteria
            if (title is None or book.title == title) and \
               (author is None or book.author == author) and \
               (publication_year is None or book.publication_year == publication_year) and \
               (genre is None or book.genre == genre):
                   empty = False
                   print("{:<40} {:<30} {:<20} {:<15}".format(book.title, book.author, book.publication_year, count))
        if empty:
            print("{:<40} {:<30} {:<20} {:<15}".format("None", "None", "None", "None"))
        
  
        
# Example usage
library = Library()

# Adding books
book1 = Book("1984", "George Orwell", 1949, "Dystopian")
book3 = Book("1984", "George Orwell", 1949,"Dystopian")
book2 = Book("To Kill a Mockingbird", "Harper Lee", 1960, "Fiction")
library.add_book(book1)
library.add_book(book2)
library.add_book(book3)

# Print filtered and unfiltered inventory
library.display_books(title="1984")
library.display_books()

# Adding members
member1 = Member("Alice", 1)
member2 = Member("Bob", 2)
member3 = Member("Chiara", 2)
library.add_member(member1)
library.add_member(member2)
library.add_member(member3)

# Members borrow a book successfully
library.lend_book(member1, book1, '2024-02-24')
library.lend_book(member2, book1, '2024-02-24')

# Display available books
library.display_books(just_available_books=True)

# extends deadline for returning the book
library.expand_deadline(Reservation(book1, member1, '2024-02-24'), '2025-02-24')

# Members borrow a book unsuccessfully
library.lend_book(member3, book1, '2024-02-24')

# Remove member (unsuccesfully)
library.remove_member(member1)


# Member returns a book without a fee
library.return_book('2024-03-04', Reservation(book1,member1, '2024-02-24'))

# Remove member (succesfully)
library.remove_member(member1)

# Display all members
library.display_all_members()

# display current reservations
library.current_reservation()

# Member returns a book with a fee
library.return_book('2024-06-24', Reservation(book1,member2, '2024-02-24'))

# Member pays fine
library.pay_fine(member2,80)
library.pay_fine(member2,40)
library.pay_fine(member2,200)

# Display current status of the library
library.display_all_members()
library.display_reviews()
