import { ref } from 'vue';
import apiClient from '@/services/api';
import type { ApiResponse } from '@/types';

export function useApi<T>() {
  const data = ref<T | null>(null);
  const error = ref<Error | null>(null);
  const loading = ref(false);

  async function execute(url: string, options = {}) {
    loading.value = true;
    try {
      const response = await apiClient(url, options);
      data.value = response.data;
    } catch (e) {
      error.value = e as Error;
    } finally {
      loading.value = false;
    }
  }

  return {
    data,
    error,
    loading,
    execute
  };
}