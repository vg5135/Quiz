from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import create_access_token, decode_token, get_jwt, jwt_required
from models import db, bcrypt, Subject, Quiz, Question, Score, User, Chapter
from rbac import role_required
import datetime

# Define IST timezone
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))

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
