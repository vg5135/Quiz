from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import create_access_token, decode_token, get_jwt, jwt_required, verify_jwt_in_request
from models import db, bcrypt, Subject, Quiz, Question, Score, User, Chapter, Notes, NotePage
from rbac import role_required
from chatbot import chatbot
import datetime
import json
import os
from werkzeug.utils import secure_filename

# Define IST timezone
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json', 'txt'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

routes = Blueprint('routes', __name__)

# Render registration form
@routes.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')

# User registration
@routes.route('/register', methods=['POST'])
def register():
    if request.is_json:
        data = request.json
    else:
        data = request.form
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({"message": "User already exists"}), 400
    
    dob = data.get('date_of_birth', None)
    print("dob1 is", dob)
    if dob:
        try:
            dob = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
            print("dob2 is", dob)
        except Exception:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400
    
    
    new_user = User(
        email=data['email'],
        full_name=data.get('full_name', ''),
        qualification=data.get('qualification', ''),
        date_of_birth=dob
    )
    new_user.set_password(data['password'])  # Hash the password
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# Render login form
@routes.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

# Login (Admin/User)
@routes.route('/login', methods=['POST'])
def login():
    try:
        if request.is_json:
            data = request.json
        else:
            data = request.form
            
        print("Login attempt for email:", data.get('email'))
        
        if not data.get('email') or not data.get('password'):
            return jsonify({"message": "Email and password are required"}), 400
            
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            print("User not found:", data.get('email'))
            return jsonify({"message": "Invalid credentials"}), 401
            
        if not user.check_password(data['password']):
            print("Invalid password for user:", data.get('email'))
            return jsonify({"message": "Invalid credentials"}), 401

        access_token = create_access_token(
            identity=user.email,
            additional_claims={"role": user.role}
        )
        
        print("Login successful for:", user.email, "with role:", user.role)
        return jsonify({
            "access_token": access_token,
            "user": {
                "email": user.email,
                "role": user.role,
                "full_name": user.full_name
            }
        }), 200
    except Exception as e:
        print("Login error:", str(e))
        return jsonify({"message": "An error occurred during login"}), 500

#admin-only route
@routes.route('/admin-only', methods=['GET'])
@role_required('admin')
def admin_only():
    return jsonify(msg="Welcome, Admin")


#user-only route
@routes.route('/user-only', methods=['GET'])
@role_required('user')
def user_only():
    return jsonify (msg = "Hello, Student!")

@routes.route("/")
def home():
    print("This is backend print")
    return "Hello from Flask"

