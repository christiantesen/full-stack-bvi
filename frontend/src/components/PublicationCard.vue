<template>
  <div class="bg-white rounded-lg shadow-md p-6 flex flex-col space-y-4">
    <h3 class="text-xl font-semibold">{{ publication.title }}</h3>
    <p class="text-gray-600">{{ publication.description }}</p>
    <div class="flex justify-between text-sm text-gray-500">
      <span>Author: {{ publication.author }}</span>
      <span>Year: {{ publication.year }}</span>
    </div>
    <div class="flex justify-between text-sm text-gray-500">
      <span>Course: {{ publication.course }}</span>
      <span>Category: {{ publication.category }}</span>
    </div>
    <div class="flex items-center space-x-2">
      <span class="text-sm text-gray-500">Recommended by:</span>
      <div class="flex space-x-1">
        <span
          v-for="(teacher, index) in publication.recommendedBy"
          :key="index"
          class="bg-blue-100 text-blue-800 text-xs font-semibold px-2 py-1 rounded"
        >
          {{ teacher }}
        </span>
      </div>
    </div>
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-1">
        <Star
          v-for="star in 5"
          :key="star"
          :class="[
            'h-5 w-5 cursor-pointer',
            star <= publication.rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
          ]"
          @click="onRate(publication.id, star)"
        />
      </div>
      <div class="flex space-x-2">
        <button
          @click="onFavorite(publication.id)"
          class="p-2 rounded-full hover:bg-red-100"
          title="Add to favorites"
        >
          <Heart class="h-5 w-5 text-red-500" />
        </button>
        <button
          @click="onReadLater(publication.id)"
          class="p-2 rounded-full hover:bg-blue-100"
          title="Read later"
        >
          <Clock class="h-5 w-5 text-blue-500" />
        </button>
        <button
          @click="onReport(publication.id)"
          class="p-2 rounded-full hover:bg-yellow-100"
          title="Report broken link"
        >
          <Flag class="h-5 w-5 text-yellow-500" />
        </button>
      </div>
    </div>
    <a
      :href="publication.pdfUrl"
      target="_blank"
      rel="noopener noreferrer"
      class="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition duration-300 text-center"
    >
      View PDF
    </a>
  </div>
</template>

<script lang="ts" setup>
import { Star, Heart, Clock, Flag } from 'lucide-vue-next';
import { Publication } from '../types';

interface Props {
  publication: Publication;
  onRate: (id: string, rating: number) => void;
  onFavorite: (id: string) => void;
  onReadLater: (id: string) => void;
  onReport: (id: string) => void;
}

defineProps<Props>();
</script>