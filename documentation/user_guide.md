# Library Management System - User Guide

Welcome to the Library Management System web application! This guide will help you understand how to use the system effectively.

---

### Introduction
The Library Management System is a web-based application designed to help libraries manage book borrowing and returns efficiently. It allows librarians to manage the inventory, track and register borrowing records.

---

### Accessing the Web App

1.	Open your preferred web browser (Chrome, Firefox, Safari, etc.).
2.  After running the app go to the web app’s URL: http://localhost:5000

---

### User Roles

There is only one types of users in the system.
(They can download the app only)

#### Librarians:

•	Manage the book inventory.

•	View and manage borrowing records.

•	Manage the user inventory.

---
	
## Features Overview (examples)

### Librarian Features

•	View Book List: See all books in the library, including titles, authors, and quantities.

•	Add New Books: Add new books to the inventory.

•	Manage Borrow Records: Track which books are borrowed and by whom.

•	Update Book Quantities: Adjust quantities when books are returned or added.
	
•	Browse Books: View the list of available books.
	
•	Borrow Books: Register book borrowing if they are available.
	
•	Return Books: Register returns through the system.

---

### Borrowing a Book
1.	Open the app.
	
2.	Go to the Book Catalog page.
	
3.	Find a book you want to register for borrowing.
	
4.	Click the “Borrow” button next to the book.
	
5. Add a user by ID, set the dates.

6. Confirm the borrowing request.


### Returning a Book
1.	Open the app.
2. Go to the Borrowed Books page.
3.	Find the book you want to return.
4.	Click the “Return” button next to the book.
5.	A confirmation message will appear if the return is successful.

Note: The book quantity will increase by 1 after returning.

---

## Troubleshooting

### Common Issues and Solutions
1.	Unable to Borrow a Book:

    Ensure the book is available (quantity > 0).

2. Return Button Not Working:

    Ensure you have borrowed the book.
    Frefreshing the page or clearing your browser cache.

3. Form Submission Errors:

    Ensure all required fields are filled out.
