# 📦 Smart Inventory & Sales Management System

A web-based **Smart Inventory & Sales Management System** developed using **Python Flask, HTML, CSS, and MySQL**. The system helps businesses manage products, inventory, customers, sales, and stock efficiently through a centralized dashboard.

## 🚀 Project Overview

The Smart Inventory & Sales Management System is designed to reduce manual inventory work and improve the accuracy of stock and sales management.

The system provides a simple interface for managing products, tracking stock, recording sales, managing customers, and viewing business information from one centralized application.

## ✨ Key Features

* 🔐 User Login & Authentication
* 📊 Dashboard with inventory and sales information
* 📦 Product Management
* 📋 Inventory Management
* 👥 Customer Management
* 💰 Sales Management
* 📉 Automatic Stock Reduction After Sales
* ⚠️ Low Stock Monitoring
* 🧾 Sales Records
* 📈 Sales and Inventory Reports
* 🗄️ MySQL Database Integration
* 🔒 Secure configuration using environment variables

## 🛠️ Technology Stack

### Frontend

* HTML5
* CSS3

### Backend

* Python
* Flask

### Database

* MySQL
* XAMPP
* phpMyAdmin

### Development Tools

* Visual Studio Code
* Git
* GitHub

## 📂 Project Structure

```text
smart-inventory-sales-management-system/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── products.html
│   ├── inventory.html
│   ├── customers.html
│   └── sales.html
│
├── app.py
├── database.sql
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

> The exact files and folders may vary depending on the current version of the project.

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vishwakarma23ks-maker/smart-inventory-sales-management-system.git
```

```bash
cd smart-inventory-sales-management-system
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup MySQL Using XAMPP

1. Open **XAMPP Control Panel**.
2. Start **Apache**.
3. Start **MySQL**.
4. Open phpMyAdmin.
5. Create a new database.
6. Import the provided `database.sql` file.

Example:

```sql
CREATE DATABASE smart_inventory;
```

Then import:

```text
database.sql
```

### 5. Configure Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
SECRET_KEY=your_secret_key

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=smart_inventory
```

Update the values according to your local MySQL configuration.

### 6. Run the Application

```bash
python app.py
```

The application should be available at:

```text
http://127.0.0.1:5000
```

or

```text
http://localhost:5000
```

## 🔄 System Workflow

```text
User Login
    ↓
Dashboard
    ↓
Product Management
    ↓
Inventory Management
    ↓
Customer Management
    ↓
Create Sale
    ↓
Update Stock
    ↓
Save Sales Record
    ↓
View Reports
```

## 📦 Inventory Management

The inventory module allows users to:

* Add products
* Update product information
* Track available stock
* Monitor stock quantities
* Identify low-stock products
* Maintain accurate inventory records

When a sale is completed, the corresponding product quantity is automatically reduced.

## 💰 Sales Management

The sales module allows users to:

* Create sales transactions
* Select products
* Enter quantities
* Calculate sale totals
* Store customer information
* Update inventory automatically
* Maintain sales history

The system also prevents invalid sales when the requested quantity is greater than the available stock.

## 👥 Customer Management

The customer module provides functionality for managing customer information and maintaining customer-related sales records.

## 🗄️ Database

The system uses **MySQL** for persistent data storage.

Main database areas include:

* Users
* Products
* Inventory
* Customers
* Sales
* Sale Items

The database structure is provided in:

```text
database.sql
```

## 🔐 Security

The application includes:

* Login authentication
* Session-based access control
* Environment-based configuration
* Protected database credentials
* Input validation
* Stock validation during sales

> Never upload your real `.env` file, passwords, API keys, or other sensitive credentials to GitHub.

## 🧪 Testing

Before using the application, verify:

* User login works correctly
* Products can be added and updated
* Inventory quantities are accurate
* Customers can be managed
* Sales can be created
* Stock decreases correctly after sales
* Invalid quantities are rejected
* Database records are saved correctly

## 🎯 Project Objectives

The main objectives of this project are:

1. Reduce manual inventory management.
2. Improve stock accuracy.
3. Simplify sales management.
4. Centralize customer and product information.
5. Automatically update inventory after sales.
6. Provide a simple and user-friendly management system.
7. Reduce errors caused by manual record keeping.

## 🔮 Future Enhancements

Possible future improvements include:

* 📊 Advanced analytics dashboard
* 📱 Mobile-responsive improvements
* 🧾 PDF invoice generation
* 📧 Email notifications
* 🔔 Low-stock notifications
* 📈 Advanced sales charts
* 📦 Supplier management
* 🔍 Advanced search and filtering
* 👤 Role-based user permissions
* ☁️ Cloud deployment

## 📸 Screenshots

Add application screenshots here:

```text
screenshots/
├── login.png
├── dashboard.png
├── products.png
├── inventory.png
├── customers.png
└── sales.png
```

Example:

```markdown
![Login Page](screenshots/login.png)

![Dashboard](screenshots/dashboard.png)

![Inventory](screenshots/inventory.png)

![Sales](screenshots/sales.png)
```

## 👨‍💻 Author

**Krishna Vishwakarma**

B.Sc. Computer Science Student
Mumbai, Maharashtra, India

## 📄 License

This project is created for **educational and academic purposes**.


