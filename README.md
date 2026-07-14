<div align="center">

# StudyMatch

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-Web%20Framework-092E20?logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Bulma](https://img.shields.io/badge/Bulma-CSS-00D1B2?logo=bulma&logoColor=white)

**Information system for managing university study groups**

</div>

StudyMatch is a Django web application for managing university study groups.  
It connects students, tutors and administrators through role-based features.  
The platform manages groups, exams, participation requests, materials and notifications.  
Data consistency is enforced through Django constraints and custom SQLite triggers.

---

## Installation

### Requirements

Before starting, make sure you have the following installed:

- Python 3
- `pip`
- Git
- SQLite command-line tools

### 1. Clone the repository

```bash
git clone https://github.com/CarMine05-Byte/Student_Match.git
cd Student_Match
```

### 2. Create a virtual environment

#### Linux and macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows PowerShell

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Import the SQL dump

The repository includes an SQL dump containing the database structure and initial data.

Import the dump into a new or empty SQLite database:

```bash
sqlite3 db.sqlite3 ".read studymatch_dump.sql"
```

Do not run the migrations before importing the dump if it already contains the complete database schema.

### 5. Start the development server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

---

## Main Features

StudyMatch allows users to:

- register and authenticate;
- store passwords using hashing;
- distinguish accounts by student, tutor and administrator roles;
- display different content and operations according to the authenticated user's role;
- create and view study groups;
- associate one or more exams with study groups;
- request and manage student participation;
- record exams completed by students;
- assign tutors and administrators to study groups;
- associate learning materials with study groups;
- send and view notifications;
- prevent unauthorized operations or actions that conflict with database constraints.

---

## Roles

### Student

Students can:

- view available study groups;
- request to join a group;
- check the status of their participation requests;
- view exams;
- record completed exams and their completion dates;
- access materials associated with study groups;
- view received notifications.

### Tutor

Tutors can:

- view the groups they are assigned to;
- support one or more study groups;
- access information about the groups they support;
- view exams and materials associated with their groups.

### Administrator

Administrators can:

- create and manage study groups;
- view the groups they are responsible for;
- manage student participation requests;
- associate study groups with exams;
- assign tutors and administrators to groups;
- send notifications to users;
- access the supervision features provided by the platform.

---

## Database

The application uses SQLite as its database, managed through the Django ORM.

### User Roles in the Database

`UTENTE` stores the common data shared by all accounts, while `STUDENTE`, `TUTOR` and `ADMIN` store the information specific to each role.

The primary key of `UTENTE` is included in the related role table as a unique reference.

---

## Project Verification

To check the general Django configuration, run:

```bash
python manage.py check
```

If automated tests are available in the repository, run:

```bash
python manage.py test
```

---

<div align="center">

**StudyMatch — University Study Group Management System**

</div>
