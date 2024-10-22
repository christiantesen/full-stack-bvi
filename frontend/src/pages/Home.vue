<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <BookOpen class="h-24 w-24 text-blue-600 mb-8" />
    <h1 class="text-4xl font-bold text-gray-800 mb-4">Welcome to Virtual Library</h1>
    <p class="text-xl text-gray-600 mb-8 text-center max-w-2xl">
      Explore a vast collection of books, articles, and theses. Read online, rate publications, and save your favorites for later.
    </p>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <FeatureCard
        title="Extensive Collection"
        description="Access a wide range of academic publications from various disciplines."
      />
      <FeatureCard
        title="Online Reading"
        description="Read publications directly in your browser without the need to download."
      />
      <FeatureCard
        title="Personalized Experience"
        description="Rate publications, save favorites, and create your reading list."
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { BookOpen } from 'lucide-vue-next';
import FeatureCard from '../components/FeatureCard.vue';
</script>