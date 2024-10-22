import React, { useState, useEffect } from 'react';
import PublicationCard from '../components/PublicationCard';
import { Publication } from '../types';

const Favorites: React.FC = () => {
  const [favorites, setFavorites] = useState<Publication[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchFavorites();
  }, []);

  const fetchFavorites = async () => {
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/favorites');
      if (!response.ok) {
        throw new Error('Failed to fetch favorites');
      }
      const data = await response.json();
      setFavorites(data);
      setLoading(false);
    } catch (err) {
      setError('An error occurred while fetching favorites. Please try again later.');
      setLoading(false);
    }
  };

  const handleRate = async (id: string, rating: number) => {
    // TODO: Implement API call to rate publication
    console.log(`Rating publication ${id} with ${rating} stars`);
  };

  const handleFavorite = async (id: string) => {
    // TODO: Implement API call to remove from favorites
    console.log(`Removing publication ${id} from favorites`);
    setFavorites(favorites.filter(fav => fav.id !== id));
  };

  const handleReadLater = async (id: string) => {
    // TODO: Implement API call to add/remove from read later list
    console.log(`Toggling read later for publication ${id}`);
  };

  const handleReport = async (id: string) => {
    // TODO: Implement API call to report broken link
    console.log(`Reporting broken link for publication ${id}`);
  };

  if (loading) {
    return <div className="text-center">Loading favorites...</div>;
  }

  if (error) {
    return <div className="text-center text-red-600">{error}</div>;
  }

  return (
    <div>
      <h2 className="text-3xl font-bold mb-8">Favorites</h2>
      {favorites.length === 0 ? (
        <p className="text-center text-gray-600">You haven't added any publications to your favorites yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {favorites.map((publication) => (
            <PublicationCard
              key={publication.id}
              publication={publication}
              onRate={handleRate}
              onFavorite={handleFavorite}
              onReadLater={handleReadLater}
              onReport={handleReport}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Favorites;