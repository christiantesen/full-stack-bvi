import { defineStore } from 'pinia';
import { User } from '@/types';
import apiClient from '@/services/api';
import { ENDPOINTS } from '@/config/api.config';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    token: null as string | null,
    isAuthenticated: false
  }),

  actions: {
    async login(credentials: { email: string; password: string }) {
      try {
        const response = await apiClient.post(ENDPOINTS.AUTH.LOGIN, credentials);
        // Handle login logic
      } catch (error) {
        // Handle error
      }
    }
    // Add more auth actions
  }
});