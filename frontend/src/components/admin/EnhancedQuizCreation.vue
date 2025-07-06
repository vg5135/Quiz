<template>
  <div class="enhanced-quiz-creation">
    <div class="card">
      <div class="card-header">
        <h3>📝 Enhanced Quiz Creation</h3>
        <p class="text-muted">Create a quiz with manual input or file upload for questions</p>
      </div>
      
      <div class="card-body">
        <!-- Quiz Details Form -->
        <div class="quiz-details-section">
          <h4>📋 Quiz Information</h4>
          <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <label>Quiz Title *</label>
                <input 
                  v-model="quizData.title" 
                  type="text" 
                  class="form-control" 
                  placeholder="Enter quiz title"
                >
              </div>
            </div>
            <div class="col-md-6">
              <div class="form-group">
                <label>Start Date & Time *</label>
                <input 
                  v-model="quizData.start_datetime" 
                  type="datetime-local" 
                  class="form-control"
                >
              </div>
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-4">
              <div class="form-group">
                <label>Subject *</label>
                <select v-model="quizData.subject_id" @change="loadChapters" class="form-control">
                  <option value="">Select Subject</option>
                  <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                    {{ subject.name }}
                  </option>
                </select>
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-group">
                <label>Chapter *</label>
                <select v-model="quizData.chapter_id" class="form-control" :disabled="!quizData.subject_id">
                  <option value="">Select Chapter</option>
                  <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
                    {{ chapter.name }}
                  </option>
                </select>
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-group">
                <label>Duration</label>
                <div class="duration-inputs">
                  <input 
                    v-model="quizData.duration_hours" 
                    type="number" 
                    class="form-control" 
                    placeholder="Hours"
                    min="0"
                  >
                  <span class="duration-separator">:</span>
                  <input 
                    v-model="quizData.duration_minutes" 
                    type="number" 
                    class="form-control" 
                    placeholder="Minutes"
                    min="0"
                    max="59"
                  >
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Questions Section -->
        <div class="questions-section">
          <h4>❓ Questions</h4>
          
          <!-- Question Input Method Tabs -->
          <div class="input-method-tabs">
            <button 
              @click="activeTab = 'manual'" 
              :class="['tab-btn', { active: activeTab === 'manual' }]"
            >
              <i class="fas fa-edit"></i> Manual Input
            </button>
            <button 
              @click="activeTab = 'file'" 
              :class="['tab-btn', { active: activeTab === 'file' }]"
            >
              <i class="fas fa-file-upload"></i> File Upload
            </button>
          </div>

          <!-- Manual Input Tab -->
          <div v-if="activeTab === 'manual'" class="manual-input-tab">
            <div class="manual-questions">
              <div v-for="(question, index) in manualQuestions" :key="index" class="question-item">
                <div class="question-header">
                  <h5>Question {{ index + 1 }}</h5>
                  <button @click="removeQuestion(index)" class="btn btn-sm btn-outline-danger">
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
                
                <div class="form-group">
                  <label>Question Text</label>
                  <textarea 
                    v-model="question.question_text" 
                    class="form-control" 
                    rows="3"
                    placeholder="Enter your question here..."
                  ></textarea>
                </div>
                
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label>Option A</label>
                      <input v-model="question.option1" type="text" class="form-control">
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group">
                      <label>Option B</label>
                      <input v-model="question.option2" type="text" class="form-control">
                    </div>
                  </div>
                </div>
                
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label>Option C</label>
                      <input v-model="question.option3" type="text" class="form-control">
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group">
                      <label>Option D</label>
                      <input v-model="question.option4" type="text" class="form-control">
                    </div>
                  </div>
                </div>
                
                <div class="form-group">
                  <label>Correct Answer</label>
                  <select v-model="question.correct_option" class="form-control">
                    <option value="">Select correct answer</option>
                    <option value="1">A</option>
                    <option value="2">B</option>
                    <option value="3">C</option>
                    <option value="4">D</option>
                  </select>
                </div>
              </div>
              
              <button @click="addQuestion" class="btn btn-outline-primary">
                <i class="fas fa-plus"></i> Add Question
              </button>
            </div>
          </div>

          <!-- File Upload Tab -->
          <div v-if="activeTab === 'file'" class="file-upload-tab">
            <div class="file-upload-area" @click="triggerFileInput" @drop="handleDrop" @dragover.prevent>
              <input 
                ref="fileInput" 
                type="file" 
                accept=".json,.txt" 
                @change="handleFileSelect" 
                style="display: none;"
              >
              <div class="upload-content">
                <i class="fas fa-cloud-upload-alt"></i>
                <p>Click to select or drag & drop your file</p>
                <small class="text-muted">Supports .json and .txt files</small>
              </div>
            </div>
            
            <div v-if="selectedFile" class="selected-file">
              <i class="fas fa-file-alt"></i>
              <span>{{ selectedFile.name }}</span>
              <button @click="removeFile" class="btn btn-sm btn-outline-danger">
                <i class="fas fa-times"></i>
              </button>
            </div>

            <!-- File Format Templates -->
            <div class="template-section">
              <h5>📋 File Format Templates</h5>
              <div class="template-buttons">
                <button @click="downloadJsonTemplate" class="btn btn-outline-secondary">
                  <i class="fas fa-download"></i> JSON Template
                </button>
                <button @click="downloadTxtTemplate" class="btn btn-outline-secondary">
                  <i class="fas fa-download"></i> TXT Template
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button 
            @click="createQuiz" 
            :disabled="!isFormValid || creating" 
            class="btn btn-primary"
          >
            <i v-if="creating" class="fas fa-spinner fa-spin"></i>
            <i v-else class="fas fa-save"></i>
            {{ creating ? 'Creating Quiz...' : 'Create Quiz' }}
          </button>
        </div>

        <!-- Results Section -->
        <div v-if="creationResult" class="results-section">
          <div :class="['alert', creationResult.success ? 'alert-success' : 'alert-danger']">
            <h5>{{ creationResult.message }}</h5>
            
            <div v-if="creationResult.quiz" class="quiz-info">
              <p><strong>Quiz ID:</strong> {{ creationResult.quiz.id }}</p>
              <p><strong>Title:</strong> {{ creationResult.quiz.title }}</p>
              <p><strong>Questions Created:</strong> {{ creationResult.quiz.questions_count }}</p>
            </div>
            
            <div v-if="creationResult.errors" class="errors">
              <h6>Errors:</h6>
              <ul>
                <li v-for="error in creationResult.errors" :key="error">{{ error }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'EnhancedQuizCreation',
  setup() {
    const quizData = ref({
      title: '',
      subject_id: '',
      chapter_id: '',
      start_datetime: '',
      duration_hours: 0,
      duration_minutes: 30
    })
    
    const subjects = ref([])
    const chapters = ref([])
    const activeTab = ref('manual')
    const manualQuestions = ref([{
      question_text: '',
      option1: '',
      option2: '',
      option3: '',
      option4: '',
      correct_option: ''
    }])
    
    const selectedFile = ref(null)
    const fileInput = ref(null)
    const creating = ref(false)
    const creationResult = ref(null)

    const isFormValid = computed(() => {
      return quizData.value.title && 
             quizData.value.subject_id && 
             quizData.value.chapter_id && 
             quizData.value.start_datetime &&
             (activeTab.value === 'file' ? selectedFile.value : manualQuestions.value.length > 0)
    })

    onMounted(async () => {
      await loadSubjects()
    })

    const loadSubjects = async () => {
      try {
        const response = await fetch('http://localhost:5006/api/subjects', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        const data = await response.json()
        subjects.value = data
      } catch (error) {
        console.error('Error loading subjects:', error)
      }
    }

    const loadChapters = async () => {
      if (!quizData.value.subject_id) {
        chapters.value = []
        quizData.value.chapter_id = ''
        return
      }
      
      try {
        const response = await fetch('http://localhost:5006/api/chapters', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        const data = await response.json()
        chapters.value = data.filter(chapter => 
          chapter.subject_id === quizData.value.subject_id
        )
      } catch (error) {
        console.error('Error loading chapters:', error)
      }
    }

    const addQuestion = () => {
      manualQuestions.value.push({
        question_text: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: ''
      })
    }

    const removeQuestion = (index) => {
      if (manualQuestions.value.length > 1) {
        manualQuestions.value.splice(index, 1)
      }
    }

    const triggerFileInput = () => {
      fileInput.value.click()
    }

    const handleFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        selectedFile.value = file
      }
    }

    const handleDrop = (event) => {
      event.preventDefault()
      const file = event.dataTransfer.files[0]
      if (file && (file.name.endsWith('.json') || file.name.endsWith('.txt'))) {
        selectedFile.value = file
      }
    }

    const removeFile = () => {
      selectedFile.value = null
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }

    const downloadJsonTemplate = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) {
          alert('Please log in first to download templates')
          return
        }

        const response = await fetch('http://localhost:5006/api/quiz-template', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
        
        if (!response.ok) {
          if (response.status === 401) {
            alert('Authentication failed. Please log in again.')
            window.location.href = '/login'
            return
          }
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const template = await response.json()
        const questions = template.quizzes[0].questions
        
        const blob = new Blob([JSON.stringify(questions, null, 2)], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'questions_template.json'
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
        
        console.log('JSON template downloaded successfully')
      } catch (error) {
        console.error('Error downloading template:', error)
        alert('Error downloading template: ' + error.message)
      }
    }

    const downloadTxtTemplate = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) {
          alert('Please log in first to download templates')
          return
        }

        const response = await fetch('http://localhost:5006/api/txt-template', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
        
        if (!response.ok) {
          if (response.status === 401) {
            alert('Authentication failed. Please log in again.')
            window.location.href = '/login'
            return
          }
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const template = await response.json()
        
        const blob = new Blob([template.template], { type: 'text/plain' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'questions_template.txt'
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
        
        console.log('TXT template downloaded successfully')
      } catch (error) {
        console.error('Error downloading template:', error)
        alert('Error downloading template: ' + error.message)
      }
    }

    const createQuiz = async () => {
      creating.value = true
      creationResult.value = null

      try {
        const formData = new FormData()
        
        // Add quiz details
        Object.keys(quizData.value).forEach(key => {
          formData.append(key, quizData.value[key])
        })
        
        // Add questions based on active tab
        if (activeTab.value === 'manual') {
          formData.append('manual_questions', JSON.stringify(manualQuestions.value))
        } else if (activeTab.value === 'file' && selectedFile.value) {
          formData.append('questions_file', selectedFile.value)
        }

        const response = await fetch('http://localhost:5006/api/create-quiz-with-questions', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: formData
        })

        const result = await response.json()
        
        if (response.ok) {
          creationResult.value = {
            success: true,
            message: result.message,
            quiz: result.quiz,
            errors: result.errors
          }
          
          // Reset form on success
          if (creationResult.value.success) {
            resetForm()
          }
        } else {
          creationResult.value = {
            success: false,
            message: result.error || 'Error creating quiz',
            errors: [result.error || 'Unknown error occurred']
          }
        }
      } catch (error) {
        console.error('Error creating quiz:', error)
        creationResult.value = {
          success: false,
          message: 'Error creating quiz',
          errors: ['Network error occurred']
        }
      } finally {
        creating.value = false
      }
    }

    const resetForm = () => {
      quizData.value = {
        title: '',
        subject_id: '',
        chapter_id: '',
        start_datetime: '',
        duration_hours: 0,
        duration_minutes: 30
      }
      manualQuestions.value = [{
        question_text: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: ''
      }]
      selectedFile.value = null
      activeTab.value = 'manual'
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }

    return {
      quizData,
      subjects,
      chapters,
      activeTab,
      manualQuestions,
      selectedFile,
      fileInput,
      creating,
      creationResult,
      isFormValid,
      loadSubjects,
      loadChapters,
      addQuestion,
      removeQuestion,
      triggerFileInput,
      handleFileSelect,
      handleDrop,
      removeFile,
      downloadJsonTemplate,
      downloadTxtTemplate,
      createQuiz
    }
  }
}
</script>

