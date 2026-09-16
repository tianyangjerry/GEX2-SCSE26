## This module contains the user interface for the library system. 
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module. 
# Replace "function_name1" with the actual function names you want to import.

from admin import (
    load_library,
    save_library,
    find_book
)



## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):
    if category is None:
        return []

    category_value = str(category).strip().casefold()

    if not category_value:
        return []

    return [
        book_id
        for book_id, book in books.items()
        if str(book.get("category", "")).strip().casefold() == category_value
    ]

    


## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    if search_text is None:
        return []

    search_value = str(search_text).strip().casefold()

    if not search_value:
        return []

    return [
        book_id
        for book_id, book in books.items()
        if search_value in str(book.get("title", "")).casefold()
    ]
    


## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    book_id = find_book(books, search_text)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if borrower is None or not str(borrower).strip():
        return "EMPTY_NAME"

    if (
        not books[book_id].get("available", False)
        or any(loan.get("book_id") == book_id for loan in loans)
    ):
        return "NOT_AVAILABLE"

    books[book_id]["available"] = False
    loans.append({
        "book_id": book_id,
        "borrower": borrower
    })

    return "OK"

    


## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"

def return_book(
    books,
    loans,
    book_title,
    borrower
):
    book_id = find_book(books, book_title)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if borrower is None or not str(borrower).strip():
        return "EMPTY_NAME"

    if books[book_id].get("available", False):
        return "NOT_ON_LOAN"

    borrower_value = str(borrower).strip().casefold()
    loan_index = None

    for index, loan in enumerate(loans):
        if (
            loan.get("book_id") == book_id
            and str(loan.get("borrower", "")).strip().casefold()
            == borrower_value
        ):
            loan_index = index
            break

    if loan_index is None:
        return "NOT_ON_LOAN"

    books[book_id]["available"] = True
    loans.pop(loan_index)

    return "OK"

    



## The main function that runs the user interface for the library system.
## The function must first load the library data from a JSON file, then display a menu for the user to select options.
## The options include searching for books by title or category, borrowing a book, returning a book, and exiting the program.
## When the user selects an option, the corresponding function is called to perform the action.
## The program continues to display the menu until the user chooses to exit, at which point the library data is saved back to the JSON file.
## The main function should also handle invalid selections by displaying an error message and prompting the user to select again.
def main():
    filename = "library.json"
    data = load_library(filename)
    books = data.get("books", {})
    loans = data.get("loans", [])

    print("LIBRARY USER SYSTEM")

    while True:
        print()
        print("1. Search by title")
        print("2. Search by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            search_text = input("Enter title or part of title: ")
            matching_ids = search_by_title(books, search_text)
            if matching_ids:
                for book_id in matching_ids:
                    print(f"{book_id} | {books[book_id].get('title', '')}")
            else:
                print("NO_BOOKS_FOUND")

        elif choice == "2":
            category = input("Enter category: ")
            matching_ids = books_in_category(books, category)
            if matching_ids:
                for book_id in matching_ids:
                    print(f"{book_id} | {books[book_id].get('title', '')}")
            else:
                print("NO_BOOKS_FOUND")

        elif choice == "3":
            search_text = input("Enter book ID, title, or author: ")
            borrower = input("Enter borrower name: ")
            result = borrow_book(books, loans, search_text, borrower)
            print(result)

        elif choice == "4":
            book_title = input("Enter book ID, title, or author: ")
            borrower = input("Enter borrower name: ")
            result = return_book(books, loans, book_title, borrower)
            print(result)

        elif choice == "5":
            data["books"] = books
            data["loans"] = loans
            save_library(data, filename)
            print("Goodbye!")
            break

        else:
            print("INVALID_SELECTION")


if __name__ == "__main__":
    main()

