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

## 📸 Screenshot of App

### 📋 Providers List  
![Providers List](https://private-user-images.githubusercontent.com/212729490/446172455-d060c615-6751-499a-8f46-315e0d73ebd8.png)

### ➕ Add Provider Form  
![Add Provider Form](https://private-user-images.githubusercontent.com/212729490/446172458-1564e6ef-4750-4974-8eeb-41a74c3507d1.png)

### ✏️ Edit Provider Form  
![Edit Provider Form](https://private-user-images.githubusercontent.com/212729490/446172648-3d13dc40-08f2-44bb-b9fd-6bbdd4fe18ac.png)

### ❌ Delete Provider Page  
![Delete Provider Page](https://private-user-images.githubusercontent.com/212729490/446172454-3cdf3eb6-f4d2-4061-b608-97179d7d6540.png)

### 📤 Upload Provider CSV File  
![Upload Provider CSV](https://private-user-images.githubusercontent.com/212729490/446172457-cdd33c0a-5ad3-4953-880a-acdd713cd014.png)

### 📊 Providers Dashboard  
![Providers Dashboard](https://private-user-images.githubusercontent.com/212729490/446172456-bf3b6e56-e92a-4bcc-b272-4668fa71eb9f.png)