#Protect Admin Management Routes
#Quizzes
# Create Quizzes
@routes.route('/create_quizzes', methods=['POST'])
@role_required('admin')
def create_quiz():
    # Define IST timezone within function scope
    IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    
    data = request.json
    print(f"Creating quiz with data: {data}")  # Debug log
    
    try:
        # Handle both ISO format and standard format datetime strings
        if 'start_datetime' in data and data['start_datetime']:
            try:
                # First try to parse as ISO format
                if 'T' in data['start_datetime']:
                    start_datetime = datetime.datetime.fromisoformat(data['start_datetime'].replace('Z', '+00:00'))
                else:
                    # Try standard format if ISO fails
                    start_datetime = datetime.datetime.strptime(data['start_datetime'], "%Y-%m-%d %H:%M")
                
                # Ensure timezone awareness
                if start_datetime.tzinfo is None:
                    start_datetime = start_datetime.replace(tzinfo=IST)
                else:
                    # Convert to IST if it has a different timezone
                    start_datetime = start_datetime.astimezone(IST)
                    
                print(f"Parsed start_datetime: {start_datetime}")  # Debug log
                
            except Exception as e:
                print(f"Error parsing start_datetime: {data['start_datetime']}, error: {str(e)}")  # Debug log
                return jsonify({"message": f"Invalid start_datetime format: {data['start_datetime']}. Use YYYY-MM-DDTHH:MM or YYYY-MM-DD HH:MM"}), 400
        else:
            return jsonify({"message": "start_datetime is required"}), 400

        quiz = Quiz(
            title=data['title'],
            chapter_id=data['chapter_id'],
            start_datetime=start_datetime,
            duration_hours=int(data.get('duration_hours', 0)),
            duration_minutes=int(data.get('duration_minutes', 30))
        )
        db.session.add(quiz)
        db.session.commit()
        
        print(f"Quiz created successfully with ID: {quiz.id}")  # Debug log
        
        return jsonify({
            "message": "Quiz created",
            "quiz": {
                "id": quiz.id,
                "title": quiz.title,
                "start_datetime": quiz.start_datetime.isoformat(),
                "end_datetime": quiz.end_datetime.isoformat() if quiz.end_datetime else None,
                "duration_hours": quiz.duration_hours,
                "duration_minutes": quiz.duration_minutes,
                "chapter_id": quiz.chapter_id
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating quiz: {str(e)}")  # Debug log
        return jsonify({"message": f"Error creating quiz: {str(e)}"}), 500


# Edit/Update Quizzes
@routes.route('/update_quizzes/<int:quiz_id>', methods=['PUT'])
@role_required('admin')
def update_quiz(quiz_id):
    # Define IST timezone within function scope
    IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    
    data = request.json
    print(f"Updating quiz {quiz_id} with data: {data}")  # Debug log
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"message": "Quiz not found"}), 404
    
    try:
        if 'title' in data:
            quiz.title = data['title']
            
        if 'chapter_id' in data:
            quiz.chapter_id = int(data['chapter_id'])
            
        if 'start_datetime' in data and data['start_datetime']:
            # Handle ISO format datetime string from frontend
            try:
                # First try to parse as ISO format
                if 'T' in data['start_datetime']:
                    start_datetime = datetime.datetime.fromisoformat(data['start_datetime'].replace('Z', '+00:00'))
                else:
                    # Try standard format if ISO fails
                    start_datetime = datetime.datetime.strptime(data['start_datetime'], "%Y-%m-%d %H:%M")
                
                # Ensure timezone awareness
                if start_datetime.tzinfo is None:
                    start_datetime = start_datetime.replace(tzinfo=IST)
                else:
                    # Convert to IST if it has a different timezone
                    start_datetime = start_datetime.astimezone(IST)
                    
                quiz.start_datetime = start_datetime
                print(f"Parsed start_datetime: {start_datetime}")  # Debug log
                
            except Exception as e:
                print(f"Error parsing start_datetime: {data['start_datetime']}, error: {str(e)}")  # Debug log
                return jsonify({"message": f"Invalid start_datetime format: {data['start_datetime']}. Use YYYY-MM-DDTHH:MM or YYYY-MM-DD HH:MM"}), 400
            
        if 'end_datetime' in data and data['end_datetime']:
            # Handle end_datetime if provided
            try:
                # First try to parse as ISO format
                if 'T' in data['end_datetime']:
                    end_datetime = datetime.datetime.fromisoformat(data['end_datetime'].replace('Z', '+00:00'))
                else:
                    # Try standard format if ISO fails
                    end_datetime = datetime.datetime.strptime(data['end_datetime'], "%Y-%m-%d %H:%M")
                
                # Ensure timezone awareness
                if end_datetime.tzinfo is None:
                    end_datetime = end_datetime.replace(tzinfo=IST)
                else:
                    # Convert to IST if it has a different timezone
                    end_datetime = end_datetime.astimezone(IST)
                    
                print(f"Parsed end_datetime: {end_datetime}")  # Debug log
                # Note: We can't directly set end_datetime as it's a property, but we can adjust duration
                
            except Exception as e:
                print(f"Error parsing end_datetime: {data['end_datetime']}, error: {str(e)}")  # Debug log
                return jsonify({"message": f"Invalid end_datetime format: {data['end_datetime']}. Use YYYY-MM-DDTHH:MM or YYYY-MM-DD HH:MM"}), 400
        
        if 'duration_hours' in data:
            quiz.duration_hours = int(data['duration_hours'])
        if 'duration_minutes' in data:
            quiz.duration_minutes = int(data['duration_minutes'])
        
        # Handle status field from frontend (convert to active/inactive logic)
        if 'status' in data:
            # The status field from frontend is just for display
            # The actual active status is calculated based on datetime
            # We don't need to do anything here as is_active is a computed property
            print(f"Status field received: {data['status']}")  # Debug log
            pass
        
        db.session.commit()
        print(f"Quiz {quiz_id} updated successfully")  # Debug log
        
        return jsonify({
            "message": "Quiz updated successfully",
            "quiz": {
                "id": quiz.id,
                "title": quiz.title,
                "start_datetime": quiz.start_datetime.isoformat() if quiz.start_datetime else None,
                "end_datetime": quiz.end_datetime.isoformat() if quiz.end_datetime else None,
                "duration_hours": quiz.duration_hours,
                "duration_minutes": quiz.duration_minutes,
                "chapter_id": quiz.chapter_id,
                "is_active": quiz.is_active
            }
        }), 200
    except (ValueError, TypeError) as e:
        db.session.rollback()
        print(f"Error updating quiz {quiz_id}: {str(e)}")  # Debug log
        return jsonify({"message": f"Invalid data format: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error updating quiz {quiz_id}: {str(e)}")  # Debug log
        return jsonify({"message": f"Error updating quiz: {str(e)}"}), 500

# Toggle Quiz Status (Make Live/Inactive)
@routes.route('/toggle_quiz/<int:quiz_id>', methods=['POST'])
@role_required('admin')
def toggle_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"message": "Quiz not found"}), 404
    
    try:
        # Toggle the manual_is_active status
        quiz.manual_is_active = not quiz.manual_is_active
        
        db.session.commit()
        
        # Get the new status after changes
        new_status = quiz.is_active
        
        return jsonify({
            "message": f"Quiz {'activated' if new_status else 'deactivated'}",
            "is_active": new_status
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error toggling quiz {quiz_id}: {str(e)}")  # Debug log
        return jsonify({"message": f"Error toggling quiz: {str(e)}"}), 500

# Delete Quizzes
@routes.route('/delete_quizzes/<int:quiz_id>', methods=['DELETE'])
@role_required('admin')
def delete_quiz(quiz_id):
    try:
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({"message": "Quiz not found"}), 404
        
        # Delete related scores first
        Score.query.filter_by(quiz_id=quiz_id).delete()
        
        # Delete related questions
        Question.query.filter_by(quiz_id=quiz_id).delete()
        
        # Now delete the quiz
        db.session.delete(quiz)
        db.session.commit()
        
        return jsonify({"message": "Quiz deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting quiz: {str(e)}"}), 500

# Create users
@routes.route('/create_users', methods=['POST'])
@role_required('admin')
def create_user():
    data=request.json
    if User.query.filter_by(email=data['email']).first():
                return jsonify({"message": "User already exists"}), 400
    dob = data.get('date_of_birth')
    if dob:
        try:
            dob = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
        except Exception:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400
    else:
        dob = None
    new_user = User(
        email=data['email'],
        full_name=data.get('full_name', ''),
        qualification=data.get('qualification', ''),
        date_of_birth=dob,
        role=data.get('role', 'user')
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created", "id": new_user.id}), 201


# Edit/Update users
@routes.route('/update_users/<int:user_id>', methods=['PUT'])
@role_required('admin')
def update_user(user_id):
    data = request.json
    user = User.query.get_or_404(user_id)
    user.full_name = data.get('full_name', user.full_name)
    user.qualification = data.get('qualification', user.qualification)
    user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
    user.role = data.get('role', user.role)
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    db.session.commit()
    return jsonify({"message": "User updated"})

# Delete users
@routes.route('/delete_users/<int:user_id>', methods=['DELETE'])
@role_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})

# Admin: List all users
@routes.route('/list_users', methods=['GET'])
@role_required('admin')
def list_users():
    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "qualification": u.qualification,
            "date_of_birth": str(u.date_of_birth) if u.date_of_birth else None,
            "role": u.role
        }
        for u in users
    ])

# Create subjects
@routes.route('/create_subjects', methods=['POST'])
@role_required('admin')
def create_subject():
    data = request.json
    subject = Subject(name=data['name'], description=data.get('description', ''))
    db.session.add(subject)
    db.session.commit()
    return jsonify({"message": "Subject created", "id": subject.id}), 201

# Edit/Update subjects
@routes.route('/update_subjects/<int:subject_id>', methods=['PUT'])
@role_required('admin')
def update_subject(subject_id):
    data = request.json
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"message": "Subject not found"}), 404
    subject.name = data['name']
    subject.description = data.get('description', '')
    db.session.commit()
    return jsonify({"message": "Subject updated"}), 200


