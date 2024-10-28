<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const email = ref('');
const password = ref('');

const handleLogin = async () => {
  await authStore.login({ email: email.value, password: password.value });
};
</script>

<template>
  <div class="login">
    <form @submit.prevent="handleLogin">
      <h2>Login</h2>
      <div class="form-group">
        <input 
          v-model="email"
          type="email"
          placeholder="Email"
          required
        />
      </div>
      <div class="form-group">
        <input 
          v-model="password"
          type="password"
          placeholder="Password"
          required
        />
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<style scoped lang="scss">
.login {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  
  form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .form-group {
    input {
      width: 100%;
      padding: 0.5rem;
      border: 1px solid #ddd;
      border-radius: 4px;
    }
  }

  button {
    padding: 0.5rem;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;

    &:hover {
      opacity: 0.9;
    }
  }
}</style>