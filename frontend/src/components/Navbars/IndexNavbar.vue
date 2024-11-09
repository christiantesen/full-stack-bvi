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
        <!-- INICIO BUSCADOR -->
        <div class="flex flex-col lg:flex-row list-none lg:ml-auto">
          <span
            class="z-10 h-full leading-snug font-normal absolute text-center text-blueGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-2"
          >
            <i class="fas fa-search"></i>
          </span>
          <input
            type="text"
            placeholder="Buscar..."
            class="px-3 py-2 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full pl-10"
          />
        </div>
        <!-- FIN BUSCADOR -->
        <!-- ITEMS -->
        <ul class="flex flex-col lg:flex-row list-none lg:ml-auto">
          <!-- MENU -->
          <li class="flex items-center">
            <index-dropdown />
          </li>
          <!-- INICIAR SESIÓN --
          <li class="flex items-center">
            <button
              @click="redirectToLogin"
              class="bg-emerald-500 text-white active:bg-emerald-600 text-xs font-bold uppercase px-4 py-2 rounded shadow hover:shadow-lg outline-none focus:outline-none lg:mr-1 lg:mb-0 ml-3 mb-3 ease-linear transition-all duration-150"
              type="button"
            >
              <i class="fas fa-right-to-bracket"></i> Iniciar Sesión
            </button>
          </li>-->
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import IndexDropdown from "@/components/Dropdowns/IndexDropdown.vue";

export default {
  components: {
    IndexDropdown,
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
      console.log("Redirecting to login");
      router.push("/auth/login"); // Usamos router.push directamente
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
