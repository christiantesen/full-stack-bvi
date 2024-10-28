import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
// Removing i18n import as it's not configured yet
import './assets/styles/main.scss';

const app = createApp(App);

app.use(createPinia())
   .use(router)
   // Removing i18n.use() as it's not configured
   .mount('#app');