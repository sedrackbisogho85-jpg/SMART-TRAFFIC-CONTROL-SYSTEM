class Student:
    def __init__(self,name,reg_no,contact):
        self.name = name
        self.reg_no = reg_no
        self.contact = contact
        self.loan = []
        
def __str__(self):
    return(f"{self.name},{self.reg_no}")

class Book:
    catalogue = []
    def __init__(self,title,author):
        self.title = title
        self.author = author
        self.copies = []
        book.catalogue.append(self)
        
@classmethod
def all_titles(cls):
    return [b.title for b in cls.catalogue]

@staticmethod
def is_valid_isbn(isbn):
    return len(isbn.replace("-","")) in (10,13)

class Bookcopy:
    def __init__(self,copy_id,book):
        self.copy_id = copy_id 
        self.book = book
        self.is_available = True
        
def __str__(self):
    status = "available" if self.is_available else "borrowed"
    return f"{self.copy_id}:{self.book.title}({status})"

def __repr__(self):
    return f"BookCopy({self.copy_id!r},{self.book.title!r})"        
def mark_borrowed(self):
    if not self.is_available:
        raise ValueError("This copy is already borrowed")
    self.is_available = False
    
def mark_returned(self):
    if self.is_avaliable:
        raise ValueError("The copy is not borrowed.")
    self.is_available =True
    
class Loan:
    FINE_PER_DAY =1000
    def __init__(self,student,book,copy,borrow_date, due_date):
        self.student = student
        self.copy = copy
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = None

def calculate_fine(self,today):
    if today<= self.due_date:
        return 0
    days = (today-self.due_date).days
    return days*Loan.FINE_PER_DAY        
        
    
