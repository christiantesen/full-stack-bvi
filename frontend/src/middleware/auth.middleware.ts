import { NavigationGuardNext, RouteLocationNormalized } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

export async function authMiddleware(
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
) {
  const authStore = useAuthStore();
  const publicRoutes = ['/auth/login', '/auth/register'];

  if (!authStore.isAuthenticated && !publicRoutes.includes(to.path)) {
    next('/auth/login');
  } else if (authStore.isAuthenticated && publicRoutes.includes(to.path)) {
    next('/');
  } else {
    next();
  }
}