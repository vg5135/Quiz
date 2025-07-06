<template>
  <div class="quiz-container">
    <!-- Header -->
    <header class="quiz-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM19 19H5V5H19V19ZM7 10H9V17H7V10ZM11 7H13V17H11V7ZM15 13H17V17H15V13Z" fill="currentColor"/>
            </svg>
          </div>
          <h1 class="logo-text">QuizMaster</h1>
        </div>
        <div class="user-section">
          <div class="user-info">
            <span class="user-name">{{ userFullName || 'Student' }}</span>
            <span class="user-role">Student</span>
          </div>
          <!-- Quiz Summary Toggle Button -->
          <button @click="toggleQuizSummary" class="summary-toggle-btn" title="Quiz Summary">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM19 19H5V5H19V19ZM7 10H9V17H7V10ZM11 7H13V17H11V7ZM15 13H17V17H15V13Z" fill="currentColor"/>
            </svg>
            <span class="summary-count" v-if="completedQuizzes.length > 0">{{ completedQuizzes.length }}</span>
          </button>
          <button @click="logout" class="logout-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M17 7L15.59 8.41L18.17 11H8V13H18.17L15.59 15.59L17 17L22 12L17 7ZM4 5H12V3H4C2.9 3 2 3.9 2 5V19C2 20.1 2.9 21 4 21H12V19H4V5Z" fill="currentColor"/>
            </svg>
            Logout
          </button>
        </div>
      </div>
    </header>

    <!-- Quiz Summary Popover -->
    <div v-if="showQuizSummary" class="quiz-summary-overlay" @click="closeQuizSummary">
      <div class="quiz-summary-popover" @click.stop>
        <div class="summary-header">
          <h2>Quiz Performance Summary</h2>
          <button @click="closeQuizSummary" class="close-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
        
        <div class="summary-content">
          <!-- Overall Statistics -->
          <div class="summary-section">
            <h3>Overall Performance</h3>
            <div class="stats-grid">
              <div class="stat-card">
                <div class="stat-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM19 19H5V5H19V19ZM7 10H9V17H7V10ZM11 7H13V17H11V7ZM15 13H17V17H15V13Z" fill="currentColor"/>
                  </svg>
                </div>
                <div class="stat-info">
                  <span class="stat-value">{{ completedQuizzes.length }}</span>
                  <span class="stat-label">Quizzes Completed</span>
                </div>
              </div>
              <div class="stat-card">
                <div class="stat-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12S6.48 22 12 22 22 17.52 22 12 17.52 2 12 2ZM12 20C7.58 20 4 16.42 4 12S7.58 4 12 4 20 7.58 20 12 16.42 20 12 20Z" fill="currentColor"/>
                    <path d="M12.5 7H11V13L16.25 16.15L17 14.92L12.5 12.25V7Z" fill="currentColor"/>
                  </svg>
                </div>
                <div class="stat-info">
                  <span class="stat-value">{{ totalTimeSpent }}</span>
                  <span class="stat-label">Total Time Spent</span>
                </div>
              </div>
              <div class="stat-card">
                <div class="stat-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" fill="currentColor"/>
                  </svg>
                </div>
                <div class="stat-info">
                  <span class="stat-value">{{ averageScore }}%</span>
                  <span class="stat-label">Average Score</span>
                </div>
              </div>
              <div class="stat-card">
                <div class="stat-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="currentColor"/>
                  </svg>
                </div>
                <div class="stat-info">
                  <span class="stat-value">{{ bestScore }}%</span>
                  <span class="stat-label">Best Score</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Quiz Results -->
          <div class="summary-section">
            <h3>Recent Quiz Results</h3>
            <div class="quiz-results-list">
              <div v-if="quizResults.length === 0" class="no-results">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM19 19H5V5H19V19ZM7 10H9V17H7V10ZM11 7H13V17H11V7ZM15 13H17V17H15V13Z" fill="currentColor"/>
                </svg>
                <p>No quiz results available yet</p>
              </div>
              <div v-else v-for="result in quizResults" :key="result.id" class="quiz-result-item">
                <div class="result-header">
                  <h4>{{ result.quiz_title }}</h4>
                  <span :class="getScoreBadgeClass(result.score_percentage)">
                    {{ result.score_percentage }}%
                  </span>
                </div>
                <div class="result-details">
                  <span class="result-subject">{{ result.subject_name }}</span>
                  <span class="result-chapter">{{ result.chapter_name }}</span>
                  <span class="result-date">{{ formatDate(result.completed_at) }}</span>
                </div>
                <div class="result-stats">
                  <span class="result-stat">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" fill="currentColor"/>
                    </svg>
                    {{ result.correct_answers }}/{{ result.total_questions }}
                  </span>
                  <span class="result-stat">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM12 20C7.58 20 4 16.42 4 12S7.58 4 12 4 20 7.58 20 12 16.42 20 12 20Z" fill="currentColor"/>
                      <path d="M12.5 7H11V13L16.25 16.15L17 14.92L12.5 12.25V7Z" fill="currentColor"/>
                    </svg>
                    {{ result.time_taken }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Performance Trends -->
          <div class="summary-section">
            <h3>Performance Trends</h3>
            <div class="trends-container">
              <div class="trend-item">
                <span class="trend-label">Improvement Rate</span>
                <div class="trend-value">
                  <span :class="getTrendClass(performanceTrend)">
                    {{ performanceTrend > 0 ? '+' : '' }}{{ performanceTrend }}%
                  </span>
                  <span class="trend-period">vs last week</span>
                </div>
              </div>
              <div class="trend-item">
                <span class="trend-label">Study Streak</span>
                <div class="trend-value">
                  <span class="streak-count">{{ studyStreak }} days</span>
                  <span class="trend-period">current streak</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="quiz-main">
      <div class="quiz-layout">
        <!-- Left Side - Quiz List (Fixed Sidebar) -->
        <div class="quiz-list-section">
          <div class="section-header">
            <h2>Available Quizzes</h2>
            <p>Select a quiz to begin your assessment</p>
            
            <!-- Quiz Filter Tabs -->
            <div class="quiz-filter-tabs">
              <button 
                @click="setActiveFilter('all')" 
                :class="['filter-tab', { active: activeFilter === 'all' }]"
              >
                <span class="tab-count">{{ quizzes.length }}</span>
                All Quizzes
              </button>
              <button 
                @click="setActiveFilter('active')" 
                :class="['filter-tab', { active: activeFilter === 'active' }]"
              >
                <span class="tab-count">{{ activeQuizzes.length }}</span>
                Active
              </button>
              <button 
                @click="setActiveFilter('upcoming')" 
                :class="['filter-tab', { active: activeFilter === 'upcoming' }]"
              >
                <span class="tab-count">{{ upcomingQuizzes.length }}</span>
                Upcoming
              </button>
              <button 
                @click="setActiveFilter('expired')" 
                :class="['filter-tab', { active: activeFilter === 'expired' }]"
              >
                <span class="tab-count">{{ expiredQuizzes.length }}</span>
                Expired
              </button>
            </div>
          </div>
          
          <!-- Search and Sort -->
          <div class="quiz-controls">
            <div class="search-box">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15.5 14H14.71L14.43 13.73C15.41 12.59 16 11.11 16 9.5C16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16C11.11 16 12.59 15.41 13.73 14.43L14 14.71V15.5L19 20.49L20.49 19L15.5 14ZM9.5 14C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14Z" fill="currentColor"/>
              </svg>
              <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="Search quizzes..." 
                class="search-input"
              />
            </div>
            <div class="sort-dropdown">
              <select v-model="sortBy" class="sort-select">
                <option value="date">Sort by Date</option>
                <option value="title">Sort by Title</option>
                <option value="duration">Sort by Duration</option>
                <option value="subject">Sort by Subject</option>
              </select>
            </div>
          </div>
          
          <div class="quiz-list">
            <div v-if="filteredQuizzes.length === 0" class="empty-state">
              <div class="empty-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM19 19H5V5H19V19ZM7 10H9V17H7V10ZM11 7H13V17H11V7ZM15 13H17V17H15V13Z" fill="currentColor"/>
                </svg>
              </div>
              <h3>{{ getEmptyStateTitle() }}</h3>
              <p>{{ getEmptyStateMessage() }}</p>
            </div>
            
            <div v-else class="quiz-grid">
              <div 
                v-for="quiz in filteredQuizzes" 
                :key="quiz.id"
                class="quiz-card"
                :class="{ 
                  'selected': selectedQuiz?.id === quiz.id,
                  'completed': completedQuizzes.includes(quiz.id),
                  'expired': quiz.status === 'expired',
                  'upcoming': quiz.status === 'upcoming'
                }"
              >
                <!-- Quiz Status Badge -->
                <div class="quiz-status-badge" :class="getQuizStatusClass(quiz)">
                  <svg v-if="getQuizStatusClass(quiz) === 'status-active'" width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z" fill="currentColor"/>
                  </svg>
                  <svg v-else-if="getQuizStatusClass(quiz) === 'status-expired'" width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z" fill="currentColor"/>
                  </svg>
                  <svg v-else width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM12 20C7.58 20 4 16.42 4 12S7.58 4 12 4 20 7.58 20 12 16.42 20 12 20Z" fill="currentColor"/>
                    <path d="M12.5 7H11V13L16.25 16.15L17 14.92L12.5 12.25V7Z" fill="currentColor"/>
                  </svg>
                  {{ getQuizStatusText(quiz) }}
                </div>

                <!-- Quiz Content -->
                <div class="quiz-card-content">
                  <div class="quiz-card-header">
                    <h3 class="quiz-title">{{ quiz.title }}</h3>
                    <div class="quiz-subject-badge">
                      {{ getSubjectNameFromChapter(quiz.chapter_id) }}
                    </div>
                  </div>
                  
                  <div class="quiz-card-body">
                    <p class="quiz-chapter">{{ getChapterName(quiz.chapter_id) }}</p>
                    
                    <div class="quiz-meta-grid">
                      <div class="meta-item">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM12 20C7.58 20 4 16.42 4 12S7.58 4 12 4 20 7.58 20 12 16.42 20 12 20Z" fill="currentColor"/>
                          <path d="M12.5 7H11V13L16.25 16.15L17 14.92L12.5 12.25V7Z" fill="currentColor"/>
                        </svg>
                        <span>{{ quiz.duration_hours }}h {{ quiz.duration_minutes }}m</span>
                      </div>
                      <div class="meta-item">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM19 19H5V8H19V19Z" fill="currentColor"/>
                        </svg>
                        <span>{{ formatDate(quiz.start_datetime) }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Quiz Actions -->
                <div class="quiz-card-actions">
                  <button 
                    v-if="!completedQuizzes.includes(quiz.id) && quiz.status === 'active'"
                    @click.stop="selectQuiz(quiz)"
                    class="btn btn-primary btn-sm"
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M9 16.17L4.83 12L3.41 13.41L9 19L21 7L19.59 5.59L9 16.17Z" fill="currentColor"/>
                    </svg>
                    Take Quiz
                  </button>
                  <button 
                    v-else-if="completedQuizzes.includes(quiz.id)"
                    class="btn btn-success btn-sm"
                    disabled
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" fill="currentColor"/>
                    </svg>
                    Completed
                  </button>
                  <button 
                    v-else-if="quiz.status === 'expired'"
                    class="btn btn-secondary btn-sm"
                    disabled
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z" fill="currentColor"/>
                    </svg>
                    Expired
                  </button>
                  <button 
                    v-else-if="quiz.status === 'upcoming'"
                    class="btn btn-info btn-sm"
                    disabled
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM12 20C7.58 20 4 16.42 4 12S7.58 4 12 4 20 7.58 20 12 16.42 20 12 20Z" fill="currentColor"/>
                      <path d="M12.5 7H11V13L16.25 16.15L17 14.92L12.5 12.25V7Z" fill="currentColor"/>
                    </svg>
                    Coming Soon
                  </button>
                  <button 
                    v-else
                    class="btn btn-secondary btn-sm"
                    disabled
                  >
                    Not Available
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side - Quiz Taking Section -->
        <div class="quiz-taking-section">
          <div v-if="!selectedQuiz" class="quiz-placeholder">
            <div class="placeholder-content">
              <div class="placeholder-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM19 19H5V5H19V19ZM7 10H9V17H7V10ZM11 7H13V17H11V7ZM15 13H17V17H15V13Z" fill="currentColor"/>
                </svg>
              </div>
              <h3>Select a Quiz</h3>
              <p>Choose a quiz from the list on the left to begin your assessment</p>
            </div>
          </div>

          <!-- Quiz Interface -->
          <div v-else class="quiz-interface">
            <!-- Debug info -->
            <div style="background: yellow; padding: 10px; margin-bottom: 10px;">
              <strong>DEBUG:</strong> selectedQuiz exists: {{ !!selectedQuiz }}, 
              selectedQuiz title: {{ selectedQuiz?.title }}, 
              quizQuestions length: {{ quizQuestions.length }}
            </div>
            
            <div class="quiz-header-bar">
              <div class="quiz-info">
                <h2>{{ selectedQuiz.title }}</h2>
                <p>{{ getSubjectNameFromChapter(selectedQuiz.chapter_id) }} - {{ getChapterName(selectedQuiz.chapter_id) }}</p>
              </div>
              <div class="quiz-timer" v-if="timeRemaining > 0">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M11.99 2C6.47 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM12 20C7.58 20 4 16.42 4 12S7.58 4 12 4 20 7.58 20 12 16.42 20 12 20Z" fill="currentColor"/>
                  <path d="M12.5 7H11V13L16.25 16.15L17 14.92L12.5 12.25V7Z" fill="currentColor"/>
                </svg>
                <span class="timer-text">{{ formatTime(timeRemaining) }}</span>
              </div>
              <button @click="exitQuiz" class="exit-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
                </svg>
                Exit Quiz
              </button>
            </div>

            <div class="quiz-progress">
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: `${Object.keys(selectedAnswers).length / quizQuestions.length * 100}%` }"
                ></div>
              </div>
              <span class="progress-text">{{ Object.keys(selectedAnswers).length }} of {{ quizQuestions.length }} questions answered</span>
            </div>

            <div class="questions-container" v-if="!showResults">
              <div class="accordion-container">
                <div 
                  v-for="(question, index) in quizQuestions" 
                  :key="question.id"
                  class="accordion-item"
                  :class="{ 
                    'active': currentQuestionIndex === index,
                    'answered': selectedAnswers[index]
                  }"
                >
                  <div 
                    class="accordion-header"
                    @click="currentQuestionIndex = index"
                  >
                    <div class="question-info">
                      <div class="question-number-badge">
                        <span class="number">{{ index + 1 }}</span>
                        <div class="status-indicator" :class="{ 'answered': selectedAnswers[index] }">
                          <svg v-if="selectedAnswers[index]" width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" fill="currentColor"/>
                          </svg>
                        </div>
                      </div>
                      <div class="question-preview">
                        <h3 class="question-title">{{ question.question_text.substring(0, 60) }}{{ question.question_text.length > 60 ? '...' : '' }}</h3>
                        <div class="question-meta">
                          <span :class="getDifficultyBadge(question.difficulty).class">
                            {{ getDifficultyBadge(question.difficulty).text }}
                          </span>
                          <span class="answer-status" v-if="selectedAnswers[index]">
                            Answer: {{ selectedAnswers[index] }}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div class="accordion-toggle">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </div>
                  </div>
                  
                  <div class="accordion-content" v-show="currentQuestionIndex === index">
                    <div class="question-full-text">
                      {{ question.question_text }}
                    </div>

                    <div class="options-container">
                      <div 
                        v-for="(option, optionIndex) in ['A', 'B', 'C', 'D']" 
                        :key="option"
                        class="option-item"
                        :class="{ 
                          selected: selectedAnswers[index] === option
                        }"
                        @click="selectAnswer(option, index)"
                      >
                        <div class="option-letter">{{ option }}</div>
                        <div class="option-text">
                          {{ question[`option${optionIndex + 1}`] }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="quiz-submit-section">
                <button 
                  @click="submitQuiz" 
                  class="btn btn-success btn-large"
                  :disabled="Object.keys(selectedAnswers).length < quizQuestions.length"
                >
                  Submit Quiz ({{ Object.keys(selectedAnswers).length }}/{{ quizQuestions.length }})
                </button>
              </div>
            </div>

            <!-- Results Modal -->
            <div v-if="showResults" class="results-modal">
              <div class="results-content">
                <div class="results-header">
                  <h2>Quiz Results</h2>
                  <div class="score-display">
                    <div class="score-circle">
                      <span class="score-number">{{ correctAnswers }}</span>
                      <span class="score-total">/ {{ quizQuestions.length }}</span>
                    </div>
                    <div class="score-percentage">
                      {{ Math.round((correctAnswers / quizQuestions.length) * 100) }}%
                    </div>
                  </div>
                </div>

                <div class="results-summary">
                  <div class="summary-item">
                    <span class="summary-label">Correct Answers:</span>
                    <span class="summary-value correct">{{ correctAnswers }}</span>
                  </div>
                  <div class="summary-item">
                    <span class="summary-label">Incorrect Answers:</span>
                    <span class="summary-value incorrect">{{ quizQuestions.length - correctAnswers }}</span>
                  </div>
                  <div class="summary-item">
                    <span class="summary-label">Time Taken:</span>
                    <span class="summary-value">{{ formatTime(quizDuration) }}</span>
                  </div>
                </div>

                <div class="results-actions">
                  <button @click="exitQuiz" class="btn btn-primary">
                    Back to Quizzes
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import { useRouter } from "vue-router";
import { getQuizzes, getQuestions, getChapters, getSubjects } from "../api";

const router = useRouter();
const userFullName = ref("");
const quizzes = ref([]);
const questions = ref([]);
const chapters = ref([]);
const subjects = ref([]);

// Quiz state
const selectedQuiz = ref(null);
const quizQuestions = ref([]);
const currentQuestionIndex = ref(0);
const selectedAnswers = ref({});
const timeRemaining = ref(0);
const quizDuration = ref(0);
const showResults = ref(false);
const correctAnswers = ref(0);
const completedQuizzes = ref([]);
let timer = null;

// Add new reactive variables for quiz summary
const showQuizSummary = ref(false);
const quizResults = ref([]);
const performanceTrend = ref(5.2); // Mock data - would come from API
const studyStreak = ref(7); // Mock data - would come from API

// Add new reactive variables for quiz filtering and organization
const activeFilter = ref('all');
const searchQuery = ref('');
const sortBy = ref('date');

// Computed properties for filtered and sorted quizzes
const filteredQuizzes = computed(() => {
  let filtered = quizzes.value;
  
  // Filter by status
  if (activeFilter.value === 'active') {
    filtered = filtered.filter(quiz => quiz.status === 'active');
  } else if (activeFilter.value === 'upcoming') {
    filtered = filtered.filter(quiz => quiz.status === 'upcoming');
  } else if (activeFilter.value === 'expired') {
    filtered = filtered.filter(quiz => quiz.status === 'expired');
  }
  
  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(quiz => 
      quiz.title.toLowerCase().includes(query) ||
      getSubjectNameFromChapter(quiz.chapter_id).toLowerCase().includes(query) ||
      getChapterName(quiz.chapter_id).toLowerCase().includes(query)
    );
  }
  
  // Sort quizzes
  filtered = [...filtered].sort((a, b) => {
    switch (sortBy.value) {
      case 'title':
        return a.title.localeCompare(b.title);
      case 'duration':
        const durationA = a.duration_hours * 60 + a.duration_minutes;
        const durationB = b.duration_hours * 60 + b.duration_minutes;
        return durationA - durationB;
      case 'subject':
        return getSubjectNameFromChapter(a.chapter_id).localeCompare(getSubjectNameFromChapter(b.chapter_id));
      case 'date':
      default:
        return new Date(a.start_datetime) - new Date(b.start_datetime);
    }
  });
  
  return filtered;
});

