import flask
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db, User, bcrypt
from routes import routes
import os

app = Flask(__name__)

# Enable CORS for all routes with proper configuration
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
     supports_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])

# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecret'
app.config['JWT_SECRET_KEY'] = 'jwt_secret'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Set to a number of seconds if you want tokens to expire

# Connect SQLAlchemy db, bcrypt, jwt to the app
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Create the database
with app.app_context():
    # Drop all tables and recreate them to ensure schema is up to date
    db.drop_all()
    db.create_all()
    print("Database and tables recreated successfully!")
    
    # Check if admin already exists before adding
    admin = User.query.filter_by(email="admin@example.com").first()
    if not admin:
        admin = User(
            email="admin@example.com",
            full_name="Admin User",
            role="admin"
        )
        admin.set_password("admin1234")
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists!")

# Register routes from routes.py
app.register_blueprint(routes)

# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Unhandled exception: {str(e)}")
    return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Function to add sample data
def add_sample_data():
    from models import Subject, Chapter, Quiz, Question
    import datetime
    
    # Check if sample data already exists
    if Subject.query.first():
        print("Sample data already exists, skipping...")
        return
    
    # Create a sample subject
    subject = Subject(name="Mathematics", description="Basic mathematics concepts")
    db.session.add(subject)
    db.session.commit()
    print("Created subject: Mathematics")
    
    # Create a sample chapter
    chapter = Chapter(
        name="Algebra", 
        description="Basic algebraic concepts",
        subject_id=subject.id
    )
    db.session.add(chapter)
    db.session.commit()
    print("Created chapter: Algebra")
    
    # Create a sample quiz (active for 2 hours starting 1 hour ago)
    start_time = datetime.datetime.now() - datetime.timedelta(hours=1)
    quiz = Quiz(
        title="Basic Algebra Quiz",
        chapter_id=chapter.id,
        start_datetime=start_time,
        duration_hours=2,
        duration_minutes=0
    )
    db.session.add(quiz)
    db.session.commit()
    print("Created quiz: Basic Algebra Quiz")
    
    # Create sample questions
    questions_data = [
        {
            "question_text": "What is 2x + 3 = 7?",
            "option1": "x = 2",
            "option2": "x = 3", 
            "option3": "x = 4",
            "option4": "x = 5",
            "correct_option": 1
        },
        {
            "question_text": "Solve for y: 3y - 6 = 9",
            "option1": "y = 3",
            "option2": "y = 4",
            "option3": "y = 5", 
            "option4": "y = 6",
            "correct_option": 3
        }
    ]
    
    for q_data in questions_data:
        question = Question(
            quiz_id=quiz.id,
            question_text=q_data["question_text"],
            option1=q_data["option1"],
            option2=q_data["option2"],
            option3=q_data["option3"],
            option4=q_data["option4"],
            correct_option=q_data["correct_option"]
        )
        db.session.add(question)
        print(f"Created question: {q_data['question_text']}")
    
    db.session.commit()
    print("Sample data added successfully!")

# Add sample data after database creation
with app.app_context():
    add_sample_data()

if __name__ == "__main__":
    app.run(debug=True, port=5006, host='0.0.0.0')