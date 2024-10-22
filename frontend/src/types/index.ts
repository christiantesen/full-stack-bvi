export interface User {
  id: string;
  name: string;
  email: string;
  role: 'student' | 'public' | 'teacher' | 'admin';
}

export interface Publication {
  id: string;
  title: string;
  description: string;
  author: string;
  year: number;
  course: string;
  category: string;
  pdfUrl: string;
  recommendedBy: string[];
  rating: number;
}

export interface Rating {
  publicationId: string;
  userId: string;
  value: number;
}

export interface Favorite {
  publicationId: string;
  userId: string;
}

export interface ReadLater {
  publicationId: string;
  userId: string;
}

export interface Report {
  publicationId: string;
  userId: string;
  reason: string;
}