<template>
  <nav
    class="top-0 fixed z-50 w-full flex flex-wrap items-center justify-between px-2 py-3 navbar-expand-lg bg-white shadow"
  >
    <div
      class="container px-4 mx-auto flex flex-wrap items-center justify-between"
    >
      <div
        class="w-full relative flex justify-between lg:w-auto lg:static lg:block lg:justify-start"
      >
        <router-link to="/">
          <li class="flex items-center">
            <a
              class="hover:text-blueGray-500 text-blueGray-700 px-3 py-2 flex items-center text-xs uppercase font-bold"
              href="https://www.urp.edu.pe/pregrado/facultad-de-ingenieria/bvi/"
            >
              <i
                class="text-blueGray-400 fas fa-house text-lg leading-lg mr-2"
              />
              BVI
            </a>
            <a
              class="text-blueGray-700 text-sm font-bold leading-relaxed inline-block mr-4 py-2 whitespace-nowrap uppercase"
              href="#Hyre"
            >
              Estantería Virtual
            </a>
          </li>
        </router-link>
        <button
          class="cursor-pointer text-xl leading-none px-3 py-1 border border-solid border-transparent rounded bg-transparent block lg:hidden outline-none focus:outline-none"
          type="button"
          v-on:click="setNavbarOpen"
        >
          <i class="fas fa-bars"></i>
        </button>
      </div>
      <div
        class="lg:flex flex-grow items-center"
        :class="[navbarOpen ? 'block' : 'hidden']"
        id="example-navbar-warning"
      >
        <!-- BUSCADOR -->
        <div class="lg:flex flex-grow items-center">
          <div
            class="relative flex w-full sm:w-7/12 md:w-5/12 px-4 flex-wrap items-stretch lg:ml-auto"
          >
            <input
              type="text"
              class="px-2 py-1 h-8 border border-solid border-emerald-600 rounded-full text-sm leading-snug text-emerald-700 bg-emerald-100 shadow-none outline-none focus:outline-none w-full font-normal rounded-l-none flex-1 border-l-0 placeholder-emerald-300"
              placeholder="🔍 Buscar..."
            />
          </div>
        </div>
        <!-- ITEMS -->
        <ul class="flex flex-col lg:flex-row list-none lg:ml-auto">
          <!-- MENU -->
          <li class="flex items-center">
            <index-dropdown />
          </li>
          <!-- INICIAR SESIÓN -->
          <li class="flex items-center">
            <button
              @click="redirectToLogin"
              class="bg-emerald-500 text-white active:bg-emerald-600 text-xs font-bold uppercase px-4 py-2 rounded shadow hover:shadow-lg outline-none focus:outline-none lg:mr-1 lg:mb-0 ml-3 mb-3 ease-linear transition-all duration-150"
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
import IndexDropdown from "@/components/Dropdowns/IndexDropdown.vue";
import { useRouter } from 'vue-router';

const router = useRouter();

export default {
  data() {
    return {
      navbarOpen: false,
    };
  },
  methods: {
    setNavbarOpen: function () {
      this.navbarOpen = !this.navbarOpen;
    },
    redirectToLogin: function () {
      // Validate if the user is already logged in
      router.push('/auth/login');
    },
  },
  components: {
    IndexDropdown,
  },
};
</script>