# Delete subjects
@routes.route('/delete_subjects/<int:subject_id>', methods=['DELETE'])
@role_required('admin')
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"message": "Subject not found"}), 404
    db.session.delete(subject)
    db.session.commit()
    return jsonify({"message": "Subject deleted"}), 200

# Create questions
@routes.route('/create_questions', methods=['POST'])
@role_required('admin')
def create_question():
    data = request.json
    question = Question(
        quiz_id=data['quiz_id'],
        question_text=data['question_text'],
        option1=data['option1'],
        option2=data['option2'],
        option3=data['option3'],
        option4=data['option4'],
        correct_option=data['correct_option']
    )
    db.session.add(question)
    db.session.commit()
    return jsonify({"message": "Question created", "id": question.id}), 201

# Edit/Update questions
@routes.route('/update_questions/<int:question_id>', methods=['PUT'])
@role_required('admin')
def update_question(question_id):
    data = request.json
    question = Question.query.get_or_404(question_id)
    question.question_text = data['question_text']
    question.option1 = data['option1']
    question.option2 = data['option2']
    question.option3 = data['option3']
    question.option4 = data['option4']
    question.correct_option = data['correct_option']
    db.session.commit()
    return jsonify({"message": "Question updated"})

# Delete questions
@routes.route('/delete_questions/<int:question_id>', methods=['DELETE'])
@role_required('admin')
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted"})

# Attempt a quiz
@routes.route('/attempt_quiz/<int:quiz_id>', methods=['POST'])
@role_required('user')
def attempt_quiz(quiz_id):
    data = request.json
    # Example: Save user's answers and calculate score
    user_email = get_jwt()['sub']
    user = User.query.filter_by(email=user_email).first()
    score = Score(user_id=user.id, quiz_id=quiz_id, score=data['score'])
    db.session.add(score)
    db.session.commit()
    return jsonify({"message": "Quiz attempted", "score": data['score']}), 201

# View user's own scores
@routes.route('/my_scores', methods=['GET'])
@role_required('user')
def view_scores():
    user_email = get_jwt()['sub']
    user = User.query.filter_by(email=user_email).first()
    scores = Score.query.filter_by(user_id=user.id).all()
    return jsonify([
        {"quiz_id": s.quiz_id, "score": s.score, "date_taken": s.date_taken}
        for s in scores
    ])
#allow users to list available quizzes
@routes.route('/available_quizzes', methods=['GET'])
@role_required('user')
def available_quizzes():
    # Define IST timezone within function scope
    IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    
    now = datetime.datetime.now(IST)
    quizzes = Quiz.query.all()
    
    print(f"DEBUG: Current time (IST): {now}")
    print(f"DEBUG: Total quizzes found: {len(quizzes)}")
    
    available_quizzes = []
    for quiz in quizzes:
        print(f"DEBUG: Checking quiz '{quiz.title}'")
        print(f"DEBUG: Quiz start_datetime: {quiz.start_datetime}")
        print(f"DEBUG: Quiz end_datetime: {quiz.end_datetime}")
        
        if quiz.start_datetime and quiz.end_datetime:
            # Ensure timezone awareness
            start_time = quiz.start_datetime.replace(tzinfo=IST) if quiz.start_datetime.tzinfo is None else quiz.start_datetime
            end_time = quiz.end_datetime.replace(tzinfo=IST) if quiz.end_datetime.tzinfo is None else quiz.end_datetime
            
            print(f"DEBUG: Start time (IST): {start_time}")
            print(f"DEBUG: End time (IST): {end_time}")
            print(f"DEBUG: Is active? {start_time <= now <= end_time}")
            
            # Only include active quizzes
            if start_time <= now <= end_time:
                available_quizzes.append({
                    "id": quiz.id, 
                    "title": quiz.title,
                    "start_datetime": start_time.isoformat(),
                    "end_datetime": end_time.isoformat(),
                    "duration_hours": quiz.duration_hours,
                    "duration_minutes": quiz.duration_minutes,
                    "status": "active"
                })
                print(f"DEBUG: Added quiz '{quiz.title}' to available list")
    
    print(f"DEBUG: Final available quizzes count: {len(available_quizzes)}")
    return jsonify(available_quizzes)