const activeQuizzes = computed(() => {
  return quizzes.value.filter(quiz => quiz.status === 'active');
});

const upcomingQuizzes = computed(() => {
  return quizzes.value.filter(quiz => quiz.status === 'upcoming');
});

const expiredQuizzes = computed(() => {
  return quizzes.value.filter(quiz => quiz.status === 'expired');
});

const currentQuestion = computed(() => {
  return quizQuestions.value[currentQuestionIndex.value] || null;
});

const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  router.push("/login");
};

const fetchData = async () => {
  try {
    console.log('📊 Fetching all data...');
    
    // Fetch quizzes first - this is the most important
    try {
      quizzes.value = await getQuizzes();
      console.log('📊 Quizzes loaded:', quizzes.value.length);
      console.log('📊 Quiz data:', quizzes.value);
      
      // Log each quiz's status
      quizzes.value.forEach((quiz, index) => {
        console.log(`📊 Quiz ${index + 1}:`, {
          id: quiz.id,
          title: quiz.title,
          status: quiz.status,
          start_datetime: quiz.start_datetime,
          end_datetime: quiz.end_datetime
        });
      });
    } catch (error) {
      console.error('📊 Error loading quizzes:', error);
      quizzes.value = [];
    }
    
    // Fetch other data (these are less critical)
    try {
      questions.value = await getQuestions();
    } catch (error) {
      console.error('Error loading questions:', error);
      questions.value = [];
    }
    
    try {
      chapters.value = await getChapters();
    } catch (error) {
      console.error('Error loading chapters:', error);
      chapters.value = [];
    }
    
    try {
      subjects.value = await getSubjects();
    } catch (error) {
      console.error('Error loading subjects:', error);
      subjects.value = [];
    }
    
    // Fetch quiz history
    try {
      await fetchQuizHistory();
    } catch (error) {
      console.error('Error loading quiz history:', error);
    }
    
    console.log('All data loaded successfully');
  } catch (error) {
    console.error("Error in fetchData:", error);
  }
};

