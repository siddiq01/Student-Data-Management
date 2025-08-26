# 🎓 Student Data Management System (Django)

A web-based **Student Data Management System** built with **Django**.  
It helps manage student records such as adding, updating, deleting, viewing, and searching student information.  

For more information, please visit the Presentation link below:
https://student-data-management--jb90c2w.gamma.site/

---

## 🚀 Features
- 🔐 User Authentication (Signup / Login / Logout)
- 👤 Student Profile Management
- 📄 Add, View, Update, Delete student records
- 🔍 Search students
- 📊 Class-wise student strength
- 📂 Profile Picture Upload
- 🛠 Admin Panel for managing users & students

---

## 🏗️ Project Structure
```
student_management/
│── manage.py
│── db.sqlite3
│── requirements.txt
│── student_management/   # Main project folder
│── students/             # App with models, views, templates
│   ├── templates/students
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── profile.html
│   │   ├── display.html
│   │   ├── add_update.html
│   │   ├── search.html
│   │   └── navbar.html
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templatetags/
│
└── media/ (uploaded profile images)
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/student-data-management.git
   cd student-data-management
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run server**
   ```bash
   python manage.py runserver
   ```

7. Open in browser → [http://127.0.0.1:8000](http://127.0.0.1:8000)

---


## 🎯 Future Scope
- Attendance Management
- Exam Marks & Results
- Role-based Access (Admin/Teacher/Student)
- Export data to Excel / PDF
- Notifications & Announcements

---

## 🙌 Author
**Siddiq badlani**  
💻 Student Management System Project (Django)
