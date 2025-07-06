<template>
  <AdminLayout>
    <!-- Stats Overview -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 4C16 5.10457 15.1046 6 14 6C12.8954 6 12 5.10457 12 4C12 2.89543 12.8954 2 14 2C15.1046 2 16 2.89543 16 4ZM21 10V9C21 7.89543 20.1046 7 19 7C18.6357 7 18.2942 7.09739 17.9999 7.26722C17.9999 7.08908 18 6.91077 18 6.73242C18 4.6863 16.2091 3 14 3C12.3438 3 10.8438 3.78778 10 5.02113C9.15625 3.78778 7.65625 3 6 3C3.79086 3 2 4.6863 2 6.73242C2 6.91077 2.00008 7.08908 2.00008 7.26722C1.70581 7.09739 1.36426 7 1 7C-0.104569 7 -1 7.89543 -1 9V10C-1 11.1046 -0.104569 12 1 12H21C22.1046 12 23 11.1046 23 10ZM8 17C8 15.8954 7.10457 15 6 15C4.89543 15 4 15.8954 4 17C4 18.1046 4.89543 19 6 19C7.10457 19 8 18.1046 8 17ZM22 17C22 15.8954 21.1046 15 20 15C18.8954 15 18 15.8954 18 17C18 18.1046 18.8954 19 20 19C21.1046 19 22 18.1046 22 17ZM13 15C13 13.8954 12.1046 13 11 13C9.89543 13 9 13.8954 9 15C9 16.1046 9.89543 17 11 17C12.1046 17 13 16.1046 13 15Z" fill="currentColor"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalUsers }}</div>
          <div class="stat-label">Total Users</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 5V7H15V5H9M3 5V7H7V5H3M9 9V11H15V9H9M3 9V11H7V9H3M9 13V15H15V13H9M3 13V15H7V13H3M9 17V19H15V17H9M3 17V19H7V17H3M19 5V19H21V5H19Z" fill="currentColor"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalQuizzes }}</div>
          <div class="stat-label">Total Quizzes</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 3L1 9L12 15L21 10.09V17H23V9M5 13.18V17.18L12 21L19 17.18V13.18L12 17L5 13.18Z" fill="currentColor"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalSubjects }}</div>
          <div class="stat-label">Total Subjects</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 3H5C3.89 3 3 3.89 3 5V19A2 2 0 0 0 5 21H19A2 2 0 0 0 21 19V5C21 3.89 20.1 3 19 3M19 5V19H5V5H19Z" fill="currentColor"/>
            <path d="M7 7H17V9H7V7M7 11H17V13H7V11M7 15H14V17H7V15Z" fill="currentColor"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalChapters }}</div>
          <div class="stat-label">Total Chapters</div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions">
      <h2 class="section-title">Quick Actions</h2>
      <div class="actions-grid">
        <div class="action-card" @click="navigateTo('/admin/users')">
          <div class="action-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 4C16 5.10457 15.1046 6 14 6C12.8954 6 12 5.10457 12 4C12 2.89543 12.8954 2 14 2C15.1046 2 16 2.89543 16 4ZM21 10V9C21 7.89543 20.1046 7 19 7C18.6357 7 18.2942 7.09739 17.9999 7.26722C17.9999 7.08908 18 6.91077 18 6.73242C18 4.6863 16.2091 3 14 3C12.3438 3 10.8438 3.78778 10 5.02113C9.15625 3.78778 7.65625 3 6 3C3.79086 3 2 4.6863 2 6.73242C2 6.91077 2.00008 7.08908 2.00008 7.26722C1.70581 7.09739 1.36426 7 1 7C-0.104569 7 -1 7.89543 -1 9V10C-1 11.1046 -0.104569 12 1 12H21C22.1046 12 23 11.1046 23 10ZM8 17C8 15.8954 7.10457 15 6 15C4.89543 15 4 15.8954 4 17C4 18.1046 4.89543 19 6 19C7.10457 19 8 18.1046 8 17ZM22 17C22 15.8954 21.1046 15 20 15C18.8954 15 18 15.8954 18 17C18 18.1046 18.8954 19 20 19C21.1046 19 22 18.1046 22 17ZM13 15C13 13.8954 12.1046 13 11 13C9.89543 13 9 13.8954 9 15C9 16.1046 9.89543 17 11 17C12.1046 17 13 16.1046 13 15Z" fill="currentColor"/>
            </svg>
          </div>
          <div class="action-content">
            <h3>User Management</h3>
            <p>Manage users, view details, and control access</p>
          </div>
        </div>
        
        <div class="action-card" @click="navigateTo('/admin/quizzes')">
          <div class="action-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 5V7H15V5H9M3 5V7H7V5H3M9 9V11H15V9H9M3 9V11H7V9H3M9 13V15H15V13H9M3 13V15H7V13H3M9 17V19H15V17H9M3 17V19H7V17H3M19 5V19H21V5H19Z" fill="currentColor"/>
            </svg>
          </div>
          <div class="action-content">
            <h3>Quiz Management</h3>
            <p>Create, edit, and manage quizzes</p>
          </div>
        </div>
        
        <div class="action-card" @click="navigateTo('/admin/subjects')">
          <div class="action-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 3L1 9L12 15L21 10.09V17H23V9M5 13.18V17.18L12 21L19 17.18V13.18L12 17L5 13.18Z" fill="currentColor"/>
            </svg>
          </div>
          <div class="action-content">
            <h3>Subject Management</h3>
            <p>Manage subjects and chapters</p>
          </div>
        </div>
        
        <div class="action-card" @click="navigateTo('/admin/questions')">
          <div class="action-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M11 18H13V16H11V18ZM12 2C6.48 2 2 6.48 2 12S6.48 22 12 22 22 17.52 22 12 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12S7.59 4 12 4 20 7.59 20 12 16.41 20 12 20ZM12 6C9.79 6 8 7.79 8 10H10C10 8.9 10.9 8 12 8S14 8.9 14 10C14 12 11 11.75 11 15H13C13 12.75 16 12.5 16 10C16 7.79 14.21 6 12 6Z" fill="currentColor"/>
            </svg>
          </div>
          <div class="action-content">
            <h3>Question Management</h3>
            <p>Create and manage quiz questions</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="recent-activity">
      <h2 class="section-title">Recent Activity</h2>
      <div class="activity-list">
        <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
          <div class="activity-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12S6.48 22 12 22 22 17.52 22 12 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12S7.59 4 12 4 20 7.59 20 12 16.41 20 12 20ZM12.5 7V12.25L17 14.92L16.25 16.15L11 13V7H12.5Z" fill="currentColor"/>
            </svg>
          </div>
          <div class="activity-content">
            <div class="activity-text">{{ activity.text }}</div>
            <div class="activity-time">{{ formatTime(activity.time) }}</div>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import AdminLayout from './AdminLayout.vue';