const fetchQuizHistory = async () => {
  try {
    console.log('Fetching quiz history...');
    const response = await fetch('http://127.0.0.1:5006/api/quiz-history', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const history = await response.json();
      completedQuizzes.value = history.map(score => score.quiz_id);
      console.log('Quiz history loaded. Completed quizzes:', completedQuizzes.value);
    } else {
      console.error('Failed to fetch quiz history:', response.status);
    }
  } catch (error) {
    console.error("Error fetching quiz history:", error);
  }
};

const getStatusBadge = (status) => {
  const statusMap = {
    active: { class: "badge bg-success", text: "Active" },
    upcoming: { class: "badge bg-warning", text: "Upcoming" },
    expired: { class: "badge bg-danger", text: "Expired" }
  };
  return statusMap[status] || { class: "badge bg-secondary", text: "Unknown" };
};

const getSubjectNameFromChapter = (chapterId) => {
  const chapter = chapters.value.find(c => c.id === chapterId);
  if (!chapter) return "Unknown";
  const subject = subjects.value.find(s => s.id === chapter.subject_id);
  return subject ? subject.name : "Unknown";
};

const getChapterName = (chapterId) => {
  const chapter = chapters.value.find(c => c.id === chapterId);
  return chapter ? chapter.name : "Unknown";
};

