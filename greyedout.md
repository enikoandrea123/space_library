# GREYEDOUT: Explanation of Disabled Features

Certain features in the Library Management System are currently disabled or unavailable in the user interface. These features are "greyed out" to indicate their unavailability and are planned for future updates.

---

## Greyed-Out Features

### 1. **Filtering in Catalog**
   - Users cannot currently filter books in the catalog by title, author, genre, or publication year.
   - **Reason**: This feature requires additional backend query logic and UI elements to handle dynamic filtering.

### 2. **Filtering in Users**
   - Users cannot filter the list of users by name, email, or ID.
   - **Reason**: Similar to catalog filtering, implementing this feature requires a robust search and filter mechanism on the backend.

### 3. **Log-In Functionality**
   - The system currently does not have a login function to authenticate users.
   - **Reason**: Role-based access control and secure user sessions are not yet implemented.

### 4. **Filtering in Borrowed Books**
   - Users cannot filter the list of borrowed books by user name, book title, or due date.
   - **Reason**: This requires advanced query handling and search functionality on the borrowed books list.

### 5. **Late Fee Display in Borrowed List**
   - Late fees for overdue books are not displayed in the borrowed books list.
   - **Reason**: While late fee calculations are possible, integrating them into the borrowed books display and ensuring their accuracy is pending.

---

## Future Plans for Greyed-Out Features

These greyed-out features are essential for the Library Management System to achieve its full functionality. They are planned for implementation in future updates:

1. **Filters** for catalog, users, and borrowed books will improve searchability and user experience.
2. **Login System** to provide secure access and user roles (e.g., admin, librarian).
3. **Late Fee Calculation and Display** in the borrowed books list for better transparency.

