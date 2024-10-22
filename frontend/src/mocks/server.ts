import { createServer, Model, Factory } from 'miragejs';
import { faker } from '@faker-js/faker';

export function makeServer({ environment = 'development' } = {}) {
  return createServer({
    environment,

    models: {
      user: Model,
      publication: Model,
      favorite: Model,
      readLater: Model,
    },

    factories: {
      user: Factory.extend({
        name() { return faker.person.fullName(); },
        email() { return faker.internet.email(); },
        role() { return faker.helpers.arrayElement(['student', 'public', 'teacher', 'admin']); },
      }),
      publication: Factory.extend({
        title() { return faker.lorem.sentence(); },
        description() { return faker.lorem.paragraph(); },
        author() { return faker.person.fullName(); },
        year() { return faker.date.past().getFullYear(); },
        course() { return faker.helpers.arrayElement(['Mathematics', 'Physics', 'Chemistry', 'Biology', 'Computer Science']); },
        category() { return faker.helpers.arrayElement(['Book', 'Article', 'Thesis']); },
        pdfUrl() { return faker.internet.url(); },
        recommendedBy() { return [faker.person.fullName(), faker.person.fullName()]; },
        rating() { return faker.number.int({ min: 1, max: 5 }); },
      }),
    },

    seeds(server) {
      server.createList('user', 10);
      server.createList('publication', 50);
    },

    routes() {
      this.namespace = 'api';

      this.get('/publications', (schema) => {
        return schema.publications.all();
      });

      this.get('/favorites', (schema) => {
        return schema.publications.all().slice(0, 10);
      });

      this.get('/read-later', (schema) => {
        return schema.publications.all().slice(10, 20);
      });

      this.get('/user/profile', () => {
        return {
          id: '1',
          name: 'John Doe',
          email: 'john.doe@example.com',
          role: 'student',
        };
      });
    },
  });
}