const getDifficultyBadge = (difficulty) => {
  const difficultyMap = {
    easy: { class: "badge bg-success", text: "Easy" },
    medium: { class: "badge bg-warning", text: "Medium" },
    hard: { class: "badge bg-danger", text: "Hard" }
  };
  return difficultyMap[difficulty] || { class: "badge bg-secondary", text: "Unknown" };
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  return `${minutes}:${secs.toString().padStart(2, '0')}`;
};

const debugSelectQuiz = async (quiz) => {
  console.log('🔧 DEBUG: debugSelectQuiz called with:', quiz);
  console.log('🔧 DEBUG: Quiz status:', quiz.status);
  console.log('🔧 DEBUG: Quiz completed:', completedQuizzes.value.includes(quiz.id));
  
  try {
    selectedQuiz.value = quiz;
    console.log('🔧 DEBUG: selectedQuiz set to:', selectedQuiz.value);
    
    // Try to fetch questions
    const response = await fetch(`http://127.0.0.1:5006/api/test-quiz/${quiz.id}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      }
    });
    
    console.log('🔧 DEBUG: Response status:', response.status);
    
    if (response.ok) {
      const data = await response.json();
      console.log('🔧 DEBUG: Quiz data received:', data);
      quizQuestions.value = data.questions || [];
      console.log('🔧 DEBUG: Questions set:', quizQuestions.value);
    } else {
      console.log('🔧 DEBUG: Response not ok, trying fallback');
      quizQuestions.value = questions.value.filter(q => q.quiz_id === quiz.id);
      console.log('🔧 DEBUG: Fallback questions:', quizQuestions.value);
    }
    
    selectedAnswers.value = {};
    currentQuestionIndex.value = 0;
    showResults.value = false;
    
    console.log('🔧 DEBUG: Quiz setup completed');
  } catch (error) {
    console.error('🔧 DEBUG: Error in debugSelectQuiz:', error);
  }
};

const selectQuiz = async (quiz) => {
  console.log('🚀 selectQuiz function called!'); // Simple debug log
  console.log('=== selectQuiz function called ==='); // Debug log
  console.log('selectQuiz called with:', quiz); // Debug log
  console.log('Quiz status from backend:', quiz.status); // Debug log
  console.log('Is completed:', completedQuizzes.value.includes(quiz.id)); // Debug log
  console.log('Token exists:', !!localStorage.getItem('token')); // Debug log
  
  // Check if quiz is already completed
  if (completedQuizzes.value.includes(quiz.id)) {
    console.log('Quiz already completed, returning'); // Debug log
    alert("You have already completed this quiz. You cannot take it again.");
    return;
  }
  
  // Use the status from the backend API
  if (quiz.status === 'expired') {
    console.log('Quiz expired, returning'); // Debug log
    alert("This quiz has expired and is no longer available.");
    return;
  }
  
  if (quiz.status === 'upcoming') {
    console.log('Quiz upcoming, returning'); // Debug log
    alert("This quiz is not yet available. Please wait until the start time.");
    return;
  }
  
  if (quiz.status !== 'active') {
    console.log('Quiz not active, returning. Status:', quiz.status); // Debug log
    alert("This quiz is not currently active. Please select an active quiz.");
    return;
  }
  
  console.log('All checks passed, proceeding with quiz selection'); // Debug log
  
  try {
    console.log('Setting selectedQuiz to:', quiz); // Debug log
    selectedQuiz.value = quiz;
    
    // Fetch questions for this specific quiz
    console.log('Fetching questions for quiz ID:', quiz.id); // Debug log
    const quizQuestionsResponse = await fetch(`http://127.0.0.1:5006/api/test-quiz/${quiz.id}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      }
    });
    
    console.log('Quiz questions response status:', quizQuestionsResponse.status); // Debug log
    
    if (quizQuestionsResponse.ok) {
      const quizData = await quizQuestionsResponse.json();
      console.log('Quiz data received:', quizData); // Debug log
      quizQuestions.value = quizData.questions || [];
      console.log('Quiz questions set:', quizQuestions.value); // Debug log
    } else {
      console.log('Fallback to filtering from all questions'); // Debug log
      // Fallback to filtering from all questions
      quizQuestions.value = questions.value.filter(q => q.quiz_id === quiz.id);
      console.log('Filtered questions:', quizQuestions.value); // Debug log
    }
    
    selectedAnswers.value = {};
    currentQuestionIndex.value = 0;
    showResults.value = false;
    
    // Set timer
    quizDuration.value = (quiz.duration_hours * 3600) + (quiz.duration_minutes * 60);
    timeRemaining.value = quizDuration.value;
    
    console.log('Starting timer with duration:', quizDuration.value); // Debug log
    startTimer();
    console.log('=== selectQuiz function completed successfully ==='); // Debug log
  } catch (error) {
    console.error("Error fetching quiz questions:", error);
    console.error("Error details:", error.message); // Debug log
    alert("Error loading quiz questions. Please try again.");
  }
};

