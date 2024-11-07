<template>
  <footer class="relative bg-blueGray-200 pt-8 pb-6">
    <div
      class="bottom-auto top-0 left-0 right-0 w-full absolute pointer-events-none overflow-hidden -mt-20 h-20"
      style="transform: translateZ(0)"
    >
      <svg
        class="absolute bottom-0 overflow-hidden"
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="none"
        version="1.1"
        viewBox="0 0 2560 100"
        x="0"
        y="0"
      >
        <polygon
          class="text-blueGray-200 fill-current"
          points="2560 0 2560 100 0 100"
        ></polygon>
      </svg>
    </div>
    <div class="container mx-auto px-4">
      <div class="flex flex-wrap text-center lg:text-left">
        <div class="w-full lg:w-6/12 px-4">
          <h4 class="text-3xl font-semibold">Sigamos en contacto!</h4>
          <h5 class="text-lg mt-0 mb-2 text-blueGray-600">
            Encuéntranos en cualquiera de estas plataformas, respondemos 1-2
            días hábiles.
          </h5>
          <div class="mt-6 lg:mb-0 mb-6">
            <button
              onclick="window.open('https://x.com/bviurp', '_blank')"
              class="bg-white text-lightBlue-400 shadow-lg font-normal h-10 w-10 items-center justify-center align-center rounded-full outline-none focus:outline-none mr-2"
              type="button"
            >
              <i class="fab fa-twitter"></i>
            </button>
            <button
              onclick="window.open('https://www.facebook.com/bibliotecavirtualing/', '_blank')"
              class="bg-white text-lightBlue-600 shadow-lg font-normal h-10 w-10 items-center justify-center align-center rounded-full outline-none focus:outline-none mr-2"
              type="button"
            >
              <i class="fab fa-facebook-square"></i>
            </button>
            <button
              onclick="window.open('https://www.youtube.com/@bviurp', '_blank')"
              class="bg-white text-pink-400 shadow-lg font-normal h-10 w-10 items-center justify-center align-center rounded-full outline-none focus:outline-none mr-2"
              type="button"
            >
              <i class="fab fa-youtube"></i>
            </button>
            <button
              onclick="window.open('https://api.whatsapp.com/send?phone=51968078224&text=Hola!%20Tengo%20una%20Consulta!%20%F0%9F%99%8B', '_blank')"
              class="bg-white text-blueGray-800 shadow-lg font-normal h-10 w-10 items-center justify-center align-center rounded-full outline-none focus:outline-none mr-2"
              type="button"
            >
              <i class="fab fa-whatsapp"></i>
            </button>
            <button
              onclick="window.open('https://www.linkedin.com/in/biblioteca-virtual-de-ingenier%C3%ADa-urp-06a414213/', '_blank')"
              class="bg-white text-blueGray-800 shadow-lg font-normal h-10 w-10 items-center justify-center align-center rounded-full outline-none focus:outline-none mr-2"
              type="button"
            >
              <i class="fab fa-linkedin"></i>
            </button>
          </div>
        </div>
        <div class="w-full lg:w-6/12 px-4">
          <div class="flex flex-wrap items-top mb-6">
            <div class="w-full lg:w-4/12 px-4 ml-auto">
              <span
                class="block uppercase text-blueGray-500 text-sm font-semibold mb-2"
              >
                Links
              </span>
              <ul class="list-unstyled">
                <li>
                  <a
                    class="text-blueGray-600 hover:text-blueGray-800 font-semibold block pb-2 text-sm"
                    href="https://www.urp.edu.pe/pregrado/facultad-de-ingenieria/bvi/nosotros/"
                    target="_blank"
                  >
                    Sobre Nosotros
                  </a>
                </li>
                <li>
                  <a
                    class="text-blueGray-600 hover:text-blueGray-800 font-semibold block pb-2 text-sm"
                    href="https://www.urp.edu.pe/pregrado/facultad-de-ingenieria/bvi/boletines-virtuales/"
                    target="_blank"
                  >
                    Boletines Virtuales
                  </a>
                </li>
                <li>
                  <a
                    class="text-blueGray-600 hover:text-blueGray-800 font-semibold block pb-2 text-sm"
                    href="https://test.urp.edu.pe/Intranet/"
                    target="_blank"
                  >
                    Aula Virtual
                  </a>
                </li>
              </ul>
            </div>
            <div class="w-full lg:w-4/12 px-4">
              <span
                class="block uppercase text-blueGray-500 text-sm font-semibold mb-2"
              >
                Otros Recursos
              </span>
              <ul class="list-unstyled">
                <li>
                  <a
                    class="text-blueGray-600 hover:text-blueGray-800 font-semibold block pb-2 text-sm"
                    href="https://www.urp.edu.pe/bvi"
                    target="_blank"
                  >
                    BVI
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <hr class="my-6 border-blueGray-300" />
      <div
        class="flex flex-wrap items-center md:justify-between justify-center"
      >
        <div class="w-full md:w-4/12 px-4 mx-auto text-center">
          <div class="text-sm text-blueGray-500 font-semibold py-1">
            <a
              href="https://www.urp.edu.pe/"
              target="_blank"
              class="text-blueGray-500 hover:text-blueGray-800"
            >
              Universidad Ricardo Palma
            </a>
          </div>
          <div class="text-sm text-blueGray-500 font-semibold py-1">
            Copyright © {{ date }} | Todos los derechos reservados.
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>
<script>
export default {
  data() {
    return {
      date: new Date().getFullYear(),
    };
  },
};
</script>
