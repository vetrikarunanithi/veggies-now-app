# VeggiesNow

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3-orange?logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)

**VeggiesNow** is a **Python Flask-based full-stack web application** for **10-minute express delivery** of fresh, organic vegetables and fruits. It brings farm-fresh produce directly to users’ doors with an intuitive and responsive interface. The project features both **User** and **Admin** panels, JSON-based data storage, and full CRUD operations for products and orders.

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Default Admin Credentials](#default-admin-credentials)

---

## Features

### User Panel
- **Login / Signup / Logout** – Secure authentication for users.  
- **Browse Products** – View fresh vegetables and fruits with images, prices, and descriptions.  
- **Add to Cart / Remove Item** – Easily manage items in the shopping cart.  
- **Buy Now** – Purchase a product immediately without adding to the cart.  
- **Checkout** – Complete the order with address, contact, and payment details.  
- **Order Tracking** – View status of current and past orders.

### Admin Panel
- **Admin Login / Signup / Logout** – Secure admin authentication.  
- **Add Product** – Add new products to the platform.  
- **Delete Product** – Remove products from the catalog.  
- **Manage Products** – Update product details such as name, price, and image.  
- **Dashboard** – View overview of all products and orders.  
- **View Orders** – Track all user orders and their status in one place.

---

## Tech Stack
- **Backend:** Python, Flask  
- **Frontend:** HTML5, CSS3, JavaScript  
- **Data Storage:** JSON files (products and orders)  
- **Deployment:** Localhost / Can be deployed to cloud servers  

---

## Project Structure
```
veggies-now-app/
│── app.py
│── data/
│ ├── products.json
│ ├── orders.json
│ └── users.json
│── static/
│ ├── css/
│ │ └── style.css
│ └── js/
│ └── app.js
│── templates/
│ ├── admin_dashboard.html
│ ├── admin_login.html
│ ├── admin_orders.html
│ ├── admin_products.html
│ ├── base.html
│ ├── cart.html
│ ├── checkout.html
│ ├── index.html
│ ├── login.html
│ ├── my_orders.html
│ ├── order_success.html
│ ├── product.html
│ └── signup.html
└── README.md
```

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/veggies-now-app.git
cd veggies-now-app
```
2. **Create and activate a virtual environment (optional)**
```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```
3. **Install dependencies**
```
pip install -r requirements.txt
```
4. **Run the application**
```
flask --app app.py --debug run
python app.py
```
**Visit http://127.0.0.1:5000 to access the app.**

## Default Admin Credentials
- Email: admin@site.com
- Password: admin123

## Live Demo
https://veggies-now-app.onrender.com/

## Author
**Vetriselvan Karunanithi**  
GitHub: [vetrikarunanithi](https://github.com/vetrikarunanithi)  
LinkedIn: [Vetriselvan Karunanithi](https://www.linkedin.com/in/vetriselvank)
