# 📚 Library Management System (C)

A simple **Library Management System** developed in C using data structures like **Linked List and Queue**.

This project allows users to manage books, issue and return them, and track issued/returned records.

---

## ✨ Features

### 📖 Book Management

* Add new books
* Delete books
* Search books by ID
* Display all available books

### 🔄 Book Transactions

* Issue books (Queue system)
* Return books
* Track issued books
* Track returned books

---

## 🛠️ Technologies Used

* C Programming
* Data Structures:

  * Linked List (for storing books)
  * Queue (for issued & returned books)
* Visual Studio Code

---

## 📂 Project Structure

```id="l0f3ws"
library-management-system/
│
├── library.c     # Main source code
└── README.md
```

---

## ⚙️ How It Works

* Books are stored using a **Linked List**
* Issued books are handled using a **Queue (FIFO)**
* Returned books are stored in another queue

---

## 🚀 How to Run

### Step 1: Compile the code

```bash id="9ptx7c"
gcc library.c -o library
```

### Step 2: Run the program

```bash id="j2w4qa"
./library
```

---

## 📋 Menu Options

```id="a8mz3n"
1. Add Book
2. Delete Book
3. Search Book
4. Display Books
5. Issue Book
6. Return Book
7. Show Issued Books
8. Show Returned Books
9. Exit
```

---

## 💡 Concepts Used

* Dynamic Memory Allocation (`malloc`, `free`)
* Structures in C
* Linked Lists
* Queue Implementation
* Menu-driven programming

---

## 👨‍💻 Author

* G.kusumanjai

---

## 📜 License

This project is for educational purposes.
