<template>
  <div class="auth-root">
    <!-- Left: Form -->
    <div class="auth-left">
      <div class="auth-brand">
        <div class="brand-logo">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM19 19H5V5H19V19ZM7 10H9V17H7V10ZM11 7H13V17H11V7ZM15 13H17V17H15V13Z" fill="currentColor"/>
          </svg>
        </div>
        <span class="brand-name">QuizMaster</span>
      </div>
      <div class="auth-form-wrapper">
        <h1 class="auth-title">Create your account</h1>
        <p class="auth-subtitle">Please enter your details to get started</p>
        
        <div v-if="error" class="error-message">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12S6.48 22 12 22 22 17.52 22 12 17.52 2 12 2ZM13 17H11V15H13V17ZM13 13H11V7H13V13Z" fill="currentColor"/>
          </svg>
          {{ error }}
        </div>
        
        <div v-if="success" class="success-message">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" fill="currentColor"/>
          </svg>
          {{ success }}
        </div>
        
        <form class="auth-form" @submit.prevent="handleRegister">
          <div class="form-group">
            <label for="name" class="form-label">Full Name</label>
            <input 
              id="name" 
              v-model="name" 
              class="form-input" 
              placeholder="Enter your full name" 
              required 
            />
          </div>
          <div class="form-group">
            <label for="email" class="form-label">Email address</label>
            <input 
              id="email" 
              v-model="email" 
              class="form-input" 
              type="email" 
              placeholder="Enter your email" 
              required 
            />
          </div>
          <div class="form-group">
            <label for="password" class="form-label">Password</label>
            <input 
              id="password" 
              v-model="password" 
              class="form-input" 
              type="password" 
              placeholder="Create a strong password" 
              required 
            />
          </div>
          <button type="submit" class="btn btn-primary btn-block" :disabled="isLoading">
            <div v-if="isLoading" class="loading-spinner"></div>
            <span v-else>Create account</span>
          </button>
          <div class="divider">
            <span>or</span>
          </div>
          <button type="button" class="btn btn-google btn-block">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22.56 12.25C22.56 11.47 22.49 10.72 22.35 10H12V14.26H17.92C17.66 15.63 16.92 16.79 15.91 17.57V20.84H19.28C21.36 18.92 22.56 15.91 22.56 12.25Z" fill="#4285F4"/>
              <path d="M12 23C15.24 23 17.95 22.01 19.28 20.84L15.91 17.57C15.03 18.18 13.82 18.58 12 18.58C8.87 18.58 6.22 16.58 5.28 13.84H1.82V17.18C3.15 20.01 7.23 23 12 23Z" fill="#34A853"/>
              <path d="M5.28 13.84C5.08 13.19 4.97 12.5 4.97 11.79C4.97 11.08 5.08 10.39 5.28 9.74V6.4H1.82C1.12 7.79 0.72 9.26 0.72 10.79C0.72 12.32 1.12 13.79 1.82 15.18L5.28 13.84Z" fill="#FBBC05"/>
              <path d="M12 5.02C13.62 5.02 15.06 5.56 16.21 6.66L19.15 3.72C17.45 2.08 14.97 1 12 1C7.23 1 3.15 3.99 1.82 6.82L5.28 9.16C6.22 6.42 8.87 4.42 12 4.42C13.43 4.42 14.74 4.84 15.82 5.56L18.36 3.02C16.95 1.84 15.08 1 12 1Z" fill="#EA4335"/>
            </svg>
            Sign up with Google
          </button>
        </form>
        <div class="auth-footer">
          <span>Already have an account?</span>
          <router-link to="/login" class="auth-link">Sign in</router-link>
        </div>
      </div>
    </div>
    <!-- Right: Illustration -->
    <div class="auth-right">
      <div class="auth-illustration">
        <div class="illustration-content">
          <div class="illustration-icon">
            <svg width="120" height="120" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 4C16 2.9 15.1 2 14 2H10C8.9 2 8 2.9 8 4V6H16V4ZM18 6V4C18 1.79 16.21 0 14 0H10C7.79 0 6 1.79 6 4V6H4C2.9 6 2 6.9 2 8V20C2 21.1 2.9 22 4 22H20C21.1 22 22 21.1 22 20V8C22 6.9 21.1 6 20 6H18ZM20 20H4V8H20V20Z" fill="currentColor"/>
              <path d="M12 12C13.1 12 14 12.9 14 14C14 15.1 13.1 16 12 16C10.9 16 10 15.1 10 14C10 12.9 10.9 12 12 12ZM12 10C9.79 10 8 11.79 8 14C8 16.21 9.79 18 12 18C14.21 18 16 16.21 16 14C16 11.79 14.21 10 12 10Z" fill="currentColor"/>
            </svg>
          </div>
          <h2>Join QuizMaster Today</h2>
          <p>Start your learning journey with our comprehensive assessment platform</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const name = ref("");