const startTimer = () => {
  timer = setInterval(() => {
    if (timeRemaining.value > 0) {
      timeRemaining.value--;
    } else {
      submitQuiz();
    }
  }, 1000);
};

const selectAnswer = (option, index) => {
  if (!showResults.value) {
    selectedAnswers.value[index] = option;
  }
};

const submitQuiz = async () => {
  clearInterval(timer);
  showResults.value = true;
  
  // Calculate correct answers - backend uses correct_option (1,2,3,4) and option1,option2,etc.
  correctAnswers.value = quizQuestions.value.reduce((count, question, index) => {
    const selectedAnswer = selectedAnswers.value[index];
    const correctOption = question.correct_option; // Backend returns 1,2,3,4
    
    // Convert selected answer (A,B,C,D) to number (1,2,3,4) for comparison
    const selectedOptionNumber = selectedAnswer === 'A' ? 1 : 
                                 selectedAnswer === 'B' ? 2 : 
                                 selectedAnswer === 'C' ? 3 : 4;
    
    return count + (selectedOptionNumber === correctOption ? 1 : 0);
  }, 0);
  
  // Submit score to backend
  try {
    const scoreData = {
      quizId: selectedQuiz.value.id,
      score: correctAnswers.value,
      totalQuestions: quizQuestions.value.length
    };
    
    const response = await fetch('http://127.0.0.1:5006/api/submit-quiz', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(scoreData)
    });
    
    if (response.ok) {
      // Immediately add the quiz to completed list to prevent retaking
      if (selectedQuiz.value && !completedQuizzes.value.includes(selectedQuiz.value.id)) {
        completedQuizzes.value.push(selectedQuiz.value.id);
      }
      console.log('Quiz submitted successfully. Quiz ID:', selectedQuiz.value.id, 'added to completed list');
    } else {
      console.error('Failed to submit quiz score');
    }
  } catch (error) {
    console.error('Error submitting quiz score:', error);
  }
};

const finishQuiz = async () => {
  console.log('Finishing quiz. Current completed quizzes:', completedQuizzes.value);
  
  // Add the completed quiz to the list if not already there
  if (selectedQuiz.value && !completedQuizzes.value.includes(selectedQuiz.value.id)) {
    completedQuizzes.value.push(selectedQuiz.value.id);
    console.log('Added quiz ID', selectedQuiz.value.id, 'to completed list');
  }
  
  selectedQuiz.value = null;
  quizQuestions.value = [];
  selectedAnswers.value = {};
  currentQuestionIndex.value = 0;
  showResults.value = false;
  timeRemaining.value = 0;
  
  // Refresh quiz history from server to ensure consistency
  await fetchQuizHistory();
  
  console.log('Final completed quizzes list:', completedQuizzes.value);
  
  // Redirect to dashboard
  router.push('/');
};

const exitQuiz = () => {
  if (confirm("Are you sure you want to exit the quiz? Your progress will be lost.")) {
    clearInterval(timer);
    finishQuiz();
  }
};

// Computed properties for summary statistics
const totalTimeSpent = computed(() => {
  // Mock calculation - would come from actual quiz results
  return '2h 15m';
});

const averageScore = computed(() => {
  if (quizResults.value.length === 0) return 0;
  const total = quizResults.value.reduce((sum, result) => sum + result.score_percentage, 0);
  return Math.round(total / quizResults.value.length);
});

const bestScore = computed(() => {
  if (quizResults.value.length === 0) return 0;
  return Math.max(...quizResults.value.map(result => result.score_percentage));
});

// Methods for quiz summary
const toggleQuizSummary = () => {
  showQuizSummary.value = !showQuizSummary.value;
  if (showQuizSummary.value) {
    loadQuizResults();
  }
};

const closeQuizSummary = () => {
  showQuizSummary.value = false;
};

const loadQuizResults = async () => {
  try {
    // Mock API call - replace with actual API endpoint
    const response = await fetch('http://127.0.0.1:5006/quiz-results', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      quizResults.value = data.results || [];
    } else {
      // Use mock data if API fails
      quizResults.value = [
        {
          id: 1,
          quiz_title: "Mathematics Quiz 1",
          subject_name: "Mathematics",
          chapter_name: "Algebra",
          score_percentage: 85,
          correct_answers: 17,
          total_questions: 20,
          time_taken: "25m 30s",
          completed_at: "2024-01-15T10:30:00Z"
        },
        {
          id: 2,
          quiz_title: "Physics Quiz 2",
          subject_name: "Physics",
          chapter_name: "Mechanics",
          score_percentage: 92,
          correct_answers: 23,
          total_questions: 25,
          time_taken: "30m 15s",
          completed_at: "2024-01-14T14:20:00Z"
        },
        {
          id: 3,
          quiz_title: "Chemistry Quiz 1",
          subject_name: "Chemistry",
          chapter_name: "Organic Chemistry",
          score_percentage: 78,
          correct_answers: 15,
          total_questions: 20,
          time_taken: "22m 45s",
          completed_at: "2024-01-13T09:15:00Z"
        }
      ];
    }
  } catch (error) {
    console.error('Error loading quiz results:', error);
    // Use mock data on error
    quizResults.value = [
      {
        id: 1,
        quiz_title: "Mathematics Quiz 1",
        subject_name: "Mathematics",
        chapter_name: "Algebra",
        score_percentage: 85,
        correct_answers: 17,
        total_questions: 20,
        time_taken: "25m 30s",
        completed_at: "2024-01-15T10:30:00Z"
      }
    ];
  }
};

const getScoreBadgeClass = (score) => {
  if (score >= 90) return 'badge excellent';
  if (score >= 80) return 'badge good';
  if (score >= 70) return 'badge average';
  return 'badge poor';
};

