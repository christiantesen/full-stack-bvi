// API Configuration
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000',
  TIMEOUT: 15000,
  RETRY_ATTEMPTS: 3,
  VERSION: 'v1'
}

// API Endpoints
export const ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    REFRESH: '/auth/refresh'
  },
  USERS: {
    BASE: '/users',
    PROFILE: '/users/profile'
  }
  // Add more endpoints as needed
}