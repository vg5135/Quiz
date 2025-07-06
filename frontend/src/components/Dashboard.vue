<template>
  <div class="dashboard-container">
    <!-- Header -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="currentColor"/>
              <path d="M19 15L19.74 17.74L22.5 18.5L19.74 19.26L19 22L18.26 19.26L15.5 18.5L18.26 17.74L19 15Z" fill="currentColor"/>
              <path d="M5 6L5.5 7.5L7 8L5.5 8.5L5 10L4.5 8.5L3 8L4.5 7.5L5 6Z" fill="currentColor"/>
            </svg>
          </div>
          <h1 class="logo-text">QuizMaster</h1>
        </div>
        <div class="user-section">
          <div class="user-info">
            <span class="user-name">{{ userFullName || 'User' }}</span>
            <span class="user-role">{{ isAdmin ? 'Administrator' : 'Student' }}</span>
          </div>
          <button @click="logout" class="logout-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M17 7L15.59 8.41L18.17 11H8V13H18.17L15.59 15.59L17 17L22 12L17 7ZM4 5H12V3H4C2.9 3 2 3.9 2 5V19C2 20.1 2.9 21 4 21H12V19H4V5Z" fill="currentColor"/>
            </svg>
            Logout
          </button>
        </div>
      </div>
    </header>

    <div class="dashboard-content">
      <!-- Sidebar for Admin Users -->
      <aside class="dashboard-sidebar" v-if="isAdmin">
        <nav class="sidebar-nav">
          <button 
            @click="navigateToAdminDashboard" 
            class="nav-item"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 13H11V3H3V13ZM3 21H11V15H3V21ZM13 21H21V11H13V21ZM13 3V9H21V3H13Z" fill="currentColor"/>
            </svg>
            <span>Admin Dashboard</span>
          </button>
          <button 
            @click="navigateToUsers" 
            class="nav-item"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 4C16 5.10457 15.1046 6 14 6C12.8954 6 12 5.10457 12 4C12 2.89543 12.8954 2 14 2C15.1046 2 16 2.89543 16 4ZM21 10V9C21 7.89543 20.1046 7 19 7C18.6357 7 18.2942 7.09739 17.9999 7.26722C17.9999 7.08908 18 6.91077 18 6.73242C18 4.6863 16.2091 3 14 3C12.3438 3 10.8438 3.78778 10 5.02113C9.15625 3.78778 7.65625 3 6 3C3.79086 3 2 4.6863 2 6.73242C2 6.91077 2.00008 7.08908 2.00008 7.26722C1.70581 7.09739 1.36426 7 1 7C-0.104569 7 -1 7.89543 -1 9V10C-1 11.1046 -0.104569 12 1 12H21C22.1046 12 23 11.1046 23 10ZM8 17C8 15.8954 7.10457 15 6 15C4.89543 15 4 15.8954 4 17C4 18.1046 4.89543 19 6 19C7.10457 19 8 18.1046 8 17ZM22 17C22 15.8954 21.1046 15 20 15C18.8954 15 18 15.8954 18 17C18 18.1046 18.8954 19 20 19C21.1046 19 22 18.1046 22 17ZM13 15C13 13.8954 12.1046 13 11 13C9.89543 13 9 13.8954 9 15C9 16.1046 9.89543 17 11 17C12.1046 17 13 16.1046 13 15Z" fill="currentColor"/>
            </svg>
            <span>User Management</span>
          </button>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="dashboard-main">
        <template v-if="isAdmin">
          <div class="content-wrapper">
            <div class="welcome-section">
              <h2>Welcome to QuizMaster Admin</h2>
              <p>Use the navigation buttons to access different admin functions.</p>
            </div>
            
            <div class="quick-actions">
              <h3>Quick Actions</h3>
              <div class="actions-grid">
                <div class="action-card" @click="navigateToAdminDashboard">
                  <div class="action-icon">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M3 13H11V3H3V13ZM3 21H11V15H3V21ZM13 21H21V11H13V21ZM13 3V9H21V3H13Z" fill="currentColor"/>
                    </svg>
                  </div>
                  <div class="action-content">
                    <h4>Admin Dashboard</h4>
                    <p>Access the full admin panel</p>
                  </div>
                </div>
                
                <div class="action-card" @click="navigateToUsers">
                  <div class="action-icon">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M16 4C16 5.10457 15.1046 6 14 6C12.8954 6 12 5.10457 12 4C12 2.89543 12.8954 2 14 2C15.1046 2 16 2.89543 16 4ZM21 10V9C21 7.89543 20.1046 7 19 7C18.6357 7 18.2942 7.09739 17.9999 7.26722C17.9999 7.08908 18 6.91077 18 6.73242C18 4.6863 16.2091 3 14 3C12.3438 3 10.8438 3.78778 10 5.02113C9.15625 3.78778 7.65625 3 6 3C3.79086 3 2 4.6863 2 6.73242C2 6.91077 2.00008 7.08908 2.00008 7.26722C1.70581 7.09739 1.36426 7 1 7C-0.104569 7 -1 7.89543 -1 9V10C-1 11.1046 -0.104569 12 1 12H21C22.1046 12 23 11.1046 23 10ZM8 17C8 15.8954 7.10457 15 6 15C4.89543 15 4 15.8954 4 17C4 18.1046 4.89543 19 6 19C7.10457 19 8 18.1046 8 17ZM22 17C22 15.8954 21.1046 15 20 15C18.8954 15 18 15.8954 18 17C18 18.1046 18.8954 19 20 19C21.1046 19 22 18.1046 22 17ZM13 15C13 13.8954 12.1046 13 11 13C9.89543 13 9 13.8954 9 15C9 16.1046 9.89543 17 11 17C12.1046 17 13 16.1046 13 15Z" fill="currentColor"/>
                    </svg>
                  </div>
                  <div class="action-content">
                    <h4>User Management</h4>
                    <p>Manage users and permissions</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
        <template v-else>
          <QuizView />
        </template>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import QuizView from "./QuizView.vue";

