import React from 'react';
import { BookOpen } from 'lucide-react';

const Home: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <BookOpen className="h-24 w-24 text-blue-600 mb-8" />
      <h1 className="text-4xl font-bold text-gray-800 mb-4">Welcome to Virtual Library</h1>
      <p className="text-xl text-gray-600 mb-8 text-center max-w-2xl">
        Explore a vast collection of books, articles, and theses. Read online, rate publications, and save your favorites for later.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <FeatureCard
          title="Extensive Collection"
          description="Access a wide range of academic publications from various disciplines."
        />
        <FeatureCard
          title="Online Reading"
          description="Read publications directly in your browser without the need to download."
        />
        <FeatureCard
          title="Personalized Experience"
          description="Rate publications, save favorites, and create your reading list."
        />
      </div>
    </div>
  );
};

const FeatureCard: React.FC<{ title: string; description: string }> = ({ title, description }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-semibold text-gray-800 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
};

export default Home;