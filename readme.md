## Restaurant Management System

This project is a Restaurant Management System, built with Tkinter for the graphical user interface and MySQL for database management. The system provides an easy-to-use interface for managing restaurant reservations for both admins and clients.

# Features

## User Features

Login and Authentication for both admin and client.
Reservation Management:
Clients can book reservations by specifying date, time, place, event type, and guest count.
View pending requests and existing reservations.

## Admin Features

Admin Dashboard for managing reservations.
View Pending Reservations and approve or reject them.
Alter Reservations by editing existing entries.

# Prerequisites

* Python 3.7+
* Tkinter for the GUI
* MySQL Connector for database interaction
Install dependencies using:
```
pip install mysql-connector-python
```

## Setup

### 1. Clone the Repository:
   
   ```
  git clone <repository-url>
  cd <repository-folder>
   ```

### 2. Set Up MySQL Database:
  Create a database named RestaurantDB and necessary tables.

### 3. Run the Application:

  ```
  python AgotAPP.py
  ```

### 4. Access the Application:
   The application will open a GUI for interaction.

# Default Login Credentials

## Admin
Username: admin

Password: admin
## Client
Username: client

Password: client

# Database Structure

`The Reservations table includes:`

* reservation_id (Primary Key)
* client_id (Foreign Key)
* date
* time
* place
* event_type
* guest_count
* status
* rejection_reason (optional)

`The Client table includes:`

* client_id (Primary Key)
* full_name
* address
* contact_number
* email
* username
* password

`The Admin table includes:`

* admin_id (Primary Key)
* username
* password

# Directory Structure
```
restaurant_management/ 
│ 
├── main.py # Main application script 
└── README.md # This file
```