const router = useRouter();
const isAdmin = ref(false);
const userFullName = ref("");

const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  router.push("/login");
};

const navigateToAdminDashboard = () => {
  router.push("/admin");
};

const navigateToUsers = () => {
  router.push("/admin/users");
};

onMounted(() => {
  if (!localStorage.getItem("token")) {
    router.push("/login");
  }
  isAdmin.value = localStorage.getItem("role") === "admin";
  // Get user info from localStorage or set default
  userFullName.value = localStorage.getItem("userFullName") || "User";
});
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  width: 100vw;
  background-color: #F5F6FA;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.dashboard-header {
  background: white;
  border-bottom: 1px solid #E0E0E0;
  padding: 0 32px;
  height: 72px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  width: 100vw;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin: 0 auto;
  max-width: none;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
  color: white;
  padding: 8px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
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

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: none;
  color: #666;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: #F5F5F5;
  color: #1976D2;
}

.dashboard-content {
  display: flex;
  flex: 1;
  width: 100vw;
  margin: 0 auto;
  padding: 32px;
  gap: 32px;
  max-width: none;
}

.dashboard-sidebar {
  width: 280px;
  flex-shrink: 0;
}

.sidebar-nav {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 8px;
  border: 1px solid #E0E0E0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: none;
  background: transparent;
  color: #666;
  font-size: 14px;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  width: 100%;
}

.nav-item:hover {
  background: #E3F2FD;
  color: #1976D2;
}

.nav-item svg {
  flex-shrink: 0;
}

.dashboard-main {
  flex: 1;
  min-width: 0;
  width: 100%;
}

.content-wrapper {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  min-height: calc(100vh - 200px);
  width: 100%;
  border: 1px solid #E0E0E0;
}

.welcome-section {
  text-align: center;
  padding: 48px 24px;
  margin-bottom: 48px;
}

.welcome-section h2 {
  font-size: 32px;
  font-weight: 700;
  color: #1A1A1A;
  margin-bottom: 16px;
}

.welcome-section p {
  font-size: 16px;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.quick-actions {
  margin-bottom: 32px;
}

.quick-actions h3 {
  font-size: 20px;
  font-weight: 600;
  color: #1A1A1A;
  margin-bottom: 24px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
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

.action-content h4 {
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

/* Responsive Design */
@media (max-width: 1024px) {
  .dashboard-content {
    flex-direction: column;
    padding: 24px 16px;
    width: 100vw;
  }
  
  .dashboard-sidebar {
    width: 100%;
  }
  
  .sidebar-nav {
    flex-direction: row;
    overflow-x: auto;
    padding: 16px;
    width: 100%;
  }
  
  .nav-item {
    white-space: nowrap;
    min-width: 160px;
  }
}

@media (min-width: 1400px) {
  .dashboard-content {
    padding: 32px 48px;
    width: 100vw;
  }
  
  .content-wrapper {
    padding: 48px;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    padding: 0 16px;
    height: 64px;
    width: 100vw;
  }
  
  .header-content {
    flex-direction: column;
    gap: 12px;
    text-align: center;
    width: 100%;
  }
  
  .user-section {
    flex-direction: column;
    gap: 8px;
  }
  
  .user-info {
    align-items: center;
  }
  
  .dashboard-content {
    padding: 16px;
    width: 100vw;
  }
  
  .content-wrapper {
    padding: 24px;
    width: 100%;
  }
  
  .welcome-section {
    padding: 32px 16px;
  }
  
  .welcome-section h2 {
    font-size: 24px;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
    width: 100%;
  }
  
  .action-card {
    padding: 20px;
    width: 100%;
  }
  
  .action-icon {
    width: 48px;
    height: 48px;
  }
}

/* Animation for page transitions */
.content-wrapper > * {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
