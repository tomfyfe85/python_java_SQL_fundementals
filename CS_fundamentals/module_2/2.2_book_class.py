t"""
Exercise 2.2: Book Class

Create a Book class for a library system with checkout and return functionality.

REQUIREMENTS:

Class: Book

Attributes:
- title (str): Book title
- author (str): Book author
- isbn (str): 13-digit ISBN
- available (bool): Whether book is available

Methods:
- __init__(title, author, isbn): Constructor (book starts as available)
- checkout(): Mark book as checked out
- return_book(): Mark book as returned
- is_available(): Return availability status
- __str__(): Return string representation

Validation Rules:
- Title cannot be empty
- Author cannot be empty
- ISBN must be exactly 13 digits
- Cannot checkout a book that's already checked out
- Cannot return a book that's not checked out

EXAMPLES:

book = Book("1984", "George Orwell", "9780451524935")
print(book)  # '1984' by George Orwell [Available]

book.checkout()
print(book.is_available())  # False
print(book)  # '1984' by George Orwell [Checked Out]

book.checkout()  # ValueError: Book is already checked out

book.return_book()
print(book.is_available())  # True

YOUR TASK:
1. Use UMPIRE to plan your approach
2. Implement the Book class with all required methods
3. Add comprehensive validation and error handling
4. Test with the provided test cases
"""

# ==========================================
# YOUR CODE GOES BELOW
# ==========================================

class Book:
    title: str
    author: str
    isbn: str

    def __init__(self, title, author, isbn):
        if title == "":
            raise ValueError('Enter a title')
        if author == "":
            raise ValueError('Enter an author')
        if len(isbn) != 13 or not isbn.isnumeric():
            raise ValueError('Isbn must be 13 digits')
        
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        
    def checkout(self):
        if not self.available:
            raise ValueError('Book is not available')
        self.available = False
    
    def return_book(self):
        if self.available:
            raise ValueError('Book is not checked out')
        self.available = True
        
    def is_available(self):
        return(self.available)
    
    def __str__(self):
        return(f"'{self.title}' by {self.author} [{'Available' if self.available else 'Checked out'}]")
# ==========================================
# TEST CASES
# ==========================================

if __name__ == "__main__":
    print("=== Testing Book Creation ===")

    book1 = Book("1984", "George Orwell", "9780451524935")
    print(book1)  # '1984' by George Orwell [Available]

    book2 = Book("To Kill a Mockingbird", "Harper Lee", "9780061120084")
    print(book2)  # 'To Kill a Mockingbird' by Harper Lee [Available]

    print("\n=== Testing Checkout ===")
    print(f"Book 1 available? {book1.is_available()}")  # True

    book1.checkout()
    print(f"After checkout, available? {book1.is_available()}")  # False
    print(book1)  # '1984' by George Orwell [Checked Out]

    print("\n=== Testing Return ===")
    book1.return_book()
    print(f"After return, available? {book1.is_available()}")  # True
    print(book1)  # '1984' by George Orwell [Available]

    # print("\n=== Testing Error Handling ===")

    # Test empty title
    try:
        bad_book = Book("", "Author Name", "9780451524935")
        print("❌ FAIL: Should raise ValueError for empty title")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # # Test empty author
    try:
        bad_book = Book("Book Title", "", "9780451524935")
        print("❌ FAIL: Should raise ValueError for empty author")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # # Test invalid ISBN (too short)
    try:
        bad_book = Book("Book Title", "Author Name", "123")
        print("❌ FAIL: Should raise ValueError for invalid ISBN")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # # Test invalid ISBN (not all digits)
    try:
        bad_book = Book("Book Title", "Author Name", "978045152493X")
        print("❌ FAIL: Should raise ValueError for non-digit ISBN")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # # Test checking out already checked out book
    try:
        book2.checkout()
        print("First checkout successful")
        book2.checkout()  # Should fail
        print("❌ FAIL: Should raise ValueError for double checkout")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # # Test returning book that's not checked out
    try:
        book2.return_book()  # Return the checked out book
        print("First return successful")
        book2.return_book()  # Should fail
        print("❌ FAIL: Should raise ValueError for returning available book")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    print("\n=== Final Status ===")
    print(f"Book 1: {book1}")
    print(f"Book 2: {book2}")