# Get all subjects with their chapters and quizzes
@routes.route('/api/subjects', methods=['GET', 'OPTIONS'])
@jwt_required(optional=True)  # Make JWT optional for CORS preflight
def get_subjects():
    if request.method == 'OPTIONS':
        from flask import make_response
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response, 200
    
    try:
        # Define IST timezone within function scope
        IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        
        subjects = Subject.query.all()
        now = datetime.datetime.now(IST)
        
        def get_quiz_status(quiz):
            try:
                if not quiz.start_datetime:
                    return 'inactive'
                
                # Handle timezone-aware datetime objects
                start_time = quiz.start_datetime
                if start_time.tzinfo is None:
                    start_time = start_time.replace(tzinfo=IST)
                
                end_time = quiz.end_datetime
                if end_time and end_time.tzinfo is None:
                    end_time = end_time.replace(tzinfo=IST)
                
                if not end_time:
                    return 'inactive'
                
                if now < start_time:
                    return 'upcoming'
                elif now > end_time:
                    return 'expired'
                return 'active'
            except Exception as e:
                print(f"Error calculating quiz status for quiz {quiz.id}: {str(e)}")
                return 'inactive'

        subject_list = []
        for subject in subjects:
            try:
                subject_data = {
                    'id': subject.id,
                    'name': subject.name,
                    'description': subject.description,
                    'chapters': []
                }
                
                for chapter in subject.chapters:
                    try:
                        chapter_data = {
                            'id': chapter.id,
                            'name': chapter.name,
                            'description': chapter.description,
                            'quizzes': []
                        }
                        
                        for quiz in chapter.quizzes:
                            try:
                                quiz_data = {
                                    'id': quiz.id,
                                    'title': quiz.title,
                                    'start_datetime': quiz.start_datetime.isoformat() if quiz.start_datetime else None,
                                    'duration_hours': quiz.duration_hours,
                                    'duration_minutes': quiz.duration_minutes,
                                    'end_datetime': quiz.end_datetime.isoformat() if quiz.end_datetime else None,
                                    'status': get_quiz_status(quiz),
                                    'questions': [{
                                        'id': question.id,
                                        'question_text': question.question_text,
                                        'option1': question.option1,
                                        'option2': question.option2,
                                        'option3': question.option3,
                                        'option4': question.option4
                                    } for question in quiz.questions]
                                }
                                chapter_data['quizzes'].append(quiz_data)
                            except Exception as e:
                                print(f"Error processing quiz {quiz.id}: {str(e)}")
                                continue
                        
                        subject_data['chapters'].append(chapter_data)
                    except Exception as e:
                        print(f"Error processing chapter {chapter.id}: {str(e)}")
                        continue
                
                subject_list.append(subject_data)
            except Exception as e:
                print(f"Error processing subject {subject.id}: {str(e)}")
                continue
        
        return jsonify(subject_list)
    except Exception as e:
        print(f"Error in get_subjects: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Test endpoint to get quiz data without strict time checks
@routes.route('/api/test-quiz/<int:quiz_id>', methods=['GET'])
@role_required('user')
def test_get_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    
    return jsonify({
        'id': quiz.id,
        'title': quiz.title,
        'start_datetime': quiz.start_datetime.isoformat() if quiz.start_datetime else None,
        'end_datetime': quiz.end_datetime.isoformat() if quiz.end_datetime else None,
        'duration_hours': quiz.duration_hours,
        'duration_minutes': quiz.duration_minutes,
        'questions': [{
            'id': q.id,
            'question_text': q.question_text,
            'option1': q.option1,
            'option2': q.option2,
            'option3': q.option3,
            'option4': q.option4,
            'correct_option': q.correct_option
        } for q in questions]
    })

# Get quiz details with questions
@routes.route('/api/quizzes/<int:quiz_id>', methods=['GET'])
@role_required('user')
def get_quiz(quiz_id):
    # Define IST timezone within function scope
    IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    now = datetime.datetime.now(IST)
    
    print(f"DEBUG: get_quiz called for quiz_id: {quiz_id}")
    print(f"DEBUG: Quiz title: {quiz.title}")
    print(f"DEBUG: Current time (IST): {now}")
    print(f"DEBUG: Quiz start_datetime: {quiz.start_datetime}")
    print(f"DEBUG: Quiz end_datetime: {quiz.end_datetime}")
    
    # Check if quiz is active
    if not quiz.start_datetime or not quiz.end_datetime:
        print(f"DEBUG: Quiz {quiz_id} has no start_datetime or end_datetime")
        return jsonify({"message": "Quiz is not available"}), 403
    
    start_time = quiz.start_datetime.replace(tzinfo=IST) if quiz.start_datetime.tzinfo is None else quiz.start_datetime
    end_time = quiz.end_datetime.replace(tzinfo=IST) if quiz.end_datetime.tzinfo is None else quiz.end_datetime
    
    print(f"DEBUG: Start time (IST): {start_time}")
    print(f"DEBUG: End time (IST): {end_time}")
    print(f"DEBUG: Is current time between start and end? {start_time <= now <= end_time}")
    
    # Only allow access if quiz is currently active
    if not (start_time <= now <= end_time):
        print(f"DEBUG: Quiz {quiz_id} is not currently active")
        return jsonify({"message": "Quiz is not currently active"}), 403
    
    print(f"DEBUG: Quiz {quiz_id} is active, fetching questions")
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    print(f"DEBUG: Found {len(questions)} questions for quiz {quiz_id}")
    
    return jsonify({
        'id': quiz.id,
        'title': quiz.title,
        'start_datetime': start_time.isoformat(),
        'duration_hours': quiz.duration_hours,
        'duration_minutes': quiz.duration_minutes,
        'end_datetime': end_time.isoformat(),
        'questions': [{
            'id': q.id,
            'question_text': q.question_text,
            'option1': q.option1,
            'option2': q.option2,
            'option3': q.option3,
            'option4': q.option4,
            'correct_option': q.correct_option
        } for q in questions]
    })

# Submit quiz attempt
@routes.route('/api/submit-quiz', methods=['POST'])
@role_required('user')
def submit_quiz():
    data = request.json
    user_email = get_jwt()['sub']
    user = User.query.filter_by(email=user_email).first()
    
    score = Score(
        user_id=user.id,
        quiz_id=data['quizId'],
        score=data['score']
    )
    db.session.add(score)
    db.session.commit()
    
    return jsonify({
        'message': 'Quiz submitted successfully',
        'score': data['score']
    }), 201

# Get user's quiz history
@routes.route('/api/quiz-history', methods=['GET'])
@role_required('user')
def get_quiz_history():
    user_email = get_jwt()['sub']
    user = User.query.filter_by(email=user_email).first()
    scores = Score.query.filter_by(user_id=user.id).all()
    
    return jsonify([{
        'quiz_id': score.quiz_id,
        'quiz_title': score.quiz.title,
        'score': score.score,
        'total_questions': len(score.quiz.questions),
        'date_taken': score.date_taken.strftime('%Y-%m-%d %H:%M:%S')
    } for score in scores])

# Create Chapter
@routes.route('/create_chapters', methods=['POST'])
@role_required('admin')
def create_chapter():
    data = request.json
    chapter = Chapter(
        name=data['name'],
        description=data.get('description', ''),
        subject_id=data['subject_id']
    )
    db.session.add(chapter)
    db.session.commit()
    return jsonify({"message": "Chapter created", "id": chapter.id}), 201

# Update Chapter
@routes.route('/update_chapters/<int:chapter_id>', methods=['PUT'])
@role_required('admin')
def update_chapter(chapter_id):
    data = request.json
    chapter = Chapter.query.get_or_404(chapter_id)
    chapter.name = data['name']
    chapter.description = data.get('description', chapter.description)
    db.session.commit()
    return jsonify({"message": "Chapter updated"}), 200

# Delete Chapter
@routes.route('/delete_chapters/<int:chapter_id>', methods=['DELETE'])
@role_required('admin')
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    return jsonify({"message": "Chapter deleted"}), 200

# Fix CORS for /api/chapters
@routes.route('/api/chapters', methods=['GET', 'OPTIONS'])
@jwt_required(optional=True)
def get_chapters():
    if request.method == 'OPTIONS':
        from flask import make_response
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response, 200
    chapters = Chapter.query.all()
    return jsonify([{
        'id': chapter.id,
        'name': chapter.name,
        'description': chapter.description,
        'subject_id': chapter.subject_id
    } for chapter in chapters])

# Fix CORS for /api/quizzes
@routes.route('/api/quizzes', methods=['GET', 'OPTIONS'])
@jwt_required(optional=True)
def get_quizzes():
    if request.method == 'OPTIONS':
        from flask import make_response
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response, 200
    
    try:
        # Define IST timezone within function scope
        IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        
        quizzes = Quiz.query.all()
        now = datetime.datetime.now(IST)
        
        def get_quiz_status(quiz):
            try:
                if not quiz.start_datetime:
                    return 'inactive'
                
                # Handle timezone-aware datetime objects
                start_time = quiz.start_datetime
                if start_time.tzinfo is None:
                    start_time = start_time.replace(tzinfo=IST)
                
                end_time = quiz.end_datetime
                if end_time and end_time.tzinfo is None:
                    end_time = end_time.replace(tzinfo=IST)
                
                if not end_time:
                    return 'inactive'
                
                if now < start_time:
                    return 'upcoming'
                elif now > end_time:
                    return 'expired'
                return 'active'
            except Exception as e:
                print(f"Error calculating quiz status for quiz {quiz.id}: {str(e)}")
                return 'inactive'
        
        quiz_list = []
        for quiz in quizzes:
            try:
                quiz_data = {
                    'id': quiz.id,
                    'title': quiz.title,
                    'chapter_id': quiz.chapter_id,
                    'start_datetime': quiz.start_datetime.isoformat() if quiz.start_datetime else None,
                    'end_datetime': quiz.end_datetime.isoformat() if quiz.end_datetime else None,
                    'duration_hours': quiz.duration_hours,
                    'duration_minutes': quiz.duration_minutes,
                    'status': get_quiz_status(quiz)
                }
                quiz_list.append(quiz_data)
            except Exception as e:
                print(f"Error processing quiz {quiz.id}: {str(e)}")
                # Skip problematic quizzes instead of failing completely
                continue
        
        return jsonify(quiz_list)
    except Exception as e:
        print(f"Error in get_quizzes: {str(e)}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Get all questions (for admin)
@routes.route('/api/questions', methods=['GET'])
@role_required('admin')
def get_questions():
    questions = Question.query.all()
    return jsonify([
        {
            'id': q.id,
            'quiz_id': q.quiz_id,
            'question_text': q.question_text,
            'option1': q.option1,
            'option2': q.option2,
            'option3': q.option3,
            'option4': q.option4,
            'correct_option': q.correct_option
        }
        for q in questions
    ])

# Debug endpoint to check quiz status
@routes.route('/debug/quizzes', methods=['GET'])
@role_required('admin')
def debug_quizzes():
    # Define IST timezone within function scope
    IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    
    now = datetime.datetime.now(IST)
    quizzes = Quiz.query.all()
    
    debug_info = {
        'current_time_ist': now.isoformat(),
        'total_quizzes': len(quizzes),
        'quizzes': []
    }
    
    for quiz in quizzes:
        quiz_info = {
            'id': quiz.id,
            'title': quiz.title,
            'start_datetime': quiz.start_datetime.isoformat() if quiz.start_datetime else None,
            'end_datetime': quiz.end_datetime.isoformat() if quiz.end_datetime else None,
            'duration_hours': quiz.duration_hours,
            'duration_minutes': quiz.duration_minutes,
            'is_active': quiz.is_active
        }
        debug_info['quizzes'].append(quiz_info)
    
    return jsonify(debug_info)

# Chatbot endpoint
@routes.route('/api/chat', methods=['POST', 'OPTIONS'])
@jwt_required(optional=True)
def chat():
    if request.method == 'OPTIONS':
        from flask import make_response
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response, 200
    
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"message": "Please provide a message"}), 400
        
        # Get user context if available
        user_context = {}
        try:
            jwt_data = get_jwt()
            user_email = jwt_data.get('sub')
            if user_email:
                user = User.query.filter_by(email=user_email).first()
                if user:
                    user_context = {
                        'role': user.role,
                        'name': user.full_name,
                        'email': user.email
                    }
        except:
            pass  # Continue without user context if JWT is invalid
        
        # Get response from chatbot
        response = chatbot.get_response(user_message, user_context)
        
        return jsonify({
            "message": response,
            "timestamp": datetime.datetime.now(IST).isoformat()
        }), 200
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            "message": "Sorry, I encountered an error. Please try again.",
            "timestamp": datetime.datetime.now(IST).isoformat()
        }), 500

