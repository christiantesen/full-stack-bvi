<template>
  <div>
    <h2 class="text-3xl font-bold mb-8">Publications</h2>
    <div v-if="loading" class="text-center">Loading publications...</div>
    <div v-else-if="error" class="text-center text-red-600">{{ error }}</div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <PublicationCard
        v-for="publication in publications"
        :key="publication.id"
        :publication="publication"
        :onRate="handleRate"
        :onFavorite="handleFavorite"
        :onReadLater="handleReadLater"
        :onReport="handleReport"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import PublicationCard from '../components/PublicationCard.vue';
import { Publication } from '../types';

const publications = ref<Publication[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

const fetchPublications = async () => {
  try {
    const response = await fetch('/api/publications');
    if (!response.ok) {
      throw new Error('Failed to fetch publications');
    }
    const data = await response.json();
    publications.value = data.publications;
    loading.value = false;
  } catch (err) {
    error.value = 'An error occurred while fetching publications. Please try again later.';
    loading.value = false;
  }
};

const handleRate = async (id: string, rating: number) => {
  console.log(`Rating publication ${id} with ${rating} stars`);
};

const handleFavorite = async (id: string) => {
  console.log(`Toggling favorite for publication ${id}`);
};

const handleReadLater = async (id: string) => {
  console.log(`Toggling read later for publication ${id}`);
};

const handleReport = async (id: string) => {
  console.log(`Reporting broken link for publication ${id}`);
};

onMounted(fetchPublications);
</script>