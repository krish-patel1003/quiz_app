# Quiz Application

## Project Description
Quiz Master is a simple web-based quiz application that allows users to:
- Start a new quiz session
- Receive random multiple-choice questions
- Submit answers
- View quiz results

## Project Assumptions
- Questions are pre-loaded into the database
- Quiz consists of a fixed set of multiple-choice questions
- Each question has 4 options (A, B, C, D)
- One correct answer per question
- User can take multiple quiz sessions
- All the questions should be answered

## Prerequisites
- Python 3.9+
- Django 4.2+
- Django Rest Framework
- SQLite (default database)

## Local Setup

### Backend Setup
1. Clone the repository
```bash
git clone https://github.com/yourusername/quiz-master.git
cd quiz-master
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Load Sample Questions
```bash
python manage.py load_questions
```

6. Run Development Server
```bash
python manage.py runserver
```

### Frontend Setup
- No additional setup required
- Ensure backend server is running on `http://localhost:8000`
- open `http://localhost:8000` in browser
- test credentials `username: newuser1` and `password: admin`

## Technology Stack
- Backend: Django, Django Rest Framework
- Frontend: HTML, CSS, JavaScript
- Database: SQLite

## Security Note
- Uses Token-based authentication
- Generates unique session ID for each quiz attempt

## Demo Video
Drive link: https://drive.google.com/file/d/1qTg_Qf5k35Kl0fSPn8cYg5aZyUkNp4DZ/view?usp=sharing
