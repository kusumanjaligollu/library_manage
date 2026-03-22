#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// ----------- Book Linked List Node -----------
typedef struct Book {
    int id;
    char name[50];
    struct Book* next;
} Book;

Book* head = NULL;

// ----------- Queue Node for Issued & Returned Books -----------
typedef struct QueueNode {
    int bookId;
    char name[50];
    struct QueueNode* next;
} QueueNode;

QueueNode* frontIssued = NULL;
QueueNode* rearIssued = NULL;
QueueNode* frontReturned = NULL;
QueueNode* rearReturned = NULL;

// ----------- Linked List Functions -----------
Book* createBook(int id, char name[]) {
    Book* newBook = (Book*)malloc(sizeof(Book));
    newBook->id = id;
    strcpy(newBook->name, name);
    newBook->next = NULL;
    return newBook;
}

void addBook(int id, char name[]) {
    Book* newBook = createBook(id, name);
    if (head == NULL)
        head = newBook;
    else {
        Book* temp = head;
        while (temp->next != NULL)
            temp = temp->next;
        temp->next = newBook;
    }
    printf("Book added successfully.\n");
    fflush(stdout);
}

void displayBooks() {
    if (head == NULL) {
        printf("No books available.\n");
        fflush(stdout);
        return;
    }
    printf("\nBook List:\n");
    Book* temp = head;
    while (temp != NULL) {
        printf("ID: %d | Name: %s\n", temp->id, temp->name);
        temp = temp->next;
    }
    fflush(stdout);
}

Book* searchBook(int id) {
    Book* temp = head;
    while (temp != NULL) {
        if (temp->id == id)
            return temp;
        temp = temp->next;
    }
    return NULL;
}

void deleteBook(int id) {
    if (head == NULL) {
        printf("No books to delete.\n");
        fflush(stdout);
        return;
    }
    Book* temp = head;
    Book* prev = NULL;
    while (temp != NULL && temp->id != id) {
        prev = temp;
        temp = temp->next;
    }
    if (temp == NULL) {
        printf("Book not found.\n");
        fflush(stdout);
        return;
    }
    if (prev == NULL)
        head = head->next;
    else
        prev->next = temp->next;
    free(temp);
    printf("Book deleted successfully.\n");
    fflush(stdout);
}

// ----------- Queue Functions -----------
void issueBook(int id, char name[]) {
    QueueNode* newNode = (QueueNode*)malloc(sizeof(QueueNode));
    newNode->bookId = id;
    strcpy(newNode->name, name);
    newNode->next = NULL;

    if (rearIssued == NULL)
        frontIssued = rearIssued = newNode;
    else {
        rearIssued->next = newNode;
        rearIssued = newNode;
    }
    printf("Book issued successfully.\n");
    fflush(stdout);
}

void returnBook() {
    if (frontIssued == NULL) {
        printf("No books to return.\n");
        fflush(stdout);
        return;
    }

    QueueNode* temp = frontIssued;
    printf("Book Returned -> ID: %d, Name: %s\n", temp->bookId, temp->name);

    // move to returned queue
    QueueNode* newNode = (QueueNode*)malloc(sizeof(QueueNode));
    newNode->bookId = temp->bookId;
    strcpy(newNode->name, temp->name);
    newNode->next = NULL;
    if (rearReturned == NULL)
        frontReturned = rearReturned = newNode;
    else {
        rearReturned->next = newNode;
        rearReturned = newNode;
    }

    // remove from issued
    frontIssued = frontIssued->next;
    if (frontIssued == NULL)
        rearIssued = NULL;

    free(temp);
    fflush(stdout);
}

void showIssuedBooks() {
    if (frontIssued == NULL) {
        printf("No issued books.\n");
        fflush(stdout);
        return;
    }
    printf("\nIssued Books:\n");
    QueueNode* temp = frontIssued;
    while (temp != NULL) {
        printf("ID: %d | Name: %s\n", temp->bookId, temp->name);
        temp = temp->next;
    }
    fflush(stdout);
}

void showReturnedBooks() {
    if (frontReturned == NULL) {
        printf("No returned books yet.\n");
        fflush(stdout);
        return;
    }
    printf("\nReturned Books:\n");
    QueueNode* temp = frontReturned;
    while (temp != NULL) {
        printf("ID: %d | Name: %s\n", temp->bookId, temp->name);
        temp = temp->next;
    }
    fflush(stdout);
}

// ----------- Main Menu -----------
int main() {
    setbuf(stdout, NULL); 
    int choice, id;
    char name[50];

    while (1) {
        printf("\n====== Library Management System ======\n");
        printf("1. Add Book\n2. Delete Book\n3. Search Book\n4. Display Books\n");
        printf("5. Issue Book\n6. Return Book\n7. Show Issued Books\n8. Show Returned Books\n9. Exit\n");
        printf("Enter choice: ");
        fflush(stdout);

        if (scanf("%d", &choice) != 1) return 0;
        getchar(); // newline

        switch (choice) {
            case 1:
                printf("Enter Book ID: ");
                fflush(stdout);
                scanf("%d", &id);
                getchar();
                printf("Enter Book Name: ");
                fflush(stdout);
                fgets(name, sizeof(name), stdin);
                name[strcspn(name, "\n")] = 0;
                addBook(id, name);
                break;
            case 2:
                printf("Enter Book ID to delete: ");
                fflush(stdout);
                scanf("%d", &id);
                deleteBook(id);
                break;
            case 3:
                printf("Enter Book ID to search: ");
                fflush(stdout);
                scanf("%d", &id);
                {
                    Book* found = searchBook(id);
                    if (found)
                        printf("Found -> %s\n", found->name);
                    else
                        printf("Book not found.\n");
                    fflush(stdout);
                }
                break;
            case 4: displayBooks(); break;
            case 5:
                printf("Enter Book ID and Name to issue:\nBook ID: ");
                fflush(stdout);
                scanf("%d", &id);
                getchar();
                printf("Book Name: ");
                fflush(stdout);
                fgets(name, sizeof(name), stdin);
                name[strcspn(name, "\n")] = 0;
                issueBook(id, name);
                break;
            case 6: returnBook(); break;
            case 7: showIssuedBooks(); break;
            case 8: showReturnedBooks(); break;
            case 9:
                printf("Exiting...\n");
                fflush(stdout);
                exit(0);
            default:
                printf("Invalid choice!\n");
                fflush(stdout);
        }
    }
}