const getTrendClass = (trend) => {
  if (trend > 0) return 'trend-positive';
  if (trend < 0) return 'trend-negative';
  return 'trend-neutral';
};

// Methods for quiz filtering and organization
const setActiveFilter = (filter) => {
  activeFilter.value = filter;
};

const isExpired = (quiz) => {
  const now = new Date();
  const endDate = new Date(quiz.start_datetime);
  endDate.setHours(endDate.getHours() + quiz.duration_hours);
  endDate.setMinutes(endDate.getMinutes() + quiz.duration_minutes);
  return now > endDate;
};

const isUpcoming = (quiz) => {
  const now = new Date();
  const startDate = new Date(quiz.start_datetime);
  return now < startDate;
};

const getQuizStatusClass = (quiz) => {
  if (completedQuizzes.value.includes(quiz.id)) {
    return 'status-completed';
  } else if (quiz.status === 'expired') {
    return 'status-expired';
  } else if (quiz.status === 'upcoming') {
    return 'status-upcoming';
  } else if (quiz.status === 'active') {
    return 'status-active';
  }
  return 'status-inactive';
};

const getQuizStatusText = (quiz) => {
  if (completedQuizzes.value.includes(quiz.id)) {
    return 'Completed';
  } else if (quiz.status === 'expired') {
    return 'Expired';
  } else if (quiz.status === 'upcoming') {
    return 'Upcoming';
  } else if (quiz.status === 'active') {
    return 'Active';
  }
  return 'Inactive';
};

const getEmptyStateTitle = () => {
  switch (activeFilter.value) {
    case 'active':
      return 'No Active Quizzes';
    case 'upcoming':
      return 'No Upcoming Quizzes';
    case 'expired':
      return 'No Expired Quizzes';
    default:
      return 'No Quizzes Found';
  }
};

const getEmptyStateMessage = () => {
  switch (activeFilter.value) {
    case 'active':
      return 'There are currently no active quizzes available. Check back later or try a different filter.';
    case 'upcoming':
      return 'No upcoming quizzes scheduled at the moment.';
    case 'expired':
      return 'No expired quizzes in your history.';
    default:
      return searchQuery.value ? 'No quizzes match your search criteria.' : 'There are currently no quizzes available.';
  }
};

onMounted(() => {
  if (!localStorage.getItem("token")) {
    router.push("/login");
  }
  userFullName.value = localStorage.getItem("userFullName") || "Student";
  console.log('Component mounted, fetching data...');
  fetchData().then(() => {
    console.log('Data fetch completed. Quizzes count:', quizzes.value.length);
    console.log('Quizzes:', quizzes.value);
  });
});

onUnmounted(() => {
  if (timer) {
    clearInterval(timer);
  }
});
</script>

<style scoped>
/* Quiz Container */
.quiz-container {
  min-height: 100vh;
  background: #F8F9FA;
  display: flex;
  flex-direction: column;
}

/* Header */
.quiz-header {
  background: white;
  border-bottom: 1px solid #E0E0E0;
  padding: 16px 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  color: #1976D2;
}

.logo-text {
  font-size: 24px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  text-align: right;
}

.user-name {
  display: block;
  font-weight: 500;
  color: #1A1A1A;
  font-size: 14px;
}

.user-role {
  display: block;
  font-size: 12px;
  color: #666;
}

/* Summary Toggle Button */
.summary-toggle-btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(25, 118, 210, 0.1);
  color: #1976D2;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-right: 12px;
}

.summary-toggle-btn:hover {
  background: rgba(25, 118, 210, 0.2);
  transform: translateY(-1px);
}

.summary-count {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #D32F2F;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 10px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(244, 67, 54, 0.1);
  color: #D32F2F;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: rgba(244, 67, 54, 0.2);
}

/* Quiz Summary Popover */
.quiz-summary-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 24px;
}

.quiz-summary-popover {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.summary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 16px 24px;
  border-bottom: 1px solid #E0E0E0;
}

.summary-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0;
}

.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: #F5F5F5;
  border: none;
  border-radius: 8px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #E0E0E0;
  color: #1A1A1A;
}

.summary-content {
  padding: 24px;
}

.summary-section {
  margin-bottom: 32px;
}

.summary-section:last-child {
  margin-bottom: 0;
}

.summary-section h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0 0 20px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #F8F9FA;
  border-radius: 12px;
  border: 1px solid #E0E0E0;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(25, 118, 210, 0.1);
  color: #1976D2;
  border-radius: 8px;
  flex-shrink: 0;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #1A1A1A;
  line-height: 1;
}

.stat-label {
  font-size: 12px;
  color: #666;
  margin-top: 2px;
}

.quiz-results-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.no-results {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.no-results svg {
  opacity: 0.5;
  margin-bottom: 16px;
}

.no-results p {
  font-size: 14px;
  margin: 0;
}

.quiz-result-item {
  padding: 16px;
  background: #F8F9FA;
  border-radius: 12px;
  border: 1px solid #E0E0E0;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
  gap: 12px;
}

.result-header h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0;
  flex: 1;
}

.result-details {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.result-subject,
.result-chapter,
.result-date {
  font-size: 12px;
  color: #666;
  padding: 4px 8px;
  background: rgba(25, 118, 210, 0.1);
  border-radius: 6px;
}

.result-stats {
  display: flex;
  gap: 16px;
}

.result-stat {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #666;
}

.result-stat svg {
  color: #999;
}

.trends-container {
  display: flex;
  gap: 24px;
}

.trend-item {
  flex: 1;
  padding: 16px;
  background: #F8F9FA;
  border-radius: 12px;
  border: 1px solid #E0E0E0;
}

.trend-label {
  display: block;
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.trend-value {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.trend-period {
  font-size: 11px;
  color: #999;
}

.streak-count {
  font-size: 18px;
  font-weight: 600;
  color: #1976D2;
}

/* Score Badge Classes */
.score-excellent {
  background: rgba(76, 175, 80, 0.1);
  color: #388E3C;
}

.score-good {
  background: rgba(255, 152, 0, 0.1);
  color: #F57C00;
}

.score-average {
  background: rgba(255, 193, 7, 0.1);
  color: #F57F17;
}

.score-poor {
  background: rgba(244, 67, 54, 0.1);
  color: #D32F2F;
}

/* Trend Classes */
.trend-positive {
  color: #388E3C;
}

.trend-negative {
  color: #D32F2F;
}

.trend-neutral {
  color: #666;
}

/* Main Content */
.quiz-main {
  flex: 1;
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  margin-top: 80px; /* Account for fixed header */
}

.quiz-layout {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 24px;
  height: calc(100vh - 120px);
}

/* Quiz List Section */
.quiz-list-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #E0E0E0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 24px;
  top: 104px; /* Header height + padding */
  width: 376px; /* 400px - 24px padding */
  height: calc(100vh - 128px);
  z-index: 100;
}

/* Quiz Taking Section */
.quiz-taking-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #E0E0E0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 424px; /* 24px + 400px (sidebar width) */
  top: 104px; /* Header height + padding */
  right: 24px; /* Account for right padding */
  height: calc(100vh - 128px);
  z-index: 100;
}

.section-header {
  padding: 24px 24px 16px 24px;
  border-bottom: 1px solid #E0E0E0;
  background: #F8F9FA;
}

.section-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0 0 4px 0;
}

