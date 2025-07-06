"""
Enhanced Chatbot module for the Quiz Application with ChatGPT AI Integration
Provides intelligent responses to user queries about quizzes, navigation, and general help
"""

import re
import random
import os
from datetime import datetime
from typing import Dict, List, Tuple
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class QuizChatbot:
    def __init__(self):
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.use_openai = bool(os.getenv('OPENAI_API_KEY'))
        
        # Quiz-specific responses for common questions
        self.responses = {
            'greeting': [
                "Hello! 👋 I'm here to help you with your quiz application. How can I assist you today?",
                "Hi there! Welcome to the Quiz Master. What would you like to know?",
                "Greetings! I'm your AI assistant for the quiz platform. How can I help?",
                "Welcome! I'm your quiz assistant. Ready to help you succeed! 🎯"
            ],
            'quiz_help': [
                "To take a quiz:\n1. Go to the 'Available Quizzes' section\n2. Click on an active quiz\n3. Read the questions carefully\n4. Select your answers\n5. Submit when you're done\n\nMake sure to check the quiz duration and start time!",
                "Taking quizzes is easy! Look for quizzes marked as 'active' in your dashboard. Each quiz has a time limit, so manage your time wisely.",
                "Here's how to take a quiz:\n• Find an available quiz in your dashboard\n• Click to start when it's active\n• Answer all questions within the time limit\n• Submit your answers before time runs out",
                "Quiz Instructions:\n📝 Read each question carefully\n⏰ Watch the timer\n✅ Select your best answer\n🚀 Submit when finished\n\nGood luck! 🍀"
            ],
            'results': [
                "To view your quiz results:\n1. Go to 'Quiz History' in your dashboard\n2. You'll see all your completed quizzes\n3. Click on any quiz to see your score and performance\n\nYour results are automatically saved after each quiz!",
                "Check your quiz history to see all your past results. Each quiz shows your score and when you took it.",
                "Your quiz results are available in the Quiz History section. You can see your scores, completion dates, and performance for all quizzes you've taken.",
                "📊 View Results:\n• Go to Quiz History\n• See all your scores\n• Track your progress\n• Identify areas to improve"
            ],
            'study_tips': [
                "Here are some study tips:\n\n📚 **Review Regularly**: Go through your notes daily\n⏰ **Time Management**: Practice with timed quizzes\n🎯 **Focus Areas**: Identify your weak subjects\n📝 **Take Notes**: Write down important concepts\n🔄 **Practice**: Take practice quizzes regularly\n\nRemember, consistent practice is key to success!",
                "Study Tips for Success:\n• Create a study schedule\n• Take breaks between study sessions\n• Use practice quizzes to test your knowledge\n• Review incorrect answers to learn from mistakes\n• Stay organized with your study materials",
                "Effective Study Strategies:\n1. **Spaced Repetition**: Review material over time\n2. **Active Learning**: Engage with the content\n3. **Practice Tests**: Use quizzes to assess knowledge\n4. **Note-Taking**: Write down key points\n5. **Healthy Habits**: Get enough sleep and exercise",
                "🎓 Study Smart:\n• Break topics into smaller chunks\n• Use the Pomodoro technique (25 min study, 5 min break)\n• Create mind maps for complex topics\n• Teach concepts to others\n• Review regularly, not just before exams"
            ],
            'navigation': [
                "Here's how to navigate the app:\n\n🏠 **Dashboard**: Your main page with overview\n📚 **Subjects**: Browse available subjects\n📖 **Chapters**: View chapters within subjects\n❓ **Quizzes**: Take available quizzes\n�� **Results**: Check your performance\n👤 **Profile**: Manage your account\n\nUse the navigation menu to move between sections!",
                "Navigation Guide:\n• Dashboard: Overview and quick access\n• Subjects: Browse all available subjects\n• Chapters: View chapters in each subject\n• Quizzes: Take tests and assessments\n• History: View your past results\n• Profile: Account settings and information",
                "Getting Around:\nThe app has several main sections:\n- Dashboard for overview\n- Subjects to browse topics\n- Chapters for detailed content\n- Quizzes for testing\n- Results to track progress",
                "🗺️ App Navigation:\n• **Dashboard**: Your command center\n• **Subjects**: Explore topics\n• **Chapters**: Dive deeper\n• **Quizzes**: Test knowledge\n• **Results**: Track progress\n• **Profile**: Manage settings"
            ],
            'technical_support': [
                "For technical issues:\n\n🔧 **Clear Browser Cache**: Try refreshing or clearing cache\n🌐 **Check Internet**: Ensure stable connection\n📱 **Browser**: Use Chrome, Firefox, or Safari\n⏰ **Timing**: Make sure quizzes are active\n\nIf problems persist, contact your administrator.",
                "Technical Troubleshooting:\n• Refresh the page\n• Check your internet connection\n• Try a different browser\n• Clear browser cache and cookies\n• Ensure JavaScript is enabled",
                "Common Solutions:\n1. Refresh the page\n2. Check your internet connection\n3. Try a different browser\n4. Clear browser data\n5. Contact support if issues continue",
                "🔧 Quick Fixes:\n• Press Ctrl+F5 (hard refresh)\n• Check your internet speed\n• Try incognito/private mode\n• Update your browser\n• Disable browser extensions"
            ],
            'quiz_rules': [
                "Quiz Rules and Guidelines:\n\n⏱️ **Time Limit**: Each quiz has a specific duration\n📝 **Questions**: Read each question carefully\n✅ **Answers**: Select only one answer per question\n🚫 **No Cheating**: Don't use external resources\n💾 **Auto-Save**: Answers are saved automatically\n⏰ **Submit**: Complete before time expires\n\nGood luck with your quiz!",
                "Important Quiz Rules:\n• Respect the time limit\n• Answer all questions\n• Don't refresh during a quiz\n• Submit before time runs out\n• Use only your knowledge",
                "Quiz Guidelines:\n- Each quiz has a time limit\n- Answer all questions\n- Don't leave the page during a quiz\n- Submit when finished\n- Be honest and use your own knowledge",
                "📋 Quiz Rules:\n• ⏰ Respect time limits\n• 📝 Read questions carefully\n• ✅ Choose one answer per question\n• 🚫 No external help\n• 💾 Auto-save is enabled\n• ⏰ Submit on time"
            ],
            'motivation': [
                "You've got this! 💪 Remember:\n\n🌟 Every expert was once a beginner\n📈 Progress comes with practice\n🎯 Focus on improvement, not perfection\n💡 Mistakes are learning opportunities\n🚀 Keep pushing forward!\n\nYou're doing great!",
                "Stay motivated! 🌟\n• Learning is a journey, not a destination\n• Every quiz is a chance to grow\n• Your effort today builds your success tomorrow\n• Believe in yourself - you can do it!",
                "Keep going! 🚀\nRemember why you started. Every question you answer, every quiz you take, brings you closer to your goals. You're building knowledge that will serve you well!",
                "You're amazing! ✨\n• Every challenge makes you stronger\n• Your dedication will pay off\n• Learning is your superpower\n• Keep that positive mindset!"
            ],
            'fallback': [
                "I'm not sure I understand. Could you please rephrase your question? You can ask me about:\n• How to take quizzes\n• Viewing your results\n• Study tips\n• Navigation help\n• Technical support",
                "I didn't quite catch that. Try asking about:\n- Quiz instructions\n- Your results\n- Study advice\n- App navigation\n- Technical help",
                "I'm here to help with quiz-related questions. You can ask me about taking quizzes, viewing results, study tips, navigation, or technical support.",
                "🤔 I'm not sure about that. Try asking me about:\n• Quiz help\n• Study tips\n• Navigation\n• Results\n• Technical issues"
            ]
        }
        
        self.patterns = {
            'greeting': [
                r'\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b',
                r'\bhow are you\b',
                r'\bstart|begin\b',
                r'\bwelcome\b'
            ],
            'quiz_help': [
                r'\b(how|what|where).*quiz\b',
                r'\btake.*quiz\b',
                r'\bstart.*quiz\b',
                r'\bbegin.*quiz\b',
                r'\bquiz.*instructions\b',
                r'\bhow.*take\b',
                r'\bquiz.*help\b'
            ],
            'results': [
                r'\b(results|scores|marks|grades)\b',
                r'\bview.*results\b',
                r'\bcheck.*scores\b',
                r'\bmy.*performance\b',
                r'\bquiz.*history\b',
                r'\bsee.*results\b',
                r'\bhow.*did.*i.*do\b'
            ],
            'study_tips': [
                r'\b(study|studying|learning|tips|advice|help.*study)\b',
                r'\bhow.*study\b',
                r'\bpreparation\b',
                r'\bimprove.*score\b',
                r'\bbetter.*performance\b',
                r'\bstudy.*tips\b',
                r'\blearning.*strategies\b'
            ],
            'navigation': [
                r'\b(navigate|navigation|menu|where|go to|find)\b',
                r'\bhow.*find\b',
                r'\bwhere.*go\b',
                r'\bmenu.*options\b',
                r'\bapp.*layout\b',
                r'\bget.*around\b'
            ],
            'technical_support': [
                r'\b(error|problem|issue|bug|not working|broken)\b',
                r'\b(technical|support|help.*problem)\b',
                r'\b(crash|freeze|slow|loading)\b',
                r'\b(can\'t|cannot|unable)\b',
                r'\b(trouble|difficulty)\b'
            ],
            'quiz_rules': [
                r'\b(rules|guidelines|instructions|what.*allowed)\b',
                r'\b(cheat|cheating|external|resources)\b',
                r'\b(time.*limit|duration)\b',
                r'\b(submit|save|complete)\b',
                r'\b(quiz.*rules|guidelines)\b'
            ],
            'motivation': [
                r'\b(motivation|encouragement|inspire|motivate)\b',
                r'\b(feel.*down|discouraged|frustrated)\b',
                r'\b(need.*help|struggling)\b',
                r'\b(can\'t.*do|impossible|too hard)\b',
                r'\b(give.*up|quit)\b'
            ]
        }

    def get_response(self, user_message: str, user_context: Dict = None) -> str:
        """
        Generate an intelligent response based on user input
        
        Args:
            user_message: The user's input message
            user_context: Optional context about the user (role, recent activity, etc.)
            
        Returns:
            str: The chatbot's response
        """
        # Convert to lowercase for pattern matching
        message_lower = user_message.lower().strip()
        
        # First, check if it's a quiz-specific question
        for category, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    response = self._get_random_response(category)
                    return self._personalize_response(response, user_context)
        
        # If no quiz-specific pattern matches, use ChatGPT for general questions
        if self.use_openai:
            try:
                return self._get_chatgpt_response(user_message, user_context)
            except Exception as e:
                print(f"ChatGPT error: {str(e)}")
                # Fallback to quiz-specific response
                return self._personalize_response(self._get_random_response('fallback'), user_context)
        else:
            # If OpenAI is not configured, return fallback response
            return self._personalize_response(self._get_random_response('fallback'), user_context)
    
    def _get_chatgpt_response(self, user_message: str, user_context: Dict = None) -> str:
        """
        Get response from ChatGPT API
        """
        # Create system prompt with context about the quiz application
        system_prompt = """You are a helpful AI assistant for a quiz application called "Quiz Master". 
        
        Context about the application:
        - This is an educational quiz platform where students can take quizzes on various subjects
        - Users can view their quiz results and track their progress
        - The app has subjects, chapters, and quizzes organized hierarchically
        - There are both students and admin users
        
        Your role:
        - Help users with any questions they have
        - Be friendly, encouraging, and educational
        - If the question is about the quiz app specifically, provide accurate information
        - For general questions, provide helpful and informative responses
        - Keep responses concise but comprehensive
        - Use emojis occasionally to make responses more engaging
        - If you don't know something, be honest about it
        
        User context: """
        
        if user_context:
            if user_context.get('role') == 'admin':
                system_prompt += f"\n- This user is an admin with name: {user_context.get('name', 'Admin')}"
            elif user_context.get('role') == 'user':
                system_prompt += f"\n- This user is a student with name: {user_context.get('name', 'Student')}"
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            raise e
    
    def _get_random_response(self, category: str) -> str:
        """Get a random response from the specified category"""
        responses = self.responses.get(category, self.responses['fallback'])
        return random.choice(responses)
    
    def _personalize_response(self, response: str, user_context: Dict = None) -> str:
        """Personalize the response based on user context"""
        if not user_context:
            return response
        
        # Add personalization based on user role
        if user_context.get('role') == 'admin':
            response += "\n\n💼 As an admin, you can also manage subjects, chapters, quizzes, and users from the admin dashboard."
        elif user_context.get('role') == 'user':
            response += "\n\n👤 As a student, focus on taking quizzes and improving your scores!"
        
        # Add personalization based on user name
        if user_context.get('name'):
            response = response.replace("Hello!", f"Hello, {user_context['name']}!")
            response = response.replace("Hi there!", f"Hi there, {user_context['name']}!")
        
        return response
    
    def get_suggested_questions(self) -> List[str]:
        """Get a list of suggested questions for the user"""
        return [
            "How do I take a quiz?",
            "Where can I view my results?",
            "What are some study tips?",
            "How do I navigate the app?",
            "What are the quiz rules?",
            "I'm having technical issues",
            "I need motivation",
            "Ask me anything!"
        ]
    
    def get_welcome_message(self, user_name: str = None) -> str:
        """Get a personalized welcome message"""
        if user_name:
            return f"Welcome back, {user_name}! 👋 How can I help you with your quizzes today?"
        else:
            return "Hello! 👋 I'm your AI assistant for the Quiz Master application. How can I help you today?"

# Create a global instance
chatbot = QuizChatbot() 