<template>
  <AdminLayout>
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">Quiz Management</h1>
          <p class="page-subtitle">Manage all quizzes in the system</p>
        </div>
        <div class="header-right">
          <div class="dropdown">
            <button @click="showCreateDropdown = !showCreateDropdown" class="btn btn-primary dropdown-toggle">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/>
              </svg>
            </button>
            <div v-if="showCreateDropdown" class="dropdown-menu">
              <button @click="showCreateModal = true; showCreateDropdown = false" class="dropdown-item">
                <i class="fas fa-edit"></i> Manual Quiz Creation
              </button>
              <button @click="showEnhancedModal = true; showCreateDropdown = false" class="dropdown-item">
                <i class="fas fa-magic"></i> Enhanced Quiz Creation
              </button>
              <button @click="showBulkModal = true; showCreateDropdown = false" class="dropdown-item">
                <i class="fas fa-upload"></i> Bulk Quiz Upload
              </button>
            </div>
          </div>
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
          placeholder="Search quizzes by title..."
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
        <select v-model="statusFilter" class="filter-select">
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
          <option value="completed">Completed</option>
        </select>
      </div>
    </div>

    <!-- Quizzes Table -->
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
          <span class="selected-count" v-if="selectedQuizzes.length > 0">
            {{ selectedQuizzes.length }} selected
          </span>
        </div>
        <div class="table-actions-right">
          <button 
            v-if="selectedQuizzes.length > 0"
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
              <th>Title</th>
              <th>Subject</th>
              <th>Chapter</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Duration</th>
              <th>Status</th>
              <th class="actions-column">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quiz in filteredQuizzes" :key="quiz.id" class="table-row">
              <td class="checkbox-column">
                <label class="checkbox-wrapper">
                  <input 
                    type="checkbox" 
                    :value="quiz.id"
                    v-model="selectedQuizzes"
                    class="checkbox"
                  />
                  <span class="checkmark"></span>
                </label>
              </td>
              <td>
                <div class="quiz-title">{{ quiz.title }}</div>
              </td>
              <td>{{ getSubjectNameFromChapter(quiz.chapter_id) }}</td>
              <td>{{ getChapterName(quiz.chapter_id) }}</td>
              <td>{{ formatDisplayDateTime(quiz.start_datetime) }}</td>
              <td>{{ formatDisplayDateTime(quiz.end_datetime) }}</td>
              <td>{{ quiz.duration_hours }}h {{ quiz.duration_minutes }}m</td>
              <td>
                <span class="status-badge" :class="`status-${quiz.status}`">
                  {{ quiz.status }}
                </span>
              </td>
              <td class="actions-column">
                <div class="action-buttons">
                  <button @click="editQuiz(quiz)" class="btn btn-icon btn-info" title="Edit">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M3 17.25V21H6.75L17.81 9.94L14.06 6.19L3 17.25ZM20.71 7.04C21.1 6.65 21.1 6.02 20.71 5.63L18.37 3.29C17.98 2.9 17.35 2.9 16.96 3.29L15.13 5.12L18.88 8.87L20.71 7.04Z" fill="currentColor"/>
                    </svg>
                  </button>
                  <button @click="toggleQuizStatus(quiz)" class="btn btn-icon btn-warning" :title="quiz.status === 'active' ? 'Deactivate' : 'Activate'">
                    <svg v-if="quiz.status === 'active'" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M6 19H18V7H6V19ZM8 9H16V17H8V9Z" fill="currentColor"/>
                    </svg>
                    <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
                    </svg>
                  </button>
                  <button @click="deleteQuiz(quiz.id)" class="btn btn-icon btn-danger" title="Delete">
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
          Showing {{ startIndex + 1 }} to {{ endIndex }} of {{ filteredQuizzes.length }} quizzes
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
      <p>Loading quizzes...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredQuizzes.length === 0" class="empty-state">
      <div class="empty-icon">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM19 19H5V5H19V19ZM7 10H9V17H7V10ZM11 7H13V17H11V7ZM15 13H17V17H15V13Z" fill="currentColor"/>
        </svg>
      </div>
      <h3>No quizzes found</h3>
      <p>Try adjusting your search or filter criteria</p>
    </div>

    <!-- Create Quiz Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Create New Quiz</h2>
          <button @click="showCreateModal = false" class="modal-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
        <form @submit.prevent="createQuiz" class="modal-form">
          <div class="form-group">
            <label>Quiz Title</label>
            <input v-model="newQuiz.title" type="text" required class="form-input" placeholder="Enter quiz title" />
          </div>
          <div class="form-group">
            <label>Subject</label>
            <select v-model="newQuiz.subject_id" required class="form-select" @change="onSubjectChange">
              <option value="">Select Subject</option>
              <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                {{ subject.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Chapter</label>
            <select v-model="newQuiz.chapter_id" required class="form-select" :disabled="!newQuiz.subject_id">
              <option value="">Select Chapter</option>
              <option v-for="chapter in filteredChapters" :key="chapter.id" :value="chapter.id">
                {{ chapter.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Start Date & Time</label>
            <input v-model="newQuiz.start_datetime" type="datetime-local" required class="form-input" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Duration (Hours)</label>
              <input v-model.number="newQuiz.duration_hours" type="number" min="0" class="form-input" placeholder="0" />
            </div>
            <div class="form-group">
              <label>Duration (Minutes)</label>
              <input v-model.number="newQuiz.duration_minutes" type="number" min="0" max="59" class="form-input" placeholder="0" />
            </div>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showCreateModal = false" class="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary">
              Create Quiz
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit Quiz Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Edit Quiz</h2>
          <button @click="showEditModal = false" class="modal-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
        <form @submit.prevent="handleUpdateQuiz" class="modal-form">
          <div class="form-group">
            <label>Quiz Title</label>
            <input v-model="editingQuiz.title" type="text" required class="form-input" placeholder="Enter quiz title" />
          </div>
          <div class="form-group">
            <label>Subject</label>
            <select v-model="editingQuiz.subject_id" required class="form-select" @change="onEditSubjectChange">
              <option value="">Select Subject</option>
              <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                {{ subject.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Chapter</label>
            <select v-model="editingQuiz.chapter_id" required class="form-select" :disabled="!editingQuiz.subject_id">
              <option value="">Select Chapter</option>
              <option v-for="chapter in filteredEditChapters" :key="chapter.id" :value="chapter.id">
                {{ chapter.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Start Date & Time</label>
            <input v-model="editingQuiz.start_datetime" type="datetime-local" required class="form-input" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Duration (Hours)</label>
              <input v-model.number="editingQuiz.duration_hours" type="number" min="0" class="form-input" placeholder="0" />
            </div>
            <div class="form-group">
              <label>Duration (Minutes)</label>
              <input v-model.number="editingQuiz.duration_minutes" type="number" min="0" max="59" class="form-input" placeholder="0" />
            </div>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showEditModal = false" class="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary">
              Update Quiz
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Enhanced Quiz Creation Modal -->
    <div v-if="showEnhancedModal" class="modal-overlay" @click="showEnhancedModal = false">
      <div class="modal-content large-modal" @click.stop>
        <div class="modal-header">
          <h2>Enhanced Quiz Creation</h2>
          <button @click="showEnhancedModal = false" class="modal-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <EnhancedQuizCreation />
        </div>
      </div>
    </div>

    <!-- Bulk Quiz Creation Modal -->
    <div v-if="showBulkModal" class="modal-overlay" @click="showBulkModal = false">
      <div class="modal-content large-modal" @click.stop>
        <div class="modal-header">
          <h2>Bulk Quiz Creation</h2>
          <button @click="showBulkModal = false" class="modal-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <BulkQuizCreation />
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import AdminLayout from './AdminLayout.vue';
import EnhancedQuizCreation from './EnhancedQuizCreation.vue';
import BulkQuizCreation from './BulkQuizCreation.vue';
import { getQuizzes, createQuiz as createQuizAPI, deleteQuiz as deleteQuizAPI, updateQuiz as updateQuizAPI, toggleQuiz, getSubjects, getChapters } from '../../api';

// Reactive data
const quizzes = ref([]);
const subjects = ref([]);
const chapters = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const subjectFilter = ref('');
const statusFilter = ref('');
const selectedQuizzes = ref([]);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const showCreateDropdown = ref(false);
const showEnhancedModal = ref(false);
const showBulkModal = ref(false);
const currentPage = ref(1);
const itemsPerPage = 10;
const errorMessage = ref('');
const successMessage = ref('');

const newQuiz = ref({
  title: '',
  subject_id: '',
  chapter_id: '',
  start_datetime: '',
  duration_hours: 0,
  duration_minutes: 0
});

const editingQuiz = ref({
  id: '',
  title: '',
  subject_id: '',
  chapter_id: '',
  start_datetime: '',
  duration_hours: 0,
  duration_minutes: 0
});

// Computed properties
const filteredQuizzes = computed(() => {
  let filtered = quizzes.value;
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(quiz => 
      quiz.title?.toLowerCase().includes(query)
    );
  }
  
  if (subjectFilter.value) {
    filtered = filtered.filter(quiz => {
      const chapter = chapters.value.find(c => c.id === quiz.chapter_id);
      return chapter && chapter.subject_id === subjectFilter.value;
    });
  }
  
  if (statusFilter.value) {
    filtered = filtered.filter(quiz => quiz.status === statusFilter.value);
  }
  
  return filtered;
});

const paginatedQuizzes = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredQuizzes.value.slice(start, end);
});

const totalPages = computed(() => Math.ceil(filteredQuizzes.value.length / itemsPerPage));
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage);
const endIndex = computed(() => Math.min(startIndex.value + itemsPerPage, filteredQuizzes.value.length));

const allSelected = computed(() => {
  return paginatedQuizzes.value.length > 0 && selectedQuizzes.value.length === paginatedQuizzes.value.length;
});

const filteredChapters = computed(() => {
  if (!newQuiz.value.subject_id) return [];
  return chapters.value.filter(chapter => chapter.subject_id === newQuiz.value.subject_id);
});

const filteredEditChapters = computed(() => {
  if (!editingQuiz.value.subject_id) return [];
  return chapters.value.filter(chapter => chapter.subject_id === editingQuiz.value.subject_id);
});

// Methods
const fetchData = async () => {
  try {
    loading.value = true;
    const [quizzesData, subjectsData, chaptersData] = await Promise.all([
      getQuizzes(),
      getSubjects(),
      getChapters()
    ]);
    
    quizzes.value = quizzesData;
    subjects.value = subjectsData;
    chapters.value = chaptersData;
  } catch (error) {
    console.error('Error fetching data:', error);
  } finally {
    loading.value = false;
  }
};

const createQuiz = async () => {
  try {
    errorMessage.value = '';
    console.log('Creating quiz with data:', newQuiz.value); // Debug log
    
    // Validate required fields
    if (!newQuiz.value.title || !newQuiz.value.chapter_id || !newQuiz.value.start_datetime) {
      errorMessage.value = 'Please fill in all required fields.';
      return;
    }
    
    const createData = {
      title: newQuiz.value.title.trim(),
      chapter_id: newQuiz.value.chapter_id,
      start_datetime: newQuiz.value.start_datetime,
      duration_hours: parseInt(newQuiz.value.duration_hours) || 0,
      duration_minutes: parseInt(newQuiz.value.duration_minutes) || 30
    };
    
    console.log('Sending create data:', createData); // Debug log
    
    await createQuizAPI(createData);
    successMessage.value = 'Quiz created successfully!';
    showCreateModal.value = false;
    newQuiz.value = {
      title: '',
      subject_id: '',
      chapter_id: '',
      start_datetime: '',
      duration_hours: 0,
      duration_minutes: 0
    };
    await fetchData();
    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
  } catch (error) {
    console.error('Error creating quiz:', error);
    console.error('Error response:', error.response); // Debug log
    errorMessage.value = error.response?.data?.message || 'Failed to create quiz. Please try again.';
  }
};

const deleteQuiz = async (quizId) => {
  if (confirm('Are you sure you want to delete this quiz?')) {
    try {
      await deleteQuizAPI(quizId);
      await fetchData();
      selectedQuizzes.value = selectedQuizzes.value.filter(id => id !== quizId);
    } catch (error) {
      console.error('Error deleting quiz:', error);
    }
  }
};

const deleteSelected = async () => {
  if (confirm(`Are you sure you want to delete ${selectedQuizzes.value.length} quizzes?`)) {
    try {
      for (const quizId of selectedQuizzes.value) {
        await deleteQuizAPI(quizId);
      }
      await fetchData();
      selectedQuizzes.value = [];
    } catch (error) {
      console.error('Error deleting quizzes:', error);
    }
  }
};

const editQuiz = (quiz) => {
  console.log('Editing quiz:', quiz); // Debug log
  
  // Format datetime for input fields
  const formatDateTimeForInput = (dateTime) => {
    if (!dateTime) return '';
    try {
      const date = new Date(dateTime);
      if (isNaN(date.getTime())) return '';
      return date.toISOString().slice(0, 16); // Format: YYYY-MM-DDTHH:MM
    } catch (error) {
      console.error('Error formatting date:', error);
      return '';
    }
  };

  editingQuiz.value = {
    id: quiz.id,
    title: quiz.title || '',
    subject_id: getSubjectIdFromChapter(quiz.chapter_id),
    chapter_id: quiz.chapter_id || '',
    start_datetime: formatDateTimeForInput(quiz.start_datetime),
    duration_hours: parseInt(quiz.duration_hours) || 0,
    duration_minutes: parseInt(quiz.duration_minutes) || 0
  };
  
  console.log('Formatted editing quiz:', editingQuiz.value); // Debug log
  showEditModal.value = true;
};

const handleUpdateQuiz = async () => {
  try {
    errorMessage.value = '';
    console.log('Updating quiz with data:', editingQuiz.value); // Debug log
    
    // Validate required fields
    if (!editingQuiz.value.title || !editingQuiz.value.chapter_id || !editingQuiz.value.start_datetime) {
      errorMessage.value = 'Please fill in all required fields.';
      return;
    }
    
    const updateData = {
      title: editingQuiz.value.title.trim(),
      chapter_id: editingQuiz.value.chapter_id,
      start_datetime: editingQuiz.value.start_datetime,
      duration_hours: parseInt(editingQuiz.value.duration_hours) || 0,
      duration_minutes: parseInt(editingQuiz.value.duration_minutes) || 0
    };
    
    console.log('Sending update data:', updateData); // Debug log
    
    await updateQuizAPI(editingQuiz.value.id, updateData);
    successMessage.value = 'Quiz updated successfully!';
    showEditModal.value = false;
    await fetchData();
    
    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
  } catch (error) {
    console.error('Error updating quiz:', error);
    console.error('Error response:', error.response); // Debug log
    
    if (error.response?.data?.message) {
      errorMessage.value = error.response.data.message;
    } else if (error.message) {
      errorMessage.value = error.message;
    } else {
      errorMessage.value = 'Failed to update quiz. Please try again.';
    }
  }
};

const toggleQuizStatus = async (quiz) => {
  try {
    console.log(`Toggling quiz ${quiz.id} status`); // Debug log
    
    // Use the toggle endpoint instead of update
    await toggleQuiz(quiz.id);
    successMessage.value = 'Quiz status toggled successfully!';
    await fetchData();
    
    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
  } catch (error) {
    console.error('Error toggling quiz status:', error);
    errorMessage.value = error.response?.data?.message || 'Failed to toggle quiz status. Please try again.';
  }
};

const toggleSelectAll = () => {
  if (allSelected.value) {
    selectedQuizzes.value = [];
  } else {
    selectedQuizzes.value = paginatedQuizzes.value.map(quiz => quiz.id);
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
  newQuiz.value.chapter_id = '';
};

const onEditSubjectChange = () => {
  editingQuiz.value.chapter_id = '';
};

const getSubjectNameFromChapter = (chapterId) => {
  const chapter = chapters.value.find(c => c.id === chapterId);
  if (!chapter) return 'N/A';
  const subject = subjects.value.find(s => s.id === chapter.subject_id);
  return subject ? subject.name : 'N/A';
};

const getChapterName = (chapterId) => {
  const chapter = chapters.value.find(c => c.id === chapterId);
  return chapter ? chapter.name : 'N/A';
};

const formatDisplayDateTime = (dateTime) => {
  if (!dateTime) return 'N/A';
  return new Date(dateTime).toLocaleString();
};

const getSubjectIdFromChapter = (chapterId) => {
  const chapter = chapters.value.find(c => c.id === chapterId);
  return chapter ? chapter.subject_id : '';
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

/* Quiz Content */
.quiz-title {
  font-weight: 500;
  color: #1A1A1A;
}

/* Status Badges */
.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.status-active {
  background: rgba(76, 175, 80, 0.1);
  color: #388E3C;
}

.status-inactive {
  background: rgba(158, 158, 158, 0.1);
  color: #616161;
}

.status-completed {
  background: rgba(33, 150, 243, 0.1);
  color: #1976D2;
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

.btn-warning {
  background: rgba(255, 152, 0, 0.1);
  color: #F57C00;
}

.btn-warning:hover {
  background: rgba(255, 152, 0, 0.2);
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

/* Message Styles */
.message {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-radius: 8px;
  margin-bottom: 24px;
  font-size: 14px;
  font-weight: 500;
  position: relative;
}

.error-message {
  background: rgba(244, 67, 54, 0.1);
  color: #D32F2F;
  border: 1px solid rgba(244, 67, 54, 0.2);
}

.success-message {
  background: rgba(76, 175, 80, 0.1);
  color: #388E3C;
  border: 1px solid rgba(76, 175, 80, 0.2);
}

.message-close {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  margin-left: auto;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.message-close:hover {
  opacity: 1;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 24px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 24px 24px 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: #F5F5F5;
  color: #1A1A1A;
}

.modal-form {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #1A1A1A;
  margin-bottom: 8px;
}

.form-input,
.form-select {
  width: 100%;
  padding: 12px;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  font-size: 14px;
  background: #F8F9FA;
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
  
  .form-row {
    grid-template-columns: 1fr;
  }
}

/* Dropdown Styles */
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.dropdown-toggle:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  z-index: 1000;
  margin-top: 4px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s ease;
  color: #333;
  font-size: 14px;
}

.dropdown-item:hover {
  background: #f5f5f5;
}

.dropdown-item i {
  width: 16px;
  color: #667eea;
}

/* Large Modal Styles */
.large-modal {
  max-width: 1000px;
  width: 90vw;
}

.modal-body {
  padding: 24px;
  max-height: 70vh;
  overflow-y: auto;
}
</style>
