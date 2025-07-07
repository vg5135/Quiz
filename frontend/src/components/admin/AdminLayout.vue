<template>
  <div class="admin-layout">
    <!-- Collapsible Sidebar -->
    <aside class="admin-sidebar" :class="{ 'collapsed': isSidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo-section">
          <div class="logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="currentColor"/>
            </svg>
          </div>
          <h1 class="logo-text" v-show="!isSidebarCollapsed">QuizMaster</h1>
        </div>
      </div>
      
      <nav class="sidebar-nav">
        <button 
          @click="navigateTo('/admin')" 
          class="nav-item"
          :class="{ active: $route.path === '/admin' }"
          :title="isSidebarCollapsed ? 'Dashboard' : ''"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 13H11V3H3V13ZM3 21H11V15H3V21ZM13 21H21V11H13V21ZM13 3V9H21V3H13Z" fill="currentColor"/>
          </svg>
          <span v-show="!isSidebarCollapsed">Dashboard</span>
        </button>
        <button 
          @click="navigateTo('/admin/users')" 
          class="nav-item"
          :class="{ active: $route.path === '/admin/users' }"
          :title="isSidebarCollapsed ? 'Users' : ''"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 4C16 5.10457 15.1046 6 14 6C12.8954 6 12 5.10457 12 4C12 2.89543 12.8954 2 14 2C15.1046 2 16 2.89543 16 4ZM21 10V9C21 7.89543 20.1046 7 19 7C18.6357 7 18.2942 7.09739 17.9999 7.26722C17.9999 7.08908 18 6.91077 18 6.73242C18 4.6863 16.2091 3 14 3C12.3438 3 10.8438 3.78778 10 5.02113C9.15625 3.78778 7.65625 3 6 3C3.79086 3 2 4.6863 2 6.73242C2 6.91077 2.00008 7.08908 2.00008 7.26722C1.70581 7.09739 1.36426 7 1 7C-0.104569 7 -1 7.89543 -1 9V10C-1 11.1046 -0.104569 12 1 12H21C22.1046 12 23 11.1046 23 10ZM8 17C8 15.8954 7.10457 15 6 15C4.89543 15 4 15.8954 4 17C4 18.1046 4.89543 19 6 19C7.10457 19 8 18.1046 8 17ZM22 17C22 15.8954 21.1046 15 20 15C18.8954 15 18 15.8954 18 17C18 18.1046 18.8954 19 20 19C21.1046 19 22 18.1046 22 17ZM13 15C13 13.8954 12.1046 13 11 13C9.89543 13 9 13.8954 9 15C9 16.1046 9.89543 17 11 17C12.1046 17 13 16.1046 13 15Z" fill="currentColor"/>
          </svg>
          <span v-show="!isSidebarCollapsed">Users</span>
        </button>
        <button 
          @click="navigateTo('/admin/subjects')" 
          class="nav-item"
          :class="{ active: $route.path === '/admin/subjects' }"
          :title="isSidebarCollapsed ? 'Subjects' : ''"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 3L1 9L12 15L21 10.09V17H23V9M5 13.18V17.18L12 21L19 17.18V13.18L12 17L5 13.18Z" fill="currentColor"/>
          </svg>
          <span v-show="!isSidebarCollapsed">Subjects</span>
        </button>
        <button 
          @click="navigateTo('/admin/chapters')" 
          class="nav-item"
          :class="{ active: $route.path === '/admin/chapters' }"
          :title="isSidebarCollapsed ? 'Chapters' : ''"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 3H5C3.89 3 3 3.89 3 5V19A2 2 0 0 0 5 21H19A2 2 0 0 0 21 19V5C21 3.89 20.1 3 19 3M19 5V19H5V5H19Z" fill="currentColor"/>
            <path d="M7 7H17V9H7V7M7 11H17V13H7V11M7 15H14V17H7V15Z" fill="currentColor"/>
          </svg>
          <span v-show="!isSidebarCollapsed">Chapters</span>
        </button>
        <button 
          @click="navigateTo('/admin/quizzes')" 
          class="nav-item"
          :class="{ active: $route.path === '/admin/quizzes' }"
          :title="isSidebarCollapsed ? 'Quizzes' : ''"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 5V7H15V5H9M3 5V7H7V5H3M9 9V11H15V9H9M3 9V11H7V9H3M9 13V15H15V13H9M3 13V15H7V13H3M9 17V19H15V17H9M3 17V19H7V17H3M19 5V19H21V5H19Z" fill="currentColor"/>
          </svg>
          <span v-show="!isSidebarCollapsed">Quizzes</span>
        </button>
        <button 
          @click="navigateTo('/admin/questions')" 
          class="nav-item"
          :class="{ active: $route.path === '/admin/questions' }"
          :title="isSidebarCollapsed ? 'Questions' : ''"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M11 18H13V16H11V18ZM12 2C6.48 2 2 6.48 2 12S6.48 22 12 22 22 17.52 22 12 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12S7.59 4 12 4 20 7.59 20 12 16.41 20 12 20ZM12 6C9.79 6 8 7.79 8 10H10C10 8.9 10.9 8 12 8S14 8.9 14 10C14 12 11 11.75 11 15H13C13 12.75 16 12.5 16 10C16 7.79 14.21 6 12 6Z" fill="currentColor"/>
          </svg>
          <span v-show="!isSidebarCollapsed">Questions</span>
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
            <h1 class="page-title">{{ pageTitle }}</h1>
          </div>
          <div class="header-right">
            <div class="user-info">
              <div class="user-details">
                <span class="user-name">{{ user?.full_name || 'Admin' }}</span>
                <span class="user-role">Administrator</span>
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
        <slot></slot>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

