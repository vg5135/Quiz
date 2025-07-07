<template>
  <div class="quiz-layout">
    <!-- Collapsible Sidebar -->
    <aside class="quiz-sidebar" :class="{ 'collapsed': isSidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo-section">
          <div class="logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM19 19H5V5H19V19ZM7 10H9V17H7V10ZM11 7H13V17H11V7ZM15 13H17V17H15V13Z" fill="currentColor"/>
            </svg>
          </div>
          <h1 class="logo-text" v-show="!isSidebarCollapsed">QuizMaster</h1>
        </div>
      </div>
      
      <nav class="sidebar-nav">
        <button 
          @click="setActiveFilter('all')" 
          class="nav-item"
          :class="{ active: activeFilter === 'all' }"
          :title="isSidebarCollapsed ? 'All Quizzes' : ''"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM19 19H5V5H19V19ZM7 10H9V17H7V10ZM11 7H13V17H11V7ZM15 13H17V17H15V13Z" fill="currentColor"/>
          </svg>
          <span v-show="!isSidebarCollapsed">All Quizzes</span>
          <span v-show="!isSidebarCollapsed" class="nav-count">{{ quizzes.length }}</span>
        </button>
        <button 
          @click="setActiveFilter('active')" 
          class="nav-item"
          :class="{ active: activeFilter === 'active' }"
          :title="isSidebarCollapsed ? 'Active Quizzes' : ''"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z" fill="currentColor"/>
          </svg>
          <span v-show="!isSidebarCollapsed">Active</span>
          <span v-show="!isSidebarCollapsed" class="nav-count">{{ activeQuizzes.length }}</span>
        </button>
        <button 
          @click="setActiveFilter('upcoming')" 
          class="nav-item"
          :class="{ active: activeFilter === 'upcoming' }"
          :title="isSidebarCollapsed ? 'Upcoming Quizzes' : ''"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM12 20C7.58 20 4 16.42 4 12S7.58 4 12 4 20 7.58 20 12 16.42 20 12 20Z" fill="currentColor"/>
            <path d="M12.5 7H11V13L16.25 16.15L17 14.92L12.5 12.25V7Z" fill="currentColor"/>
          </svg>
          <span v-show="!isSidebarCollapsed">Upcoming</span>
          <span v-show="!isSidebarCollapsed" class="nav-count">{{ upcomingQuizzes.length }}</span>
        </button>
        <button 
          @click="setActiveFilter('expired')" 
          class="nav-item"
          :class="{ active: activeFilter === 'expired' }"
          :title="isSidebarCollapsed ? 'Expired Quizzes' : ''"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z" fill="currentColor"/>
          </svg>
          <span v-show="!isSidebarCollapsed">Expired</span>
          <span v-show="!isSidebarCollapsed" class="nav-count">{{ expiredQuizzes.length }}</span>
        </button>
        <button 
          @click="toggleQuizSummary" 
          class="nav-item"
          :class="{ active: showQuizSummary }"
          :title="isSidebarCollapsed ? 'Quiz Summary' : ''"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM19 19H5V5H19V19ZM7 10H9V17H7V10ZM11 7H13V17H11V7ZM15 13H17V17H15V13Z" fill="currentColor"/>
          </svg>
          <span v-show="!isSidebarCollapsed">Summary</span>
          <span v-show="!isSidebarCollapsed" class="nav-count" v-if="completedQuizzes.length > 0">{{ completedQuizzes.length }}</span>
        </button>
        <button 
          @click="openNotes" 
          class="nav-item"
          :class="{ active: showNotes }"
          :title="isSidebarCollapsed ? 'Notes' : ''"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M14 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.89 22 6 22H18C19.1 22 20 21.1 20 20V8L14 2ZM18 20H6V4H13V9H18V20ZM8 12H16V14H8V12ZM8 16H13V18H8V16Z" fill="currentColor"/>
          </svg>
          <span v-show="!isSidebarCollapsed">Notes</span>
        </button>
      </nav>
      
      <!-- Sidebar Toggle Button -->
      <button @click="toggleSidebar" class="sidebar-toggle-btn" :title="isSidebarCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'">
        <svg v-if="!isSidebarCollapsed" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M15.41 16.59L10.83 12L15.41 7.41L14 6L8 12L14 18L15.41 16.59Z" fill="currentColor"/>
        </svg>
        <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M8.59 16.59L13.17 12L8.59 7.41L10 6L16 12L10 18L8.59 16.59Z" fill="currentColor"/>
        </svg>
      </button>
    </aside>

    <!-- Main Content Area -->
    <div class="main-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <!-- Header -->
      <header class="dashboard-header">
        <div class="header-content">
          <div class="header-left">
            <h1 class="page-title">Quiz Dashboard</h1>
            <p class="page-subtitle">Select and take quizzes to test your knowledge</p>
          </div>
          <div class="header-right">
            <div class="user-info">
              <div class="user-details">
                <span class="user-name">{{ userFullName || 'Student' }}</span>
                <span class="user-role">Student</span>
              </div>
              <div class="user-avatar">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z" fill="currentColor"/>
                </svg>
              </div>
              <button @click="logout" class="logout-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M17 7L15.59 8.41L18.17 11H8V13H18.17L15.59 15.59L17 17L22 12L17 7ZM4 5H12V3H4C2.9 3 2 3.9 2 5V19C2 20.1 2.9 21 4 21H12V19H4V5Z" fill="currentColor"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="page-content">
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
                        <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM12 20C7.58 20 4 16.42 4 12S7.58 4 12 4 20 7.58 20 12 16.42 20 12 20Z" fill="currentColor"/>
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

        <!-- Main Quiz Content -->
        <div class="quiz-content">
          <!-- Search and Sort Controls -->
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

          <!-- Quiz Grid -->
          <div class="quiz-grid-container">
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

          <!-- Quiz Taking Interface -->
          <div v-if="selectedQuiz" class="quiz-taking-interface">
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
      </main>
    </div>

    <!-- Notes Popover -->
    <Notes 
      :isVisible="showNotes" 
      @close="closeNotes"
    />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import Notes from './Notes.vue';