import { listUsers, getQuizzes, getSubjects, getChapters } from '../../api';

const router = useRouter();

// Reactive data
const stats = ref({
  totalUsers: 0,
  totalQuizzes: 0,
  totalSubjects: 0,
  totalChapters: 0
});

const recentActivities = ref([
  {
    id: 1,
    text: 'New user registered: John Doe',
    time: new Date(Date.now() - 1000 * 60 * 30) // 30 minutes ago
  },
  {
    id: 2,
    text: 'Quiz "Mathematics Basics" created',
    time: new Date(Date.now() - 1000 * 60 * 60 * 2) // 2 hours ago
  },
  {
    id: 3,
    text: 'New subject "Physics" added',
    time: new Date(Date.now() - 1000 * 60 * 60 * 4) // 4 hours ago
  },
  {
    id: 4,
    text: 'Chapter "Mechanics" updated',
    time: new Date(Date.now() - 1000 * 60 * 60 * 6) // 6 hours ago
  }
]);

// Methods
const fetchStats = async () => {
  try {
    const [users, quizzes, subjects, chapters] = await Promise.all([
      listUsers(),
      getQuizzes(),
      getSubjects(),
      getChapters()
    ]);

    stats.value = {
      totalUsers: users.length,
      totalQuizzes: quizzes.length,
      totalSubjects: subjects.length,
      totalChapters: chapters.length
    };
  } catch (error) {
    console.error('Error fetching stats:', error);
  }
};

const navigateTo = (path) => {
  router.push(path);
};

const formatTime = (time) => {
  const now = new Date();
  const diff = now - time;
  const minutes = Math.floor(diff / (1000 * 60));
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));

  if (minutes < 60) return `${minutes} minutes ago`;
  if (hours < 24) return `${hours} hours ago`;
  return `${days} days ago`;
};

onMounted(() => {
  fetchStats();
});
</script>

<style scoped>
/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
  width: 100%;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #E0E0E0;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.2s ease;
}

.stat-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.stat-icon {
  width: 48px;
  height: 48px;
  background: #E3F2FD;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1976D2;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1A1A1A;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

/* Quick Actions */
.quick-actions {
  margin-bottom: 40px;
  width: 100%;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 24px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  width: 100%;
}

.action-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #E0E0E0;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 16px;
}

.action-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
  border-color: #1976D2;
}

.action-icon {
  width: 56px;
  height: 56px;
  background: #E3F2FD;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1976D2;
  flex-shrink: 0;
}

.action-content {
  flex: 1;
}

.action-content h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0 0 4px 0;
}

.action-content p {
  font-size: 14px;
  color: #666;
  margin: 0;
  line-height: 1.4;
}

/* Recent Activity */
.recent-activity {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #E0E0E0;
  width: 100%;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #F8F9FA;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.activity-item:hover {
  background: #E3F2FD;
}

.activity-icon {
  width: 32px;
  height: 32px;
  background: #E3F2FD;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1976D2;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: 14px;
  font-weight: 500;
  color: #1A1A1A;
  margin-bottom: 2px;
}

.activity-time {
  font-size: 12px;
  color: #666;
}

/* Responsive Design */
@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .stat-card,
  .action-card {
    padding: 20px;
  }
  
  .stat-value {
    font-size: 28px;
  }
  
  .action-icon {
    width: 48px;
    height: 48px;
  }
}
</style> 