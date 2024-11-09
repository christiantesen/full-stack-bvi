<template>
  <div >
    <a class="github-star inline-block text-white font-bold px-4 py-2 rounded outline-none focus:outline-none lg:mr-1 lg:mb-0 ml-3 mb-3 bg-blueGray-700 active:bg-blueGray-600 uppercase text-sm shadow hover:shadow-lg ease-linear transition-all duration-150"
      href="#Hyre" ref="btnDropdownRef" v-on:click="toggleDropdown($event)">
      MENU&ensp;<i class=" fa fa-bars"></i>
    </a>
    <div ref="popoverDropdownRef"
      class="bg-white text-base z-50 float-left py-2 list-none text-left rounded shadow-lg min-w-48" v-bind:class="{
        hidden: !dropdownPopoverShow,
        block: dropdownPopoverShow,
      }">
      <span class="text-sm pt-2 pb-0 px-4 font-bold block w-full whitespace-nowrap bg-transparent text-blueGray-400">
        Contenido
      </span>
      <router-link to="/landing"
        class="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700">
        Catálogo
      </router-link>
      <div class="h-0 mx-4 my-2 border border-solid border-blueGray-100" />
      <span class="text-sm pt-2 pb-0 px-4 font-bold block w-full whitespace-nowrap bg-transparent text-blueGray-400">
        Usuario
      </span>
      <!--<router-link to="/auth/register"
        class="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700">
        Registrarse
      </router-link>-->
      <router-link to="/profile"
        class="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700">
        Perfil
      </router-link>
      <router-link to="/admin/dashboard"
        class="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700">
        Panel
      </router-link>
      <div class="h-0 mx-4 my-2 border border-solid border-blueGray-100" />
      <!-- INICIAR SESIÓN -->
      <li class="flex items-center">
        <button @click="redirectToLogin"
          class="bg-emerald-500 text-white active:bg-emerald-600 text-xs font-bold uppercase px-4 py-2 rounded shadow hover:shadow-lg outline-none focus:outline-none lg:mr-1 lg:mb-0 ml-3 mb-3 ease-linear transition-all duration-150"
          type="button">
          <i class="fas fa-right-to-bracket"></i> Iniciar Sesión
        </button>
      </li>
      <div class="h-0 mx-4 my-2 border border-solid border-blueGray-100" />
      <!-- REGISTRARSE -->
      <li class="flex items-center">
        <button @click="redirectToRegister"
          class="bg-emerald-500 text-white active:bg-emerald-600 text-xs font-bold uppercase px-4 py-2 rounded shadow hover:shadow-lg outline-none focus:outline-none lg:mr-1 lg:mb-0 ml-3 mb-3 ease-linear transition-all duration-150"
          type="button">
          <i class="fas fa-right-to-bracket"></i> Registrarse
        </button>
      </li>
    </div>
  </div>
</template>
<script>
import { createPopper } from "@popperjs/core";
import { useRouter } from "vue-router";
import { ref } from "vue";

export default {
  setup() {
    const dropdownPopoverShow = ref(false);
    const router = useRouter(); // Usamos useRouter dentro de setup
    const toggleDropdown = (event) => {
      event.preventDefault();
      if (this.dropdownPopoverShow) {
        this.dropdownPopoverShow = false;
      } else {
        this.dropdownPopoverShow = true;
        createPopper(this.$refs.btnDropdownRef, this.$refs.popoverDropdownRef, {
          placement: "bottom-start",
        });
      }
    };
    // Método para redirigir al login
    const redirectToLogin = () => {
      console.log("Redirecting to login");
      router.push("/auth/login"); // Usamos router.push directamente
    };
    // Método para redirigir al register
    const redirectToRegister = () => {
      console.log("Redirecting to register");
      router.push("/auth/register"); // Usamos router.push directamente
    };
    return {
      dropdownPopoverShow: false
    };
  }
};
</script>