// User data (you might want to get this from your auth store)
const user = ref({
  full_name: 'Admin User'
});

// Page title based on current route
const pageTitle = computed(() => {
  const titles = {
    '/admin': 'Dashboard',
    '/admin/users': 'User Management',
    '/admin/subjects': 'Subject Management',
    '/admin/chapters': 'Chapter Management',
    '/admin/quizzes': 'Quiz Management',
    '/admin/questions': 'Question Management'
  };
  return titles[route.path] || 'Admin Panel';
});

const navigateTo = (path) => {
  router.push(path);
};

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  router.push('/login');
};

const isSidebarCollapsed = ref(false);
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background-color: #F5F6FA;
}

/* Sidebar Styles */
.admin-sidebar {
  width: 280px;
  background: linear-gradient(180deg, #1976D2 0%, #1565C0 100%);
  color: white;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
  z-index: 1000;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  transition: width 0.3s ease;
}

.admin-sidebar.collapsed {
  width: 80px;
}

.admin-sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 12px 8px;
}

.admin-sidebar.collapsed .nav-item span {
  display: none;
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  background: rgba(255, 255, 255, 0.2);
  padding: 8px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: white;
}

.sidebar-nav {
  flex: 1;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  width: 100%;
  border-radius: 0;
  margin: 0 8px;
  border-radius: 8px;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-weight: 600;
}

.nav-item svg {
  flex-shrink: 0;
}

/* Sidebar Toggle Button */
.sidebar-toggle-btn {
  position: absolute;
  top: 50%;
  right: -20px;
  width: 40px;
  height: 40px;
  background: #1976D2;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
  z-index: 1001;
  transform: translateY(-50%);
}

.sidebar-toggle-btn:hover {
  background: #1565C0;
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Main Content Area */
.main-content {
  flex: 1;
  margin-left: 280px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: calc(100vw - 280px);
  transition: margin-left 0.3s ease, width 0.3s ease;
}

.main-content.sidebar-collapsed {
  margin-left: 80px;
  width: calc(100vw - 80px);
}

/* Header Styles */
.dashboard-header {
  background: white;
  border-bottom: 1px solid #E0E0E0;
  padding: 0 32px;
  height: 72px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.header-left {
  display: flex;
  align-items: center;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #1A1A1A;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-details {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #1A1A1A;
}

.user-role {
  font-size: 12px;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: #E3F2FD;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1976D2;
}

.logout-btn {
  background: transparent;
  border: none;
  color: #666;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logout-btn:hover {
  background: #F5F5F5;
  color: #1976D2;
}

/* Page Content */
.page-content {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
  width: 100%;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .admin-sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .admin-sidebar.open {
    transform: translateX(0);
  }
  
  .admin-sidebar.collapsed {
    transform: translateX(-100%);
  }
  
  .main-content {
    margin-left: 0;
    width: 100vw;
  }
  
  .main-content.sidebar-collapsed {
    margin-left: 0;
    width: 100vw;
  }
  
  .page-content {
    padding: 24px 16px;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    padding: 0 16px;
    height: 64px;
    width: 100vw;
  }
  
  .page-title {
    font-size: 20px;
  }
  
  .user-details {
    display: none;
  }
  
  .page-content {
    padding: 16px;
    width: 100%;
  }
  
  .main-content {
    width: 100vw;
  }
}
</style> 