<template>
  <div class="max-w-2xl mx-auto">
    <h2 class="text-3xl font-bold mb-8">User Profile</h2>
    <div v-if="loading" class="text-center">Loading profile...</div>
    <div v-else-if="error" class="text-center text-red-600">{{ error }}</div>
    <div v-else-if="!user" class="text-center">No user data available.</div>
    <div v-else class="bg-white shadow-md rounded-lg p-6">
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2">Name</label>
        <p class="text-gray-900">{{ user.name }}</p>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2">Email</label>
        <p class="text-gray-900">{{ user.email }}</p>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2">Role</label>
        <p class="text-gray-900 capitalize">{{ user.role }}</p>
      </div>
      <div v-if="user.role === 'teacher' || user.role === 'admin'" class="mt-6">
        <h3 class="text-xl font-semibold mb-4">Management Options</h3>
        <button
          v-if="user.role === 'admin'"
          class="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition duration-300 mr-4"
        >
          Manage Users
        </button>
        <button class="bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700 transition duration-300">
          Manage Publications
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { User } from '../types';

const user = ref<User | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);

const fetchUserProfile = async () => {
  try {
    const response = await fetch('/api/user/profile');
    if (!response.ok) {
      throw new Error('Failed to fetch user profile');
    }
    const data = await response.json();
    user.value = data;
    loading.value = false;
  } catch (err) {
    error.value = 'An error occurred while fetching your profile. Please try again later.';
    loading.value = false;
  }
};

onMounted(fetchUserProfile);
</script>