// Import all the reactive variables and functions from the external script file
import {
  userFullName,
  quizzes,
  questions,
  chapters,
  subjects,
  selectedQuiz,
  quizQuestions,
  currentQuestionIndex,
  selectedAnswers,
  timeRemaining,
  quizDuration,
  showResults,
  correctAnswers,
  completedQuizzes,
  showQuizSummary,
  quizResults,
  performanceTrend,
  studyStreak,
  activeFilter,
  searchQuery,
  sortBy,
  isSidebarCollapsed,
  filteredQuizzes,
  activeQuizzes,
  upcomingQuizzes,
  expiredQuizzes,
  currentQuestion,
  totalTimeSpent,
  averageScore,
  bestScore,
  logout,
  fetchData,
  fetchQuizHistory,
  getStatusBadge,
  getSubjectNameFromChapter,
  getChapterName,
  getDifficultyBadge,
  formatDate,
  formatTime,
  debugSelectQuiz,
  selectQuiz,
  startTimer,
  selectAnswer,
  submitQuiz,
  finishQuiz,
  exitQuiz,
  toggleQuizSummary,
  closeQuizSummary,
  loadQuizResults,
  getScoreBadgeClass,
  getTrendClass,
  setActiveFilter,
  toggleSidebar,
  isExpired,
  isUpcoming,
  getQuizStatusClass,
  getQuizStatusText,
  getEmptyStateTitle,
  getEmptyStateMessage
} from './QuizView.script.js';

// Add router functionality directly in the component
const router = useRouter();

// Notes popover state
const showNotes = ref(false);

const openNotes = () => {
  showNotes.value = true;
};

const closeNotes = () => {
  showNotes.value = false;
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
@import './QuizView.style.css';
</style>