.section-header p {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.quiz-filter-tabs {
  display: flex;
  gap: 4px;
  margin-top: 12px;
  padding: 2px;
  background: #F8F9FA;
  border-radius: 8px;
  border: 1px solid #E0E0E0;
}

.filter-tab {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: #666;
  font-size: 10px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  flex: 1;
  justify-content: center;
  position: relative;
  min-height: 24px;
}

.filter-tab:hover {
  background: rgba(25, 118, 210, 0.1);
  color: #1976D2;
}

.filter-tab.active {
  background: #1976D2;
  color: white;
  box-shadow: 0 1px 4px rgba(25, 118, 210, 0.3);
}

.tab-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 14px;
  height: 14px;
  padding: 0 2px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  font-size: 8px;
  font-weight: 600;
}

.filter-tab.active .tab-count {
  background: rgba(255, 255, 255, 0.3);
}

/* Quiz Controls */
.quiz-controls {
  display: flex;
  gap: 8px;
  margin: 16px 0;
  padding: 0 4px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  padding: 8px 12px;
  background: white;
  border: 1px solid #E0E0E0;
  border-radius: 6px;
  transition: all 0.2s ease;
  height: 32px;
}

.search-box:focus-within {
  border-color: #1976D2;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
}

.search-box svg {
  color: #666;
  flex-shrink: 0;
  width: 14px;
  height: 14px;
}

.search-input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 12px;
  color: #1A1A1A;
  background: transparent;
}

.search-input::placeholder {
  color: #999;
  font-size: 12px;
}

.sort-dropdown {
  position: relative;
  min-width: 120px;
}

.sort-select {
  width: 100%;
  padding: 8px 12px;
  background: white;
  border: 1px solid #E0E0E0;
  border-radius: 6px;
  font-size: 12px;
  color: #1A1A1A;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 8px center;
  background-repeat: no-repeat;
  background-size: 12px;
  padding-right: 28px;
  height: 32px;
}

.sort-select:focus {
  border-color: #1976D2;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
}

/* Quiz Grid */
.quiz-list {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.quiz-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 12px;
  padding: 4px;
}

/* Quiz Cards */
.quiz-card {
  position: relative;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border: 1px solid #E0E0E0;
  border-radius: 12px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  min-height: 140px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.quiz-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #E0E0E0 0%, #F5F5F5 100%);
  transition: all 0.3s ease;
}

.quiz-card::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 20px 20px 0;
  border-color: transparent transparent rgba(25, 118, 210, 0.1) transparent;
  opacity: 0;
  transition: all 0.3s ease;
}

.quiz-card:hover {
  border-color: #1976D2;
  box-shadow: 0 8px 25px rgba(25, 118, 210, 0.15);
  transform: translateY(-2px);
  background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%);
}

