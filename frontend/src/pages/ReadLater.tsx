import React, { useState, useEffect } from 'react';
import PublicationCard from '../components/PublicationCard';
import { Publication } from '../types';

const ReadLater: React.FC = () => {
  const [readLaterList, setReadLaterList] = useState<Publication[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchReadLaterList();
  }, []);

  const fetchReadLaterList = async () => {
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/read-later');
      if (!response.ok) {
        throw new Error('Failed to fetch read later list');
      }
      const data = await response.json();
      setReadLaterList(data);
      setLoading(false);
    } catch (err) {
      setError('An error occurred while fetching your read later list. Please try again later.');
      setLoading(false);
    }
  };

  const handleRate = async (id: string, rating: number) => {
    // TODO: Implement API call to rate publication
    console.log(`Rating publication ${id} with ${rating} stars`);
  };

  const handleFavorite = async (id: string) => {
    // TODO: Implement API call to add/remove from favorites
    console.log(`Toggling favorite for publication ${id}`);
  };

  const handleReadLater = async (id: string) => {
    // TODO: Implement API call to remove from read later list
    console.log(`Removing publication ${id} from read later list`);
    setReadLaterList(readLaterList.filter(item => item.id !== id));
  };

  const handleReport = async (id: string) => {
    // TODO: Implement API call to report broken link
    console.log(`Reporting broken link for publication ${id}`);
  };

  if (loading) {
    return <div className="text-center">Loading read later list...</div>;
  }

  if (error) {
    return <div className="text-center text-red-600">{error}</div>;
  }

  return (
    <div>
      <h2 className="text-3xl font-bold mb-8">Read Later</h2>
      {readLaterList.length === 0 ? (
        <p className="text-center text-gray-600">You haven't added any publications to your read later list yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {readLaterList.map((publication) => (
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

export default ReadLater;