# Mesonet-Provider-Dashboard
A Flask-based web application for managing and visualizing provider data with CSV import functionality and interactive dashboard.

## Features

- Provider Management (Add, Edit, Delete)
- Bulk Import via CSV
- Data Validation
- Interactive Dashboard with Charts
- Duplicate Entry Prevention
- Active/Inactive Status Tracking

## Tech Stack

- Python 3.8+
- Flask
- SQLAlchemy
- Chart.js
- Bootstrap
- SQLite Database

## Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/manib90/Mesonet-Provider-Dashboard.git
cd mesonet-provider-dashboard

2. **Create Virtual Environment**
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies**
pip install -r requirements.txt

4. **Run the Application**
flask run
The application will be available at http://localhost:5000


##  Database Schema
SQL
CREATE TABLE provider (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    status VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, location)
);

## Sample CSV
name,location,category,status
Provider A,NYC,Weather,Active
Provider B,LA,Satellite,Inactive

## Screenshot of app

## Proviers List
![alt text](image.png)
## Add Provider Form
![alt text](image-1.png)
## Edit Provider Form
![alt text](image-2.png)
## Delete Provider Page
![alt text](image-3.png)
## Upload Provider CSV File
![alt text](image-4.png)
## Providers Dashboard
![alt text](image-5.png)
