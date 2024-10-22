<template>
  <div>
    <h2 class="text-3xl font-bold mb-8">Favorites</h2>
    <div v-if="loading" class="text-center">Loading favorites...</div>
    <div v-else-if="error" class="text-center text-red-600">{{ error }}</div>
    <div v-else-if="favorites.length === 0" class="text-center text-gray-600">
      You haven't added any publications to your favorites yet.
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <PublicationCard
        v-for="publication in favorites"
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

const favorites = ref<Publication[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

const fetchFavorites = async () => {
  try {
    const response = await fetch('/api/favorites');
    if (!response.ok) {
      throw new Error('Failed to fetch favorites');
    }
    const data = await response.json();
    favorites.value = data.publications;
    loading.value = false;
  } catch (err) {
    error.value = 'An error occurred while fetching favorites. Please try again later.';
    loading.value = false;
  }
};

const handleRate = async (id: string, rating: number) => {
  console.log(`Rating publication ${id} with ${rating} stars`);
};

const handleFavorite = async (id: string) => {
  console.log(`Removing publication ${id} from favorites`);
  favorites.value = favorites.value.filter(fav => fav.id !== id);
};

const handleReadLater = async (id: string) => {
  console.log(`Toggling read later for publication ${id}`);
};

const handleReport = async (id: string) => {
  console.log(`Reporting broken link for publication ${id}`);
};

onMounted(fetchFavorites);
</script>