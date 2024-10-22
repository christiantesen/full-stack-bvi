<template>
  <nav class="bg-blue-600 text-white shadow-lg">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <router-link to="/" class="flex items-center space-x-2">
          <BookOpen class="h-8 w-8" />
          <span class="text-xl font-bold">Virtual Library</span>
        </router-link>
        <div class="flex items-center space-x-4">
          <router-link to="/publications" class="hover:text-blue-200">Publications</router-link>
          <router-link to="/favorites" class="hover:text-blue-200">Favorites</router-link>
          <router-link to="/read-later" class="hover:text-blue-200">Read Later</router-link>
          <router-link to="/profile" class="flex items-center space-x-1 hover:text-blue-200">
            <User class="h-5 w-5" />
            <span>Profile</span>
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script lang="ts" setup>
import { BookOpen, User } from 'lucide-vue-next';
</script>