# Enhanced Quiz Creation Routes

# Bulk Quiz Creation with JSON File Upload
@routes.route('/api/bulk-create-quiz', methods=['POST', 'OPTIONS'])
def bulk_create_quiz():
    """
    Create multiple quizzes from a JSON file upload
    Expected JSON format:
    {
        "subject_name": "Mathematics",
        "chapter_name": "Algebra",
        "quizzes": [
            {
                "title": "Basic Algebra Quiz",
                "start_datetime": "2024-01-15T10:00:00",
                "duration_hours": 1,
                "duration_minutes": 30,
                "questions": [
                    {
                        "question_text": "What is 2x + 3 = 7?",
                        "option1": "x = 2",
                        "option2": "x = 3",
                        "option3": "x = 4",
                        "option4": "x = 5",
                        "correct_option": 1
                    }
                ]
            }
        ]
    }
    """
    if request.method == 'OPTIONS':
        from flask import make_response
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response, 200
    
    # Verify role for POST requests
    verify_jwt_in_request()
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify(msg="Access denied"), 403
    
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Only JSON files are allowed."}), 400
        
        # Read and parse JSON file
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            return jsonify({"error": f"Invalid JSON format: {str(e)}"}), 400
        
        # Validate required fields
        required_fields = ['subject_name', 'chapter_name', 'quizzes']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Find or create subject
        subject = Subject.query.filter_by(name=data['subject_name']).first()
        if not subject:
            subject = Subject(
                name=data['subject_name'],
                description=f"Subject: {data['subject_name']}"
            )
            db.session.add(subject)
            db.session.commit()
        
        # Find or create chapter
        chapter = Chapter.query.filter_by(
            name=data['chapter_name'],
            subject_id=subject.id
        ).first()
        if not chapter:
            chapter = Chapter(
                name=data['chapter_name'],
                description=f"Chapter: {data['chapter_name']}",
                subject_id=subject.id
            )
            db.session.add(chapter)
            db.session.commit()
        
        created_quizzes = []
        errors = []
        
        for quiz_data in data['quizzes']:
            try:
                # Parse start datetime
                start_datetime = datetime.datetime.fromisoformat(quiz_data['start_datetime'].replace('Z', '+00:00'))
                if start_datetime.tzinfo is None:
                    start_datetime = start_datetime.replace(tzinfo=IST)
                else:
                    start_datetime = start_datetime.astimezone(IST)
                
                # Create quiz
                quiz = Quiz(
                    title=quiz_data['title'],
                    chapter_id=chapter.id,
                    start_datetime=start_datetime,
                    duration_hours=int(quiz_data.get('duration_hours', 0)),
                    duration_minutes=int(quiz_data.get('duration_minutes', 30))
                )
                db.session.add(quiz)
                db.session.flush()  # Get quiz ID
                
                # Create questions
                for question_data in quiz_data.get('questions', []):
                    question = Question(
                        quiz_id=quiz.id,
                        question_text=question_data['question_text'],
                        option1=question_data['option1'],
                        option2=question_data['option2'],
                        option3=question_data['option3'],
                        option4=question_data['option4'],
                        correct_option=int(question_data['correct_option'])
                    )
                    db.session.add(question)
                
                created_quizzes.append({
                    'id': quiz.id,
                    'title': quiz.title,
                    'questions_count': len(quiz_data.get('questions', []))
                })
                
            except Exception as e:
                errors.append(f"Error creating quiz '{quiz_data.get('title', 'Unknown')}': {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            "message": f"Successfully created {len(created_quizzes)} quizzes",
            "created_quizzes": created_quizzes,
            "errors": errors if errors else None
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500

# Enhanced Quiz Creation with File Upload for Questions
@routes.route('/api/create-quiz-with-questions', methods=['POST', 'OPTIONS'])
def create_quiz_with_questions():
    """
    Create a quiz with questions from form data or file upload
    Supports both manual question entry and file upload (JSON/TXT)
    """
    if request.method == 'OPTIONS':
        from flask import make_response
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response, 200
    
    # Verify role for POST requests
    verify_jwt_in_request()
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify(msg="Access denied"), 403
    
    try:
        # Get quiz details from form
        quiz_data = {
            'title': request.form.get('title'),
            'subject_id': int(request.form.get('subject_id')),
            'chapter_id': int(request.form.get('chapter_id')),
            'start_datetime': request.form.get('start_datetime'),
            'duration_hours': int(request.form.get('duration_hours', 0)),
            'duration_minutes': int(request.form.get('duration_minutes', 30))
        }
        
        # Validate quiz data
        if not all([quiz_data['title'], quiz_data['subject_id'], quiz_data['chapter_id'], quiz_data['start_datetime']]):
            return jsonify({"error": "Missing required quiz information"}), 400
        
        # Parse start datetime
        try:
            start_datetime = datetime.datetime.fromisoformat(quiz_data['start_datetime'].replace('Z', '+00:00'))
            if start_datetime.tzinfo is None:
                start_datetime = start_datetime.replace(tzinfo=IST)
            else:
                start_datetime = start_datetime.astimezone(IST)
        except Exception as e:
            return jsonify({"error": f"Invalid start_datetime format: {str(e)}"}), 400
        
        # Create quiz
        quiz = Quiz(
            title=quiz_data['title'],
            chapter_id=quiz_data['chapter_id'],
            start_datetime=start_datetime,
            duration_hours=quiz_data['duration_hours'],
            duration_minutes=quiz_data['duration_minutes']
        )
        db.session.add(quiz)
        db.session.flush()  # Get quiz ID
        
        questions_created = 0
        errors = []
        
        # Handle questions from file upload
        if 'questions_file' in request.files:
            file = request.files['questions_file']
            if file.filename != '' and allowed_file(file.filename):
                try:
                    if file.filename.endswith('.json'):
                        # Parse JSON questions
                        questions_data = json.load(file)
                        if isinstance(questions_data, list):
                            for question_data in questions_data:
                                try:
                                    question = Question(
                                        quiz_id=quiz.id,
                                        question_text=question_data['question_text'],
                                        option1=question_data['option1'],
                                        option2=question_data['option2'],
                                        option3=question_data['option3'],
                                        option4=question_data['option4'],
                                        correct_option=int(question_data['correct_option'])
                                    )
                                    db.session.add(question)
                                    questions_created += 1
                                except Exception as e:
                                    errors.append(f"Error creating question: {str(e)}")
                        else:
                            errors.append("JSON file should contain an array of questions")
                    
                    elif file.filename.endswith('.txt'):
                        # Parse TXT questions (simple format)
                        content = file.read().decode('utf-8')
                        lines = content.strip().split('\n')
                        
                        current_question = None
                        for line in lines:
                            line = line.strip()
                            if not line:
                                continue
                            
                            if line.startswith('Q:'):
                                # Save previous question if exists
                                if current_question and all(k in current_question for k in ['question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option']):
                                    try:
                                        question = Question(
                                            quiz_id=quiz.id,
                                            question_text=current_question['question_text'],
                                            option1=current_question['option1'],
                                            option2=current_question['option2'],
                                            option3=current_question['option3'],
                                            option4=current_question['option4'],
                                            correct_option=int(current_question['correct_option'])
                                        )
                                        db.session.add(question)
                                        questions_created += 1
                                    except Exception as e:
                                        errors.append(f"Error creating question: {str(e)}")
                                
                                # Start new question
                                current_question = {'question_text': line[2:].strip()}
                            
                            elif line.startswith('A:') and current_question:
                                current_question['option1'] = line[2:].strip()
                            elif line.startswith('B:') and current_question:
                                current_question['option2'] = line[2:].strip()
                            elif line.startswith('C:') and current_question:
                                current_question['option3'] = line[2:].strip()
                            elif line.startswith('D:') and current_question:
                                current_question['option4'] = line[2:].strip()
                            elif line.startswith('Correct:') and current_question:
                                correct_letter = line[8:].strip().upper()
                                correct_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
                                if correct_letter in correct_map:
                                    current_question['correct_option'] = correct_map[correct_letter]
                        
                        # Save last question
                        if current_question and all(k in current_question for k in ['question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option']):
                            try:
                                question = Question(
                                    quiz_id=quiz.id,
                                    question_text=current_question['question_text'],
                                    option1=current_question['option1'],
                                    option2=current_question['option2'],
                                    option3=current_question['option3'],
                                    option4=current_question['option4'],
                                    correct_option=int(current_question['correct_option'])
                                )
                                db.session.add(question)
                                questions_created += 1
                            except Exception as e:
                                errors.append(f"Error creating question: {str(e)}")
                
                except Exception as e:
                    errors.append(f"Error processing file: {str(e)}")
        
        # Handle manual questions from form
        manual_questions = request.form.get('manual_questions', '')
        if manual_questions:
            try:
                questions_list = json.loads(manual_questions)
                for question_data in questions_list:
                    try:
                        question = Question(
                            quiz_id=quiz.id,
                            question_text=question_data['question_text'],
                            option1=question_data['option1'],
                            option2=question_data['option2'],
                            option3=question_data['option3'],
                            option4=question_data['option4'],
                            correct_option=int(question_data['correct_option'])
                        )
                        db.session.add(question)
                        questions_created += 1
                    except Exception as e:
                        errors.append(f"Error creating manual question: {str(e)}")
            except json.JSONDecodeError:
                errors.append("Invalid JSON format for manual questions")
        
        db.session.commit()
        
        return jsonify({
            "message": f"Quiz created successfully with {questions_created} questions",
            "quiz": {
                "id": quiz.id,
                "title": quiz.title,
                "questions_count": questions_created
            },
            "errors": errors if errors else None
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating quiz: {str(e)}"}), 500

# Get quiz creation template
@routes.route('/api/quiz-template', methods=['GET', 'OPTIONS'])
@jwt_required(optional=True)  # Make JWT optional for CORS preflight
def get_quiz_template():
    """
    Return a template for quiz creation
    """
    if request.method == 'OPTIONS':
        from flask import make_response
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response, 200
    
    # Check admin role only for GET requests
    try:
        jwt_data = get_jwt()
        user_email = jwt_data.get('sub')
        if user_email:
            user = User.query.filter_by(email=user_email).first()
            if not user or user.role != 'admin':
                return jsonify({"error": "Admin access required"}), 403
    except:
        return jsonify({"error": "Authentication required"}), 401
    
    template = {
        "subject_name": "Example Subject",
        "chapter_name": "Example Chapter",
        "quizzes": [
            {
                "title": "Example Quiz",
                "start_datetime": "2024-01-15T10:00:00",
                "duration_hours": 1,
                "duration_minutes": 30,
                "questions": [
                    {
                        "question_text": "What is 2 + 2?",
                        "option1": "3",
                        "option2": "4",
                        "option3": "5",
                        "option4": "6",
                        "correct_option": 2
                    }
                ]
            }
        ]
    }
    
    return jsonify(template)

# Get TXT format template
@routes.route('/api/txt-template', methods=['GET', 'OPTIONS'])
@jwt_required(optional=True)  # Make JWT optional for CORS preflight
def get_txt_template():
    """
    Return a template for TXT format questions
    """
    if request.method == 'OPTIONS':
        from flask import make_response
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response, 200
    
    # Check admin role only for GET requests
    try:
        jwt_data = get_jwt()
        user_email = jwt_data.get('sub')
        if user_email:
            user = User.query.filter_by(email=user_email).first()
            if not user or user.role != 'admin':
                return jsonify({"error": "Admin access required"}), 403
    except:
        return jsonify({"error": "Authentication required"}), 401
    
    template = """Q: What is the capital of France?
A: London
B: Paris
C: Berlin
D: Madrid
Correct: B

Q: What is 2 + 2?
A: 3
B: 4
C: 5
D: 6
Correct: B

Q: Which planet is closest to the Sun?
A: Venus
B: Earth
C: Mercury
D: Mars
Correct: C"""
    
    return jsonify({"template": template})

# Notes Routes
@routes.route('/api/notes', methods=['GET'])
@role_required('user')
def get_notes():
    """Get all notes for the current user"""
    try:
        print("=== GET NOTES DEBUG ===")
        print("Request method:", request.method)
        print("Request headers:", dict(request.headers))
        
        # Get user from JWT token
        verify_jwt_in_request()
        claims = get_jwt()
        user_email = claims.get('sub')
        print("User email from JWT:", user_email)
        
        user = User.query.filter_by(email=user_email).first()
        print("User found:", user is not None)
        if user:
            print("User ID:", user.id)
        
        if not user:
            print("User not found, returning 404")
            return jsonify({"message": "User not found"}), 404
        
        notes = Notes.query.filter_by(user_id=user.id).order_by(Notes.updated_at.desc()).all()
        print("Found notes count:", len(notes))
        
        notes_data = []
        for note in notes:
            note_data = {
                "id": note.id,
                "title": note.title,
                "created_at": note.created_at.isoformat(),
                "updated_at": note.updated_at.isoformat(),
                "page_count": len(note.pages)
            }
            notes_data.append(note_data)
            print(f"Note {note.id}: {note.title} with {len(note.pages)} pages")
        
        response_data = {"notes": notes_data}
        print("Returning response:", response_data)
        return jsonify(response_data), 200
    except Exception as e:
        print("ERROR in get_notes:", str(e))
        print("Error type:", type(e))
        import traceback
        traceback.print_exc()
        return jsonify({"message": f"Error fetching notes: {str(e)}"}), 500

@routes.route('/api/notes', methods=['POST'])
@role_required('user')
def create_notes():
    """Create a new notes collection"""
    try:
        print("=== CREATE NOTES DEBUG ===")
        print("Request method:", request.method)
        print("Request headers:", dict(request.headers))
        print("Request data:", request.get_json())
        
        verify_jwt_in_request()
        claims = get_jwt()
        user_email = claims.get('sub')
        print("User email from JWT:", user_email)
        
        user = User.query.filter_by(email=user_email).first()
        print("User found:", user is not None)
        if user:
            print("User ID:", user.id)
        
        if not user:
            print("User not found, returning 404")
            return jsonify({"message": "User not found"}), 404
        
        data = request.json
        title = data.get('title', 'Untitled Notes')
        print("Creating notes with title:", title)
        
        notes = Notes(user_id=user.id, title=title)
        db.session.add(notes)
        db.session.commit()
        print("Notes created with ID:", notes.id)
        
        # Create a default first page
        first_page = NotePage(
            notes_id=notes.id,
            title="Page 1",
            content="",
            page_number=1
        )
        db.session.add(first_page)
        db.session.commit()
        print("First page created with ID:", first_page.id)
        
        response_data = {
            "message": "Notes created successfully",
            "notes": {
                "id": notes.id,
                "title": notes.title,
                "created_at": notes.created_at.isoformat(),
                "updated_at": notes.updated_at.isoformat()
            }
        }
        print("Returning response:", response_data)
        return jsonify(response_data), 201
    except Exception as e:
        print("ERROR in create_notes:", str(e))
        print("Error type:", type(e))
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({"message": f"Error creating notes: {str(e)}"}), 500

@routes.route('/api/notes/<int:notes_id>', methods=['GET'])
@role_required('user')
def get_notes_detail(notes_id):
    """Get detailed notes with all pages"""
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        user_email = claims.get('sub')
        user = User.query.filter_by(email=user_email).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        notes = Notes.query.filter_by(id=notes_id, user_id=user.id).first()
        if not notes:
            return jsonify({"message": "Notes not found"}), 404
        
        pages_data = []
        for page in notes.pages:
            page_data = {
                "id": page.id,
                "title": page.title,
                "content": page.content,
                "page_number": page.page_number,
                "created_at": page.created_at.isoformat(),
                "updated_at": page.updated_at.isoformat()
            }
            pages_data.append(page_data)
        
        # Sort pages by page number
        pages_data.sort(key=lambda x: x['page_number'])
        
        return jsonify({
            "notes": {
                "id": notes.id,
                "title": notes.title,
                "created_at": notes.created_at.isoformat(),
                "updated_at": notes.updated_at.isoformat(),
                "pages": pages_data
            }
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching notes: {str(e)}"}), 500

@routes.route('/api/notes/<int:notes_id>', methods=['PUT'])
@role_required('user')
def update_notes(notes_id):
    """Update notes title"""
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        user_email = claims.get('sub')
        user = User.query.filter_by(email=user_email).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        notes = Notes.query.filter_by(id=notes_id, user_id=user.id).first()
        if not notes:
            return jsonify({"message": "Notes not found"}), 404
        
        data = request.json
        notes.title = data.get('title', notes.title)
        notes.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "message": "Notes updated successfully",
            "notes": {
                "id": notes.id,
                "title": notes.title,
                "updated_at": notes.updated_at.isoformat()
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating notes: {str(e)}"}), 500

@routes.route('/api/notes/<int:notes_id>', methods=['DELETE'])
@role_required('user')
def delete_notes(notes_id):
    """Delete notes and all its pages"""
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        user_email = claims.get('sub')
        user = User.query.filter_by(email=user_email).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        notes = Notes.query.filter_by(id=notes_id, user_id=user.id).first()
        if not notes:
            return jsonify({"message": "Notes not found"}), 404
        
        db.session.delete(notes)
        db.session.commit()
        
        return jsonify({"message": "Notes deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting notes: {str(e)}"}), 500

@routes.route('/api/notes/<int:notes_id>/pages', methods=['POST'])
@role_required('user')
def create_note_page(notes_id):
    """Create a new page in notes"""
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        user_email = claims.get('sub')
        user = User.query.filter_by(email=user_email).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        notes = Notes.query.filter_by(id=notes_id, user_id=user.id).first()
        if not notes:
            return jsonify({"message": "Notes not found"}), 404
        
        data = request.json
        title = data.get('title', f"Page {len(notes.pages) + 1}")
        content = data.get('content', '')
        
        # Get the next page number
        max_page_number = max([page.page_number for page in notes.pages]) if notes.pages else 0
        page_number = max_page_number + 1
        
        page = NotePage(
            notes_id=notes.id,
            title=title,
            content=content,
            page_number=page_number
        )
        db.session.add(page)
        notes.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "message": "Page created successfully",
            "page": {
                "id": page.id,
                "title": page.title,
                "content": page.content,
                "page_number": page.page_number,
                "created_at": page.created_at.isoformat(),
                "updated_at": page.updated_at.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating page: {str(e)}"}), 500

@routes.route('/api/notes/<int:notes_id>/pages/<int:page_id>', methods=['PUT'])
@role_required('user')
def update_note_page(notes_id, page_id):
    """Update a note page"""
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        user_email = claims.get('sub')
        user = User.query.filter_by(email=user_email).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        notes = Notes.query.filter_by(id=notes_id, user_id=user.id).first()
        if not notes:
            return jsonify({"message": "Notes not found"}), 404
        
        page = NotePage.query.filter_by(id=page_id, notes_id=notes_id).first()
        if not page:
            return jsonify({"message": "Page not found"}), 404
        
        data = request.json
        if 'title' in data:
            page.title = data['title']
        if 'content' in data:
            page.content = data['content']
        
        page.updated_at = datetime.datetime.utcnow()
        notes.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "message": "Page updated successfully",
            "page": {
                "id": page.id,
                "title": page.title,
                "content": page.content,
                "page_number": page.page_number,
                "updated_at": page.updated_at.isoformat()
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating page: {str(e)}"}), 500

@routes.route('/api/notes/<int:notes_id>/pages/<int:page_id>', methods=['DELETE'])
@role_required('user')
def delete_note_page(notes_id, page_id):
    """Delete a note page"""
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        user_email = claims.get('sub')
        user = User.query.filter_by(email=user_email).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        notes = Notes.query.filter_by(id=notes_id, user_id=user.id).first()
        if not notes:
            return jsonify({"message": "Notes not found"}), 404
        
        page = NotePage.query.filter_by(id=page_id, notes_id=notes_id).first()
        if not page:
            return jsonify({"message": "Page not found"}), 404
        
        # Don't allow deleting the last page
        if len(notes.pages) <= 1:
            return jsonify({"message": "Cannot delete the last page"}), 400
        
        db.session.delete(page)
        notes.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        
        return jsonify({"message": "Page deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting page: {str(e)}"}), 500
