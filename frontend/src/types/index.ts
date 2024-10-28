// Global type definitions
export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
}

export enum UserRole {
  ADMIN = 'admin',
  USER = 'user'
}

export interface ApiResponse<T> {
  data: T;
  message: string;
  status: number;
}

// Add more interfaces and types as needed