<template>
  <nav
    class="top-0 absolute z-50 w-full flex flex-wrap items-center justify-between px-2 py-3 navbar-expand-lg"
  >
    <div
      class="container px-4 mx-auto flex flex-wrap items-center justify-between"
    >
      <div
        class="w-full relative flex justify-between lg:w-auto lg:static lg:block lg:justify-start"
      >
        <router-link
          class="text-white text-sm font-bold leading-relaxed inline-block mr-4 py-2 whitespace-nowrap uppercase"
          to="/"
        >
          <a href="https://www.urp.edu.pe/pregrado/facultad-de-ingenieria/bvi/">
            <i class="fas fa-house text-lg leading-lg mr-2" />
            BVI
          </a>
          Estantería Virtual
        </router-link>
        <button
          class="cursor-pointer text-xl leading-none px-3 py-1 border border-solid border-transparent rounded bg-transparent block lg:hidden outline-none focus:outline-none"
          type="button"
          v-on:click="setNavbarOpen"
        >
          <i class="text-white fas fa-bars"></i>
        </button>
      </div>
      <div
        class="lg:flex flex-grow items-center bg-white lg:bg-opacity-0 lg:shadow-none"
        :class="[navbarOpen ? 'block rounded shadow-lg' : 'hidden']"
        id="example-navbar-warning"
      >
        <!-- ITEMS -->
        <ul class="flex flex-col lg:flex-row list-none lg:ml-auto">
          <!-- MENU -->
          <li class="flex items-center">
            <PagesDropdown />
          </li>

          <li class="flex items-center">
            <button
              @click="redirectToLogin"
              class="bg-white text-blueGray-700 active:bg-blueGray-50 text-xs font-bold uppercase px-4 py-2 rounded shadow hover:shadow-md outline-none focus:outline-none lg:mr-1 lg:mb-0 ml-3 mb-3 ease-linear transition-all duration-150"
              type="button"
            >
              <i class="fas fa-right-to-bracket"></i> Iniciar Sesión
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import PagesDropdown from "@/components/Dropdowns/PagesDropdown.vue";

export default {
  components: {
    PagesDropdown,
  },
  setup() {
    const router = useRouter(); // Usamos useRouter dentro de setup
    const navbarOpen = ref(false); // Usamos `ref` para manejar estado reactivo

    // Método para alternar la visibilidad del navbar
    const setNavbarOpen = () => {
      navbarOpen.value = !navbarOpen.value;
    };

    // Método para redirigir al login
    const redirectToLogin = () => {
      console.log('Redirecting to login');
      router.push('/auth/login'); // Usamos router.push directamente
    };

    // Retornamos las propiedades y métodos para usarlos en la plantilla
    return {
      navbarOpen,
      setNavbarOpen,
      redirectToLogin,
    };
  },
};
</script>