.quiz-card:hover::before {
  background: linear-gradient(90deg, #1976D2 0%, #42a5f5 100%);
}

.quiz-card:hover::after {
  opacity: 1;
}

.quiz-card.selected {
  border-color: #1976D2;
  background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
  box-shadow: 0 6px 20px rgba(25, 118, 210, 0.15);
}

.quiz-card.selected::before {
  background: linear-gradient(90deg, #1976D2 0%, #42a5f5 100%);
}

.quiz-card.selected::after {
  opacity: 1;
}

.quiz-card.completed {
  opacity: 0.9;
  background: linear-gradient(135deg, #ffffff 0%, #f1f8e9 100%);
}

.quiz-card.completed::before {
  background: linear-gradient(90deg, #388E3C 0%, #66bb6a 100%);
}

.quiz-card.expired {
  opacity: 0.7;
  cursor: not-allowed;
  background: linear-gradient(135deg, #ffffff 0%, #ffebee 100%);
}

.quiz-card.expired::before {
  background: linear-gradient(90deg, #D32F2F 0%, #ef5350 100%);
}

.quiz-card.upcoming {
  opacity: 0.8;
  cursor: not-allowed;
  background: linear-gradient(135deg, #ffffff 0%, #fff3e0 100%);
}

.quiz-card.upcoming::before {
  background: linear-gradient(90deg, #F57C00 0%, #ff9800 100%);
}

/* Quiz Status Badge */
.quiz-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 6px;
  border-radius: 10px;
  font-size: 9px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
  align-self: flex-start;
}

.status-active {
  background: rgba(76, 175, 80, 0.1);
  color: #388E3C;
}

.status-upcoming {
  background: rgba(255, 152, 0, 0.1);
  color: #F57C00;
}

.status-expired {
  background: rgba(244, 67, 54, 0.1);
  color: #D32F2F;
}

.status-completed {
  background: rgba(33, 150, 243, 0.1);
  color: #1976D2;
}

.status-inactive {
  background: rgba(158, 158, 158, 0.1);
  color: #616161;
}

/* Quiz Card Content */
.quiz-card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-bottom: 8px;
}

.quiz-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 6px;
  gap: 6px;
}

.quiz-title {
  font-size: 13px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0;
  line-height: 1.2;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.quiz-subject-badge {
  padding: 2px 4px;
  border-radius: 6px;
  background: rgba(25, 118, 210, 0.1);
  color: #1976D2;
  font-size: 8px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex-shrink: 0;
}

.quiz-card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.quiz-chapter {
  color: #666;
  margin: 0 0 6px 0;
  font-size: 11px;
  line-height: 1.2;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.quiz-meta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  margin-bottom: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 10px;
  color: #666;
}

.meta-item svg {
  color: #999;
  flex-shrink: 0;
  width: 10px;
  height: 10px;
}

/* Quiz Card Actions */
.quiz-card-actions {
  display: flex;
  justify-content: center;
  margin-top: auto;
}

/* Enhanced Button Styles */
.btn {
  padding: 6px 12px;
  border: none;
  border-radius: 8px;
  font-size: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 3px;
  text-decoration: none;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  min-width: 70px;
  justify-content: center;
  height: 28px;
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn:hover::before {
  left: 100%;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 9px;
  min-width: 60px;
  height: 24px;
  border-radius: 6px;
}

.btn-large {
  padding: 10px 20px;
  font-size: 12px;
  min-width: 90px;
  height: 36px;
  border-radius: 10px;
}

.btn-primary {
  background: linear-gradient(135deg, #1976D2 0%, #42a5f5 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.3);
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.4);
}

.btn-secondary {
  background: linear-gradient(135deg, #F5F5F5 0%, #E0E0E0 100%);
  color: #666;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.btn-secondary:hover:not(:disabled) {
  background: linear-gradient(135deg, #E0E0E0 0%, #D0D0D0 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.btn-success {
  background: linear-gradient(135deg, #388E3C 0%, #66bb6a 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(56, 142, 60, 0.3);
}

.btn-success:hover:not(:disabled) {
  background: linear-gradient(135deg, #2E7D32 0%, #388E3C 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(56, 142, 60, 0.4);
}

.btn-info {
  background: linear-gradient(135deg, #1976D2 0%, #42a5f5 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.3);
}

.btn-info:hover:not(:disabled) {
  background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.4);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn:disabled::before {
  display: none;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 24px;
  color: #666;
}

.empty-icon {
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0 0 8px 0;
}

.empty-state p {
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
  max-width: 400px;
  margin: 0 auto;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .quiz-layout {
    grid-template-columns: 1fr;
  }
  
  .quiz-list-section {
    position: relative;
    left: auto;
    top: auto;
    width: auto;
    height: auto;
    margin-bottom: 24px;
  }
  
  .quiz-taking-section {
    position: relative;
    left: auto;
    top: auto;
    right: auto;
    height: auto;
    margin-left: 0;
  }
  
  .quiz-grid {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 12px;
  }
  
  .quiz-filter-tabs {
    flex-wrap: wrap;
  }
  
  .filter-tab {
    flex: 1 1 calc(50% - 4px);
  }
}

@media (max-width: 768px) {
  .quiz-main {
    padding: 16px;
    margin-top: 70px;
  }
  
  .quiz-header {
    padding: 12px 16px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .user-section {
    width: 100%;
    justify-content: space-between;
  }
  
  .quiz-controls {
    flex-direction: column;
    gap: 12px;
  }
  
  .quiz-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .quiz-filter-tabs {
    flex-direction: column;
  }
  
  .filter-tab {
    flex: none;
  }
  
  .quiz-meta-grid {
    grid-template-columns: 1fr;
    gap: 6px;
  }
  
  .quiz-card {
    padding: 14px;
  }
  
  .quiz-title {
    font-size: 14px;
  }
  
  /* Mobile Accordion Styles */
  .questions-container {
    padding: 16px;
  }
  
  .accordion-header {
    padding: 12px 16px;
  }
  
  .question-info {
    gap: 12px;
  }
  
  .question-number-badge {
    width: 36px;
    height: 36px;
    font-size: 14px;
  }
  
  .question-title {
    font-size: 14px;
  }
  
  .accordion-content {
    padding: 16px;
  }
  
  .question-full-text {
    font-size: 14px;
    padding: 12px;
  }
  
  .option-item {
    padding: 12px;
  }
  
  .option-letter {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }
  
  .option-text {
    font-size: 13px;
  }
  
  .quiz-header-bar {
    padding: 16px 20px;
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .quiz-info h2 {
    font-size: 20px;
  }
  
  .quiz-timer {
    align-self: flex-end;
  }
}

/* Quiz Interface Styles */
.quiz-interface {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.quiz-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px 12px 0 0;
}

.quiz-info h2 {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.quiz-info p {
  font-size: 14px;
  margin: 0;
  opacity: 0.9;
}

.quiz-timer {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.timer-text {
  font-weight: 600;
  font-size: 16px;
}

.exit-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
}

.exit-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.quiz-progress {
  padding: 16px 24px;
  background: white;
  border-bottom: 1px solid #E0E0E0;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #F0F0F0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
  border-radius: 4px;
}

.progress-text {
  font-size: 14px;
  color: #666;
  text-align: center;
}

/* Accordion Questions Container */
.questions-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: #F8F9FA;
}

.accordion-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.accordion-item {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #E0E0E0;
  overflow: hidden;
  transition: all 0.3s ease;
}

.accordion-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-1px);
}

.accordion-item.active {
  border-color: #667eea;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.15);
}

.accordion-item.answered {
  border-color: #38a169;
  background: linear-gradient(135deg, #ffffff 0%, #f0fff4 100%);
}

.accordion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
}

.accordion-item.active .accordion-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.accordion-item.answered .accordion-header {
  background: linear-gradient(135deg, #38a169 0%, #48bb78 100%);
  color: white;
}

.question-info {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.question-number-badge {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  font-weight: 600;
  font-size: 16px;
  flex-shrink: 0;
}

.accordion-item.answered .question-number-badge {
  background: linear-gradient(135deg, #38a169 0%, #48bb78 100%);
}

.status-indicator {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 16px;
  height: 16px;
  background: #38a169;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.status-indicator.answered {
  opacity: 1;
}

.status-indicator svg {
  color: white;
}

.question-preview {
  flex: 1;
}

.question-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.question-meta {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.answer-status {
  font-size: 12px;
  font-weight: 500;
  padding: 4px 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  backdrop-filter: blur(10px);
}

.accordion-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
}

.accordion-item.active .accordion-toggle {
  transform: rotate(180deg);
}

.accordion-content {
  padding: 20px;
  background: white;
  border-top: 1px solid #E0E0E0;
}

.question-full-text {
  font-size: 16px;
  line-height: 1.6;
  color: #1A1A1A;
  margin-bottom: 24px;
  padding: 16px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.options-container {
  display: grid;
  gap: 12px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border: 2px solid #E0E0E0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.option-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
  transition: left 0.5s;
}

.option-item:hover::before {
  left: 100%;
}

.option-item:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
  transform: translateY(-1px);
}

.option-item.selected {
  border-color: #667eea;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.25);
}

.option-letter {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.option-item.selected .option-letter {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.option-text {
  flex: 1;
  font-size: 14px;
  line-height: 1.5;
}

.quiz-submit-section {
  display: flex;
  justify-content: center;
  padding: 24px 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-top: 24px;
}

/* Difficulty Badge Styles */
.difficulty-easy {
  background: linear-gradient(135deg, #38a169 0%, #48bb78 100%);
  color: white;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.difficulty-medium {
  background: linear-gradient(135deg, #d69e2e 0%, #f6e05e 100%);
  color: white;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.difficulty-hard {
  background: linear-gradient(135deg, #e53e3e 0%, #fc8181 100%);
  color: white;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Quiz Placeholder */
.quiz-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 400px;
}

.placeholder-content {
  text-align: center;
  max-width: 400px;
  padding: 40px 20px;
}

.placeholder-icon {
  color: #999;
  margin-bottom: 24px;
}

.placeholder-content h3 {
  font-size: 24px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0 0 12px 0;
}

.placeholder-content p {
  font-size: 16px;
  color: #666;
  margin: 0;
  line-height: 1.5;
}
</style>
