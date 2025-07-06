<template>
  <div class="bulk-quiz-creation">
    <div class="card">
      <div class="card-header">
        <h3>📁 Bulk Quiz Creation</h3>
        <p class="text-muted">Upload a JSON file to create multiple quizzes at once</p>
      </div>
      
      <div class="card-body">
        <!-- File Upload Section -->
        <div class="upload-section">
          <h4>📤 Upload JSON File</h4>
          <div class="file-upload-area" @click="triggerFileInput" @drop="handleDrop" @dragover.prevent>
            <input 
              ref="fileInput" 
              type="file" 
              accept=".json" 
              @change="handleFileSelect" 
              style="display: none;"
            >
            <div class="upload-content">
              <i class="fas fa-cloud-upload-alt"></i>
              <p>Click to select or drag & drop your JSON file</p>
              <small class="text-muted">Only .json files are supported</small>
            </div>
          </div>
          
          <div v-if="selectedFile" class="selected-file">
            <i class="fas fa-file-alt"></i>
            <span>{{ selectedFile.name }}</span>
            <button @click="removeFile" class="btn btn-sm btn-outline-danger">
              <i class="fas fa-times"></i>
            </button>
          </div>
        </div>

        <!-- Template Download Section -->
        <div class="template-section">
          <h4>📋 Get Template</h4>
          <p>Download a template to see the required JSON format:</p>
          <button @click="downloadTemplate" class="btn btn-outline-primary">
            <i class="fas fa-download"></i> Download JSON Template
          </button>
        </div>

        <!-- Preview Section -->
        <div v-if="previewData" class="preview-section">
          <h4>👀 Preview</h4>
          <div class="preview-content">
            <div class="preview-item">
              <strong>Subject:</strong> {{ previewData.subject_name }}
            </div>
            <div class="preview-item">
              <strong>Chapter:</strong> {{ previewData.chapter_name }}
            </div>
            <div class="preview-item">
              <strong>Quizzes:</strong> {{ previewData.quizzes.length }}
            </div>
            <div class="preview-item">
              <strong>Total Questions:</strong> {{ totalQuestions }}
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button 
            @click="uploadFile" 
            :disabled="!selectedFile || uploading" 
            class="btn btn-primary"
          >
            <i v-if="uploading" class="fas fa-spinner fa-spin"></i>
            <i v-else class="fas fa-upload"></i>
            {{ uploading ? 'Creating Quizzes...' : 'Create Quizzes' }}
          </button>
        </div>

        <!-- Results Section -->
        <div v-if="uploadResult" class="results-section">
          <div :class="['alert', uploadResult.success ? 'alert-success' : 'alert-danger']">
            <h5>{{ uploadResult.message }}</h5>
            
            <div v-if="uploadResult.created_quizzes" class="created-quizzes">
              <h6>Created Quizzes:</h6>
              <ul>
                <li v-for="quiz in uploadResult.created_quizzes" :key="quiz.id">
                  {{ quiz.title }} ({{ quiz.questions_count }} questions)
                </li>
              </ul>
            </div>
            
            <div v-if="uploadResult.errors" class="errors">
              <h6>Errors:</h6>
              <ul>
                <li v-for="error in uploadResult.errors" :key="error">{{ error }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { getSubjects, getChapters } from '../../api.js'

export default {
  name: 'BulkQuizCreation',
  setup() {
    const selectedFile = ref(null)
    const previewData = ref(null)
    const uploading = ref(false)
    const uploadResult = ref(null)
    const fileInput = ref(null)

    const totalQuestions = computed(() => {
      if (!previewData.value) return 0
      return previewData.value.quizzes.reduce((total, quiz) => {
        return total + (quiz.questions ? quiz.questions.length : 0)
      }, 0)
    })

    const triggerFileInput = () => {
      fileInput.value.click()
    }

    const handleFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        processFile(file)
      }
    }

    const handleDrop = (event) => {
      event.preventDefault()
      const file = event.dataTransfer.files[0]
      if (file && file.name.endsWith('.json')) {
        processFile(file)
      }
    }

    const processFile = (file) => {
      selectedFile.value = file
      previewData.value = null
      uploadResult.value = null

      const reader = new FileReader()
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result)
          previewData.value = data
        } catch (error) {
          alert('Invalid JSON file: ' + error.message)
          selectedFile.value = null
        }
      }
      reader.readAsText(file)
    }

    const removeFile = () => {
      selectedFile.value = null
      previewData.value = null
      uploadResult.value = null
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }

    const downloadTemplate = async () => {
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
            // Redirect to login
            window.location.href = '/login'
            return
          }
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const template = await response.json()
        
        const blob = new Blob([JSON.stringify(template, null, 2)], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'quiz_template.json'
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
        
        console.log('Template downloaded successfully')
      } catch (error) {
        console.error('Error downloading template:', error)
        alert('Error downloading template: ' + error.message)
      }
    }

    const uploadFile = async () => {
      if (!selectedFile.value) return

      uploading.value = true
      uploadResult.value = null

      try {
        const formData = new FormData()
        formData.append('file', selectedFile.value)

        const response = await fetch('http://localhost:5006/api/bulk-create-quiz', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: formData
        })

        const result = await response.json()
        
        if (response.ok) {
          uploadResult.value = {
            success: true,
            message: result.message,
            created_quizzes: result.created_quizzes,
            errors: result.errors
          }
        } else {
          uploadResult.value = {
            success: false,
            message: result.error || 'Error creating quizzes',
            errors: [result.error || 'Unknown error occurred']
          }
        }
      } catch (error) {
        console.error('Error uploading file:', error)
        uploadResult.value = {
          success: false,
          message: 'Error creating quizzes',
          errors: ['Network error occurred']
        }
      } finally {
        uploading.value = false
      }
    }

    return {
      selectedFile,
      previewData,
      uploading,
      uploadResult,
      fileInput,
      totalQuestions,
      triggerFileInput,
      handleFileSelect,
      handleDrop,
      removeFile,
      downloadTemplate,
      uploadFile
    }
  }
}
</script>

<style scoped>
.bulk-quiz-creation {
  max-width: 800px;
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

.upload-section, .template-section, .preview-section {
  margin-bottom: 2rem;
}

.upload-section h4, .template-section h4, .preview-section h4 {
  color: #333;
  margin-bottom: 1rem;
  font-weight: 600;
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

.upload-content p {
  margin: 0.5rem 0;
  font-weight: 500;
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

.selected-file i {
  color: #28a745;
}

.template-section p {
  color: #666;
  margin-bottom: 1rem;
}

.preview-content {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.preview-item {
  margin-bottom: 0.5rem;
}

.preview-item strong {
  color: #495057;
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

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.btn-outline-primary {
  border-color: #667eea;
  color: #667eea;
}

.btn-outline-primary:hover {
  background: #667eea;
  border-color: #667eea;
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

.created-quizzes, .errors {
  margin-top: 1rem;
}

.created-quizzes h6, .errors h6 {
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.created-quizzes ul, .errors ul {
  margin: 0;
  padding-left: 1.5rem;
}

.created-quizzes li, .errors li {
  margin-bottom: 0.25rem;
}

@media (max-width: 768px) {
  .card-body {
    padding: 1rem;
  }
  
  .file-upload-area {
    padding: 1.5rem;
  }
  
  .upload-content i {
    font-size: 2rem;
  }
}
</style> 