<style scoped>
.enhanced-quiz-creation {
  max-width: 1000px;
  margin: 0 auto;
}

.card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 8px 8px 0 0;
}

.card-header h3 {
  margin: 0;
  font-weight: 600;
}

.card-body {
  padding: 2rem;
}

.quiz-details-section, .questions-section {
  margin-bottom: 2rem;
}

.quiz-details-section h4, .questions-section h4 {
  color: #333;
  margin-bottom: 1rem;
  font-weight: 600;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  font-weight: 500;
  color: #495057;
  margin-bottom: 0.5rem;
}

.form-control {
  border: 1px solid #ced4da;
  border-radius: 6px;
  padding: 0.75rem;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.duration-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.duration-separator {
  font-weight: bold;
  color: #666;
}

.input-method-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.tab-btn {
  padding: 0.75rem 1.5rem;
  border: 2px solid #e9ecef;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.tab-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.tab-btn.active {
  border-color: #667eea;
  background: #667eea;
  color: white;
}

.question-item {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  background: #f8f9fa;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-header h5 {
  margin: 0;
  color: #495057;
}

.file-upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fafafa;
}

.file-upload-area:hover {
  border-color: #667eea;
  background: #f0f4ff;
}

.upload-content i {
  font-size: 3rem;
  color: #667eea;
  margin-bottom: 1rem;
}

.selected-file {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 0.75rem;
  background: #e8f5e8;
  border-radius: 6px;
  border: 1px solid #c3e6c3;
}

.template-section {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 6px;
}

.template-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.action-buttons {
  text-align: center;
  margin: 2rem 0;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.results-section {
  margin-top: 2rem;
}

.alert {
  padding: 1rem;
  border-radius: 6px;
  border: 1px solid;
}

.alert-success {
  background: #d4edda;
  border-color: #c3e6c3;
  color: #155724;
}

.alert-danger {
  background: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
}

.quiz-info p {
  margin-bottom: 0.5rem;
}

.errors {
  margin-top: 1rem;
}

.errors h6 {
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.errors ul {
  margin: 0;
  padding-left: 1.5rem;
}

.errors li {
  margin-bottom: 0.25rem;
}

@media (max-width: 768px) {
  .card-body {
    padding: 1rem;
  }
  
  .input-method-tabs {
    flex-direction: column;
  }
  
  .template-buttons {
    flex-direction: column;
  }
  
  .duration-inputs {
    flex-direction: column;
    gap: 0.25rem;
  }
}
</style> 