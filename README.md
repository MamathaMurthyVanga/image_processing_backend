# image_processing_backend

# 📌 Image Processing API  

This project provides an **asynchronous image processing system** using **Django, Celery, and MySQL**.  
It allows users to **upload a CSV file**, process images in the background, and retrieve the processed images via APIs.

---

## 📌 Features  

✅ Upload CSV with input image URLs  
✅ Asynchronous image processing using Celery & Redis  
✅ Store and retrieve processed images  
✅ RESTful API using Django REST Framework  

---

## 📌 Tech Stack  

🔹 **Backend:** Python (Django, Django REST Framework)  
🔹 **Database:** MySQL
🔹 **Hosting:** PythonAnywhere / AWS / Heroku  
🔹 **Version Control:** Git & GitHub  

---

## 📌 Installation Guide  

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/image-processing-api.git
cd image-processing-api
Set Up Virtual Environment
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate

# Install Dependencies
pip install -r requirements.txt


# Set Up Database (MySQL)
Create a database (image_processing_db).
Update settings.py with your database credentials.
Run migrations:
python manage.py makemigrations
python manage.py migrate


# Start Django Server
python manage.py runserver


API Documentation 
Included in repository

Asynchronous Workers Documentation:
Included in the repository

Database Documentation 
Included in the repository

LLD included in repository



