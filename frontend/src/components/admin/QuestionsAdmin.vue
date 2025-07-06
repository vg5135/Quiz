<template>
  <AdminLayout>
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">Question Management</h1>
          <p class="page-subtitle">Manage all quiz questions in the system</p>
        </div>
        <div class="header-right">
          <button @click="showCreateModal = true" class="btn btn-primary">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/>
            </svg>
            Add New Question
          </button>
        </div>
      </div>
    </div>

    <!-- Error and Success Messages -->
    <div v-if="errorMessage" class="message error-message">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z" fill="currentColor"/>
      </svg>
      {{ errorMessage }}
      <button @click="errorMessage = ''" class="message-close">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
        </svg>
      </button>
    </div>

    <div v-if="successMessage" class="message success-message">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" fill="currentColor"/>
      </svg>
      {{ successMessage }}
      <button @click="successMessage = ''" class="message-close">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
        </svg>
      </button>
    </div>

    <!-- Search and Filters -->
    <div class="filters-section">
      <div class="search-box">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M15.5 14H14.71L14.43 13.73C15.41 12.59 16 11.11 16 9.5C16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16C11.11 16 12.59 15.41 13.73 14.43L14 14.71V15.5L19 20.49L20.49 19L15.5 14ZM9.5 14C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14Z" fill="currentColor"/>
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search questions by text..."
          class="search-input"
        />
      </div>
      <div class="filter-options">
        <select v-model="subjectFilter" class="filter-select">
          <option value="">All Subjects</option>
          <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
            {{ subject.name }}
          </option>
        </select>
        <select v-model="difficultyFilter" class="filter-select">
          <option value="">All Difficulties</option>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>
    </div>

    <!-- Questions Table -->
    <div class="table-container">
      <div class="table-header">
        <div class="table-actions">
          <label class="checkbox-wrapper">
            <input 
              type="checkbox" 
              :checked="allSelected" 
              @change="toggleSelectAll"
              class="checkbox"
            />
            <span class="checkmark"></span>
          </label>
          <span class="selected-count" v-if="selectedQuestions.length > 0">
            {{ selectedQuestions.length }} selected
          </span>
        </div>
        <div class="table-actions-right">
          <button 
            v-if="selectedQuestions.length > 0"
            @click="deleteSelected" 
            class="btn btn-danger btn-sm"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 19C6 20.1 6.9 21 8 21H16C17.1 21 18 20.1 18 19V7H6V19ZM8 9H16V19H8V9ZM15.5 4L14.5 3H9.5L8.5 4H5V6H19V4H15.5Z" fill="currentColor"/>
            </svg>
            Delete Selected
          </button>
        </div>
      </div>

      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th class="checkbox-column">
                <label class="checkbox-wrapper">
                  <input 
                    type="checkbox" 
                    :checked="allSelected" 
                    @change="toggleSelectAll"
                    class="checkbox"
                  />
                  <span class="checkmark"></span>
                </label>
              </th>
              <th>Question</th>
              <th>Subject</th>
              <th>Chapter</th>
              <th>Quiz</th>
              <th>Difficulty</th>
              <th>Correct Answer</th>
              <th class="actions-column">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="question in filteredQuestions" :key="question.id" class="table-row">
              <td class="checkbox-column">
                <label class="checkbox-wrapper">
                  <input 
                    type="checkbox" 
                    :value="question.id"
                    v-model="selectedQuestions"
                    class="checkbox"
                  />
                  <span class="checkmark"></span>
                </label>
              </td>
              <td>
                <div class="question-content">
                  <div class="question-text">{{ question.question_text }}</div>
                  <div class="question-options">
                    <span class="option">A: {{ question.option1 }}</span>
                    <span class="option">B: {{ question.option2 }}</span>
                    <span class="option">C: {{ question.option3 }}</span>
                    <span class="option">D: {{ question.option4 }}</span>
                  </div>
                </div>
              </td>
              <td>{{ getSubjectNameFromQuiz(question.quiz_id) }}</td>
              <td>{{ getChapterNameFromQuiz(question.quiz_id) }}</td>
              <td>{{ getQuizTitle(question.quiz_id) }}</td>
              <td>
                <span class="difficulty-badge difficulty-medium">
                  Medium
                </span>
              </td>
              <td>
                <span class="correct-answer">{{ getCorrectAnswerText(question.correct_option) }}</span>
              </td>
              <td class="actions-column">
                <div class="action-buttons">
                  <button @click="editQuestion(question)" class="btn btn-icon btn-info" title="Edit">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M3 17.25V21H6.75L17.81 9.94L14.06 6.19L3 17.25ZM20.71 7.04C21.1 6.65 21.1 6.02 20.71 5.63L18.37 3.29C17.98 2.9 17.35 2.9 16.96 3.29L15.13 5.12L18.88 8.87L20.71 7.04Z" fill="currentColor"/>
                    </svg>
                  </button>
                  <button @click="deleteQuestion(question.id)" class="btn btn-icon btn-danger" title="Delete">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M6 19C6 20.1 6.9 21 8 21H16C17.1 21 18 20.1 18 19V7H6V19ZM8 9H16V19H8V9ZM15.5 4L14.5 3H9.5L8.5 4H5V6H19V4H15.5Z" fill="currentColor"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="pagination">
        <div class="page-info">
          Showing {{ startIndex + 1 }} to {{ endIndex }} of {{ filteredQuestions.length }} questions
        </div>
        <div class="pagination-controls">
          <button 
            @click="previousPage" 
            :disabled="currentPage === 1"
            class="btn btn-secondary btn-sm"
          >
            Previous
          </button>
          <span class="page-numbers">
            Page {{ currentPage }} of {{ totalPages }}
          </span>
          <button 
            @click="nextPage" 
            :disabled="currentPage === totalPages"
            class="btn btn-secondary btn-sm"
          >
            Next
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Loading questions...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredQuestions.length === 0" class="empty-state">
      <div class="empty-icon">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M11 18H13V16H11V18ZM12 2C6.48 2 2 6.48 2 12S6.48 22 12 22 22 17.52 22 12 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12S7.59 4 12 4 20 7.59 20 12 16.41 20 12 20ZM12 6C9.79 6 8 7.79 8 10H10C10 8.9 10.9 8 12 8S14 8.9 14 10C14 12 11 11.75 11 15H13C13 12.75 16 12.5 16 10C16 7.79 14.21 6 12 6Z" fill="currentColor"/>
        </svg>
      </div>
      <h3>No questions found</h3>
      <p>Try adjusting your search or filter criteria</p>
    </div>

    <!-- Create Question Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Create New Question</h2>
          <button @click="showCreateModal = false" class="modal-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
        <form @submit.prevent="createQuestion" class="modal-form">
          <div class="form-group">
            <label>Subject</label>
            <select v-model="newQuestion.subject_id" required class="form-select" @change="onSubjectChange">
              <option value="">Select Subject</option>
              <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                {{ subject.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Chapter</label>
            <select v-model="newQuestion.chapter_id" required class="form-select" :disabled="!newQuestion.subject_id">
              <option value="">Select Chapter</option>
              <option v-for="chapter in filteredChapters" :key="chapter.id" :value="chapter.id">
                {{ chapter.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Quiz</label>
            <select v-model="newQuestion.quiz_id" required class="form-select" :disabled="!newQuestion.chapter_id">
              <option value="">Select Quiz</option>
              <option v-for="quiz in filteredQuizzes" :key="quiz.id" :value="quiz.id">
                {{ quiz.title }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Question Text</label>
            <textarea v-model="newQuestion.question_text" required class="form-input" rows="3" placeholder="Enter question text"></textarea>
          </div>
          <div class="form-group">
            <label>Option A</label>
            <input v-model="newQuestion.option1" type="text" required class="form-input" placeholder="Option A" />
          </div>
          <div class="form-group">
            <label>Option B</label>
            <input v-model="newQuestion.option2" type="text" required class="form-input" placeholder="Option B" />
          </div>
          <div class="form-group">
            <label>Option C</label>
            <input v-model="newQuestion.option3" type="text" required class="form-input" placeholder="Option C" />
          </div>
          <div class="form-group">
            <label>Option D</label>
            <input v-model="newQuestion.option4" type="text" required class="form-input" placeholder="Option D" />
          </div>
          <div class="form-group">
            <label>Correct Answer</label>
            <select v-model="newQuestion.correct_option" required class="form-select">
              <option value="">Select Answer</option>
              <option value="A">A</option>
              <option value="B">B</option>
              <option value="C">C</option>
              <option value="D">D</option>
            </select>
          </div>
          <div class="form-group">
            <label>Difficulty</label>
            <select v-model="newQuestion.difficulty" required class="form-select">
              <option value="">Select Difficulty</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showCreateModal = false" class="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary">
              Create Question
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit Question Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Edit Question</h2>
          <button @click="showEditModal = false" class="modal-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
        <form @submit.prevent="updateQuestion" class="modal-form">
          <div class="form-group">
            <label>Subject</label>
            <select v-model="editingQuestion.subject_id" required class="form-select">
              <option value="">Select Subject</option>
              <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                {{ subject.name }}
              </option>
            </select>
          </div>
                     <div class="form-group">
             <label>Chapter</label>
             <select v-model="editingQuestion.chapter_id" required class="form-select">
               <option value="">Select Chapter</option>
               <option v-for="chapter in editFilteredChapters" :key="chapter.id" :value="chapter.id">
                 {{ chapter.name }}
               </option>
             </select>
           </div>
           <div class="form-group">
             <label>Quiz</label>
             <select v-model="editingQuestion.quiz_id" required class="form-select">
               <option value="">Select Quiz</option>
               <option v-for="quiz in editFilteredQuizzes" :key="quiz.id" :value="quiz.id">
                 {{ quiz.title }}
               </option>
             </select>
           </div>
          <div class="form-group">
            <label>Question Text</label>
            <textarea v-model="editingQuestion.question_text" required class="form-input" rows="3" placeholder="Enter question text"></textarea>
          </div>
          <div class="form-group">
            <label>Option A</label>
            <input v-model="editingQuestion.option1" type="text" required class="form-input" placeholder="Option A" />
          </div>
          <div class="form-group">
            <label>Option B</label>
            <input v-model="editingQuestion.option2" type="text" required class="form-input" placeholder="Option B" />
          </div>
          <div class="form-group">
            <label>Option C</label>
            <input v-model="editingQuestion.option3" type="text" required class="form-input" placeholder="Option C" />
          </div>
          <div class="form-group">
            <label>Option D</label>
            <input v-model="editingQuestion.option4" type="text" required class="form-input" placeholder="Option D" />
          </div>
          <div class="form-group">
            <label>Correct Answer</label>
            <select v-model="editingQuestion.correct_option" required class="form-select">
              <option value="">Select Answer</option>
              <option value="A">A</option>
              <option value="B">B</option>
              <option value="C">C</option>
              <option value="D">D</option>
            </select>
          </div>
          <div class="form-group">
            <label>Difficulty</label>
            <select v-model="editingQuestion.difficulty" required class="form-select">
              <option value="">Select Difficulty</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showEditModal = false" class="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary">
              Update Question
            </button>
          </div>
        </form>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import AdminLayout from './AdminLayout.vue';
import { getQuestions, createQuestion as createQuestionAPI, updateQuestion as updateQuestionAPI, deleteQuestion as deleteQuestionAPI, getSubjects, getChapters, getQuizzes } from '../../api';

// Reactive data
const questions = ref([]);
const subjects = ref([]);
const chapters = ref([]);
const quizzes = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const subjectFilter = ref('');
const difficultyFilter = ref('');
const selectedQuestions = ref([]);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const currentPage = ref(1);
const itemsPerPage = 10;
const errorMessage = ref('');
const successMessage = ref('');

const newQuestion = ref({
  subject_id: '',
  chapter_id: '',
  quiz_id: '',
  question_text: '',
  option1: '',
  option2: '',
  option3: '',
  option4: '',
  correct_option: '',
  difficulty: ''
});

const editingQuestion = ref({
  id: null,
  subject_id: '',
  chapter_id: '',
  quiz_id: '',
  question_text: '',
  option1: '',
  option2: '',
  option3: '',
  option4: '',
  correct_option: '',
  difficulty: ''
});

// Computed properties
const filteredQuestions = computed(() => {
  let filtered = questions.value;
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(question => 
      question.question_text?.toLowerCase().includes(query) ||
      question.option1?.toLowerCase().includes(query) ||
      question.option2?.toLowerCase().includes(query) ||
      question.option3?.toLowerCase().includes(query) ||
      question.option4?.toLowerCase().includes(query)
    );
  }
  
  if (subjectFilter.value) {
    filtered = filtered.filter(question => question.subject_id === subjectFilter.value);
  }
  
  if (difficultyFilter.value) {
    filtered = filtered.filter(question => question.difficulty === difficultyFilter.value);
  }
  
  return filtered;
});

const paginatedQuestions = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredQuestions.value.slice(start, end);
});

const totalPages = computed(() => Math.ceil(filteredQuestions.value.length / itemsPerPage));
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage);
const endIndex = computed(() => Math.min(startIndex.value + itemsPerPage, filteredQuestions.value.length));

const allSelected = computed(() => {
  return paginatedQuestions.value.length > 0 && selectedQuestions.value.length === paginatedQuestions.value.length;
});

const filteredChapters = computed(() => {
  if (!newQuestion.value.subject_id) return [];
  return chapters.value.filter(chapter => chapter.subject_id === newQuestion.value.subject_id);
});

const filteredQuizzes = computed(() => {
  if (!newQuestion.value.chapter_id) return [];
  return quizzes.value.filter(quiz => quiz.chapter_id === newQuestion.value.chapter_id);
});

const editFilteredChapters = computed(() => {
  if (!editingQuestion.value.subject_id) return [];
  return chapters.value.filter(chapter => chapter.subject_id === editingQuestion.value.subject_id);
});

const editFilteredQuizzes = computed(() => {
  if (!editingQuestion.value.chapter_id) return [];
  return quizzes.value.filter(quiz => quiz.chapter_id === editingQuestion.value.chapter_id);
});

// Methods
const fetchData = async () => {
  try {
    loading.value = true;
    const [questionsData, subjectsData, chaptersData, quizzesData] = await Promise.all([
      getQuestions(),
      getSubjects(),
      getChapters(),
      getQuizzes()
    ]);
    
    questions.value = questionsData;
    subjects.value = subjectsData;
    chapters.value = chaptersData;
    quizzes.value = quizzesData;
  } catch (error) {
    console.error('Error fetching data:', error);
  } finally {
    loading.value = false;
  }
};

const createQuestion = async () => {
  try {
    console.log('Creating question with data:', newQuestion.value); // Debug log
    
    // Validate required fields
    if (!newQuestion.value.quiz_id || !newQuestion.value.question_text || 
        !newQuestion.value.option1 || !newQuestion.value.option2 || 
        !newQuestion.value.option3 || !newQuestion.value.option4 || 
        !newQuestion.value.correct_option) {
      errorMessage.value = 'Please fill in all required fields.';
      return;
    }
    
    // Convert correct_answer from A/B/C/D to 1/2/3/4
    const correctOptionMap = { 'A': 1, 'B': 2, 'C': 3, 'D': 4 };
    const correctOption = correctOptionMap[newQuestion.value.correct_option];
    
    if (!correctOption) {
      errorMessage.value = 'Please select a valid correct answer.';
      return;
    }
    
    const createData = {
      quiz_id: newQuestion.value.quiz_id,
      question_text: newQuestion.value.question_text.trim(),
      option1: newQuestion.value.option1.trim(),
      option2: newQuestion.value.option2.trim(),
      option3: newQuestion.value.option3.trim(),
      option4: newQuestion.value.option4.trim(),
      correct_option: correctOption
    };
    
    console.log('Sending create data:', createData); // Debug log
    
    await createQuestionAPI(createData);
    successMessage.value = 'Question created successfully!';
    showCreateModal.value = false;
    newQuestion.value = {
      subject_id: '',
      chapter_id: '',
      quiz_id: '',
      question_text: '',
      option1: '',
      option2: '',
      option3: '',
      option4: '',
      correct_option: '',
      difficulty: ''
    };
    await fetchData();
    
    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
  } catch (error) {
    console.error('Error creating question:', error);
    console.error('Error response:', error.response); // Debug log
    errorMessage.value = error.response?.data?.message || 'Failed to create question. Please try again.';
  }
};

const deleteQuestion = async (questionId) => {
  if (confirm('Are you sure you want to delete this question?')) {
    try {
      await deleteQuestionAPI(questionId);
      await fetchData();
      selectedQuestions.value = selectedQuestions.value.filter(id => id !== questionId);
    } catch (error) {
      console.error('Error deleting question:', error);
    }
  }
};

const deleteSelected = async () => {
  if (confirm(`Are you sure you want to delete ${selectedQuestions.value.length} questions?`)) {
    try {
      for (const questionId of selectedQuestions.value) {
        await deleteQuestionAPI(questionId);
      }
      await fetchData();
      selectedQuestions.value = [];
    } catch (error) {
      console.error('Error deleting questions:', error);
    }
  }
};

const editQuestion = (question) => {
  // Get the quiz and chapter info to populate the form
  const quiz = quizzes.value.find(q => q.id === question.quiz_id);
  const chapter = quiz ? chapters.value.find(c => c.id === quiz.chapter_id) : null;
  const subject = chapter ? subjects.value.find(s => s.id === chapter.subject_id) : null;
  
  editingQuestion.value = {
    id: question.id,
    subject_id: subject ? subject.id : '',
    chapter_id: chapter ? chapter.id : '',
    quiz_id: question.quiz_id,
    question_text: question.question_text,
    option1: question.option1,
    option2: question.option2,
    option3: question.option3,
    option4: question.option4,
    correct_option: getCorrectAnswerText(question.correct_option),
    difficulty: 'medium' // Default difficulty
  };
  showEditModal.value = true;
};

const updateQuestion = async () => {
  try {
    console.log('Updating question with data:', editingQuestion.value); // Debug log
    
    // Validate required fields
    if (!editingQuestion.value.quiz_id || !editingQuestion.value.question_text || 
        !editingQuestion.value.option1 || !editingQuestion.value.option2 || 
        !editingQuestion.value.option3 || !editingQuestion.value.option4 || 
        !editingQuestion.value.correct_option) {
      errorMessage.value = 'Please fill in all required fields.';
      return;
    }
    
    // Convert correct_answer from A/B/C/D to 1/2/3/4
    const correctOptionMap = { 'A': 1, 'B': 2, 'C': 3, 'D': 4 };
    const correctOption = correctOptionMap[editingQuestion.value.correct_option];
    
    if (!correctOption) {
      errorMessage.value = 'Please select a valid correct answer.';
      return;
    }
    
    const updateData = {
      quiz_id: editingQuestion.value.quiz_id,
      question_text: editingQuestion.value.question_text.trim(),
      option1: editingQuestion.value.option1.trim(),
      option2: editingQuestion.value.option2.trim(),
      option3: editingQuestion.value.option3.trim(),
      option4: editingQuestion.value.option4.trim(),
      correct_option: correctOption
    };
    
    console.log('Sending update data:', updateData); // Debug log
    
    await updateQuestionAPI(editingQuestion.value.id, updateData);
    successMessage.value = 'Question updated successfully!';
    showEditModal.value = false;
    await fetchData();
    
    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
  } catch (error) {
    console.error('Error updating question:', error);
    console.error('Error response:', error.response); // Debug log
    errorMessage.value = error.response?.data?.message || 'Failed to update question. Please try again.';
  }
};

const toggleSelectAll = () => {
  if (allSelected.value) {
    selectedQuestions.value = [];
  } else {
    selectedQuestions.value = paginatedQuestions.value.map(question => question.id);
  }
};

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const onSubjectChange = () => {
  newQuestion.value.chapter_id = '';
  newQuestion.value.quiz_id = '';
};

const getSubjectName = (subjectId) => {
  const subject = subjects.value.find(s => s.id === subjectId);
  return subject ? subject.name : 'N/A';
};

const getChapterName = (chapterId) => {
  const chapter = chapters.value.find(c => c.id === chapterId);
  return chapter ? chapter.name : 'N/A';
};

const getQuizTitle = (quizId) => {
  const quiz = quizzes.value.find(q => q.id === quizId);
  return quiz ? quiz.title : 'N/A';
};

const getSubjectNameFromQuiz = (quizId) => {
  const quiz = quizzes.value.find(q => q.id === quizId);
  if (!quiz) return 'N/A';
  const chapter = chapters.value.find(c => c.id === quiz.chapter_id);
  if (!chapter) return 'N/A';
  const subject = subjects.value.find(s => s.id === chapter.subject_id);
  return subject ? subject.name : 'N/A';
};

const getChapterNameFromQuiz = (quizId) => {
  const quiz = quizzes.value.find(q => q.id === quizId);
  if (!quiz) return 'N/A';
  const chapter = chapters.value.find(c => c.id === quiz.chapter_id);
  return chapter ? chapter.name : 'N/A';
};

const getCorrectAnswerText = (correctOption) => {
  const optionMap = { 1: 'A', 2: 'B', 3: 'C', 4: 'D' };
  return optionMap[correctOption] || 'N/A';
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
/* Page Header */
.page-header {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #E0E0E0;
  width: 100%;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0 0 4px 0;
}

.page-subtitle {
  font-size: 14px;
  color: #666;
  margin: 0;
}

/* Filters Section */
.filters-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #E0E0E0;
  display: flex;
  gap: 16px;
  align-items: center;
  width: 100%;
}

.search-box {
  flex: 1;
  position: relative;
  max-width: 400px;
}

.search-box svg {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.search-input {
  width: 100%;
  padding: 12px 12px 12px 40px;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  font-size: 14px;
  background: #F8F9FA;
}

.search-input:focus {
  outline: none;
  border-color: #1976D2;
  background: white;
}

.filter-select {
  padding: 12px;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  font-size: 14px;
  background: #F8F9FA;
  min-width: 120px;
}

.filter-select:focus {
  outline: none;
  border-color: #1976D2;
  background: white;
}

/* Table Container */
.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #E0E0E0;
  overflow: hidden;
  width: 100%;
}

.table-header {
  padding: 16px 24px;
  border-bottom: 1px solid #E0E0E0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #F8F9FA;
}

.table-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.selected-count {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.table-actions-right {
  display: flex;
  gap: 8px;
}

.table-wrapper {
  overflow-x: auto;
  width: 100%;
}

/* Data Table */
.data-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 100%;
}

.data-table th {
  background: #F8F9FA;
  padding: 16px 24px;
  text-align: left;
  font-size: 14px;
  font-weight: 600;
  color: #1A1A1A;
  border-bottom: 1px solid #E0E0E0;
}

.data-table td {
  padding: 16px 24px;
  border-bottom: 1px solid #F0F0F0;
  font-size: 14px;
  color: #1A1A1A;
}

.data-table tr:hover {
  background: #F8F9FA;
}

.checkbox-column {
  width: 48px;
}

.actions-column {
  width: 120px;
}

/* Checkbox Styles */
.checkbox-wrapper {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.checkbox {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.checkmark {
  height: 18px;
  width: 18px;
  background-color: white;
  border: 2px solid #E0E0E0;
  border-radius: 4px;
  display: inline-block;
  position: relative;
  transition: all 0.2s ease;
}

.checkbox:checked ~ .checkmark {
  background-color: #1976D2;
  border-color: #1976D2;
}

.checkbox:checked ~ .checkmark:after {
  content: '';
  position: absolute;
  left: 5px;
  top: 2px;
  width: 4px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

/* Question Content */
.question-content {
  max-width: 300px;
}

.question-text {
  font-weight: 500;
  color: #1A1A1A;
  margin-bottom: 8px;
  line-height: 1.4;
}

.question-options {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.option {
  font-size: 12px;
  color: #666;
}

/* Badges */
.difficulty-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.difficulty-easy {
  background: rgba(76, 175, 80, 0.1);
  color: #388E3C;
}

.difficulty-medium {
  background: rgba(255, 152, 0, 0.1);
  color: #F57C00;
}

.difficulty-hard {
  background: rgba(244, 67, 54, 0.1);
  color: #D32F2F;
}

.correct-answer {
  font-weight: 600;
  color: #1976D2;
  background: rgba(25, 118, 210, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 8px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.btn-primary {
  background: #1976D2;
  color: white;
}

.btn-primary:hover {
  background: #1565C0;
}

.btn-secondary {
  background: #F5F5F5;
  color: #666;
}

.btn-secondary:hover {
  background: #E0E0E0;
}

.btn-danger {
  background: rgba(244, 67, 54, 0.1);
  color: #D32F2F;
}

.btn-danger:hover {
  background: rgba(244, 67, 54, 0.2);
}

.btn-info {
  background: rgba(33, 150, 243, 0.1);
  color: #1976D2;
}

.btn-info:hover {
  background: rgba(33, 150, 243, 0.2);
}

.btn-icon {
  padding: 8px;
  min-width: 32px;
  justify-content: center;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Pagination */
.pagination {
  padding: 20px 24px;
  border-top: 1px solid #E0E0E0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #F8F9FA;
}

.page-info {
  font-size: 14px;
  color: #666;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-numbers {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

/* Loading and Empty States */
.loading-state,
.empty-state {
  text-align: center;
  padding: 60px 24px;
  color: #666;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #E3F2FD;
  border-left: 4px solid #1976D2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-icon {
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0 0 8px 0;
}

.empty-state p {
  font-size: 14px;
  margin: 0;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #E0E0E0;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #1A1A1A;
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  color: #666;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #F5F5F5;
  color: #333;
}

.modal-form {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.form-input,
.form-select {
  width: 100%;
  padding: 12px;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  font-size: 14px;
  background: #F8F9FA;
  transition: all 0.2s;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #1976D2;
  background: white;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #E0E0E0;
}

/* Message Styles */
.message {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-radius: 8px;
  margin-bottom: 24px;
  font-size: 14px;
  position: relative;
}

.error-message {
  background: #FEF2F2;
  border: 1px solid #FECACA;
  color: #DC2626;
}

.success-message {
  background: #F0FDF4;
  border: 1px solid #BBF7D0;
  color: #16A34A;
}

.message-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  color: inherit;
  opacity: 0.7;
  transition: opacity 0.2s;
  margin-left: auto;
}

.message-close:hover {
  opacity: 1;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    max-width: none;
  }
  
  .table-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .pagination {
    flex-direction: column;
    gap: 12px;
    align-items: center;
  }
  
  .data-table {
    font-size: 12px;
  }
  
  .data-table th,
  .data-table td {
    padding: 12px 16px;
  }
  
  .modal-content {
    margin: 16px;
    max-width: none;
  }
}
</style>