const email = ref("");
const password = ref("");
const error = ref("");
const success = ref("");
const isLoading = ref(false);

const handleRegister = async () => {
  error.value = "";
  success.value = "";
  isLoading.value = true;
  
  try {
    const res = await fetch("http://127.0.0.1:5006/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        full_name: name.value,
        email: email.value,
        password: password.value,
      }),
    });
    
    if (!res.ok) {
      const data = await res.json();
      error.value = data.message || "Registration failed. Please try again.";
      return;
    }
    
    success.value = "Registration successful! You can now sign in to your account.";
    name.value = "";
    email.value = "";
    password.value = "";
  } catch (e) {
    error.value = "Network error. Please check your connection and try again.";
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.auth-root {
  display: flex;
  min-height: 100vh;
  background: #F8F9FA;
  width: 100vw;
  height: 100vh;
}

.auth-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 48px 32px;
  background: white;
  width: 50vw;
  height: 100vh;
}

.auth-right {
  flex: 1;
  background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50vw;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.auth-right::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="10" cy="60" r="0.5" fill="white" opacity="0.1"/><circle cx="90" cy="40" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
}

.auth-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 48px;
}

.brand-logo {
  color: #1976D2;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-name {
  font-size: 24px;
  font-weight: 600;
  color: #1A1A1A;
  letter-spacing: -0.02em;
}

.auth-form-wrapper {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  padding: 40px 32px;
  border: 1px solid #E0E0E0;
}

.auth-title {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #1A1A1A;
  text-align: center;
}

.auth-subtitle {
  color: #666;
  font-size: 16px;
  margin-bottom: 32px;
  text-align: center;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(244, 67, 54, 0.1);
  color: #D32F2F;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 24px;
  border: 1px solid rgba(244, 67, 54, 0.2);
}

.success-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(76, 175, 80, 0.1);
  color: #388E3C;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 24px;
  border: 1px solid rgba(76, 175, 80, 0.2);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  color: #1A1A1A;
  font-weight: 500;
}

.form-input {
  padding: 12px 16px;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  font-size: 16px;
  background: #F8F9FA;
  color: #1A1A1A;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #1976D2;
  background: white;
  box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
}

.form-input::placeholder {
  color: #999;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-decoration: none;
}

.btn-block {
  width: 100%;
}

.btn-primary {
  background: #1976D2;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #1565C0;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-google {
  background: white;
  color: #1A1A1A;
  border: 1px solid #E0E0E0;
}

.btn-google:hover {
  background: #F8F9FA;
  border-color: #D0D0D0;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: #666;
  font-size: 14px;
  margin: 8px 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #E0E0E0;
}

.divider span {
  padding: 0 16px;
  background: white;
}

.auth-footer {
  text-align: center;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #F0F0F0;
  color: #666;
  font-size: 14px;
}

.auth-footer span {
  margin-right: 4px;
}

.auth-link {
  color: #1976D2;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s ease;
}

.auth-link:hover {
  color: #1565C0;
  text-decoration: underline;
}

.auth-illustration {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
}

.illustration-content {
  max-width: 400px;
}

.illustration-icon {
  margin-bottom: 24px;
  opacity: 0.9;
}

.illustration-content h2 {
  font-size: 32px;
  font-weight: 600;
  margin: 0 0 16px 0;
  line-height: 1.2;
}

.illustration-content p {
  font-size: 18px;
  line-height: 1.6;
  opacity: 0.9;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .auth-root {
    flex-direction: column;
  }
  
  .auth-left,
  .auth-right {
    width: 100vw;
    height: auto;
    min-height: 50vh;
  }
  
  .auth-left {
    order: 2;
    padding: 32px 24px;
  }
  
  .auth-right {
    order: 1;
    padding: 48px 24px;
  }
  
  .auth-form-wrapper {
    max-width: 100%;
    box-shadow: none;
    border: none;
    padding: 0;
  }
  
  .illustration-content h2 {
    font-size: 24px;
  }
  
  .illustration-content p {
    font-size: 16px;
  }
}

@media (max-width: 768px) {
  .auth-left {
    padding: 24px 16px;
  }
  
  .auth-right {
    padding: 32px 16px;
  }
  
  .auth-title {
    font-size: 24px;
  }
  
  .auth-subtitle {
    font-size: 14px;
  }
  
  .illustration-content h2 {
    font-size: 20px;
  }
  
  .illustration-content p {
    font-size: 14px;
  }
}
</style>
