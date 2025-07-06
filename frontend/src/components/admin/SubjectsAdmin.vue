<template>
  <AdminLayout>
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">Subject Management</h1>
          <p class="page-subtitle">Manage all subjects in the system</p>
        </div>
        <div class="header-right">
          <button @click="showCreateModal = true" class="btn btn-primary">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/>
            </svg>
            Add New Subject
          </button>
        </div>
      </div>
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
          placeholder="Search subjects by name..."
          class="search-input"
        />
      </div>
    </div>

    <!-- Subjects Table -->
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
          <span class="selected-count" v-if="selectedSubjects.length > 0">
            {{ selectedSubjects.length }} selected
          </span>
        </div>
        <div class="table-actions-right">
          <button 
            v-if="selectedSubjects.length > 0"
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
              <th>Subject Name</th>
              <th>Description</th>
              <th>Chapters Count</th>
              <th>Quizzes Count</th>
              <th class="actions-column">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="subject in filteredSubjects" :key="subject.id" class="table-row">
              <td class="checkbox-column">
                <label class="checkbox-wrapper">
                  <input 
                    type="checkbox" 
                    :value="subject.id"
                    v-model="selectedSubjects"
                    class="checkbox"
                  />
                  <span class="checkmark"></span>
                </label>
              </td>
              <td>
                <div class="subject-name">{{ subject.name }}</div>
              </td>
              <td>
                <div class="subject-description">
                  {{ subject.description || 'No description' }}
                </div>
              </td>
              <td>
                <span class="chapter-count">{{ subject.chapters?.length || 0 }} chapters</span>
              </td>
              <td>
                <span class="quiz-count">{{ getTotalQuizzes(subject) }} quizzes</span>
              </td>
              <td class="actions-column">
                <div class="action-buttons">
                  <button @click="editSubject(subject)" class="btn btn-icon btn-info" title="Edit">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M3 17.25V21H6.75L17.81 9.94L14.06 6.19L3 17.25ZM20.71 7.04C21.1 6.65 21.1 6.02 20.71 5.63L18.37 3.29C17.98 2.9 17.35 2.9 16.96 3.29L15.13 5.12L18.88 8.87L20.71 7.04Z" fill="currentColor"/>
                    </svg>
                  </button>
                  <button @click="deleteSubject(subject.id)" class="btn btn-icon btn-danger" title="Delete">
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
          Showing {{ startIndex + 1 }} to {{ endIndex }} of {{ filteredSubjects.length }} subjects
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
      <p>Loading subjects...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredSubjects.length === 0" class="empty-state">
      <div class="empty-icon">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 3L1 9L5 11.18V17H7V12.18L12 15L17 12.18V17H19V11.18L23 9L12 3ZM12 13L3 9L12 5L21 9L12 13Z" fill="currentColor"/>
        </svg>
      </div>
      <h3>No subjects found</h3>
      <p>Try adjusting your search criteria</p>
    </div>

    <!-- Create Subject Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Create New Subject</h2>
          <button @click="showCreateModal = false" class="modal-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
        <form @submit.prevent="createSubject" class="modal-form">
          <div class="form-group">
            <label>Subject Name</label>
            <input v-model="newSubject.name" type="text" required class="form-input" placeholder="Enter subject name" />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="newSubject.description" class="form-input" rows="3" placeholder="Enter subject description (optional)"></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showCreateModal = false" class="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary">
              Create Subject
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit Subject Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Edit Subject</h2>
          <button @click="showEditModal = false" class="modal-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
        <form @submit.prevent="updateSubject" class="modal-form">
          <div class="form-group">
            <label>Subject Name</label>
            <input v-model="editingSubject.name" type="text" required class="form-input" placeholder="Enter subject name" />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="editingSubject.description" class="form-input" rows="3" placeholder="Enter subject description (optional)"></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showEditModal = false" class="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary">
              Update Subject
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
import { getSubjects, createSubject as createSubjectAPI, updateSubject as updateSubjectAPI, deleteSubject as deleteSubjectAPI } from '../../api';

// Reactive data
const subjects = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const selectedSubjects = ref([]);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const currentPage = ref(1);
const itemsPerPage = 10;

const newSubject = ref({
  name: '',
  description: ''
});

const editingSubject = ref({
  id: null,
  name: '',
  description: ''
});

// Computed properties
const filteredSubjects = computed(() => {
  let filtered = subjects.value;
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(subject => 
      subject.name?.toLowerCase().includes(query) ||
      subject.description?.toLowerCase().includes(query)
    );
  }
  
  return filtered;
});

const paginatedSubjects = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredSubjects.value.slice(start, end);
});

const totalPages = computed(() => Math.ceil(filteredSubjects.value.length / itemsPerPage));
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage);
const endIndex = computed(() => Math.min(startIndex.value + itemsPerPage, filteredSubjects.value.length));

const allSelected = computed(() => {
  return paginatedSubjects.value.length > 0 && selectedSubjects.value.length === paginatedSubjects.value.length;
});

// Methods
const fetchData = async () => {
  try {
    loading.value = true;
    const subjectsData = await getSubjects();
    subjects.value = subjectsData;
  } catch (error) {
    console.error('Error fetching data:', error);
  } finally {
    loading.value = false;
  }
};

const createSubject = async () => {
  try {
    await createSubjectAPI(newSubject.value);
    showCreateModal.value = false;
    newSubject.value = {
      name: '',
      description: ''
    };
    await fetchData();
  } catch (error) {
    console.error('Error creating subject:', error);
  }
};

const deleteSubject = async (subjectId) => {
  if (confirm('Are you sure you want to delete this subject?')) {
    try {
      await deleteSubjectAPI(subjectId);
      await fetchData();
      selectedSubjects.value = selectedSubjects.value.filter(id => id !== subjectId);
    } catch (error) {
      console.error('Error deleting subject:', error);
    }
  }
};

const deleteSelected = async () => {
  if (confirm(`Are you sure you want to delete ${selectedSubjects.value.length} subjects?`)) {
    try {
      for (const subjectId of selectedSubjects.value) {
        await deleteSubjectAPI(subjectId);
      }
      await fetchData();
      selectedSubjects.value = [];
    } catch (error) {
      console.error('Error deleting subjects:', error);
    }
  }
};

const editSubject = (subject) => {
  editingSubject.value = {
    id: subject.id,
    name: subject.name,
    description: subject.description
  };
  showEditModal.value = true;
};

const updateSubject = async () => {
  try {
    await updateSubjectAPI(editingSubject.value.id, {
      name: editingSubject.value.name,
      description: editingSubject.value.description
    });
    showEditModal.value = false;
    await fetchData();
  } catch (error) {
    console.error('Error updating subject:', error);
  }
};

const toggleSelectAll = () => {
  if (allSelected.value) {
    selectedSubjects.value = [];
  } else {
    selectedSubjects.value = paginatedSubjects.value.map(subject => subject.id);
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

const getTotalQuizzes = (subject) => {
  if (!subject.chapters) return 0;
  return subject.chapters.reduce((total, chapter) => {
    return total + (chapter.quizzes?.length || 0);
  }, 0);
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

/* Subject Content */
.subject-name {
  font-weight: 500;
  color: #1A1A1A;
}

.subject-description {
  max-width: 300px;
  color: #666;
  line-height: 1.4;
}

.chapter-count,
.quiz-count {
  font-weight: 500;
  color: #1976D2;
  background: rgba(25, 118, 210, 0.1);
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
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
}
</style>
