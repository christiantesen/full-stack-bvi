import React from 'react';
import { Star, Heart, Clock, Flag } from 'lucide-react';
import { Publication } from '../types';

interface PublicationCardProps {
  publication: Publication;
  onRate: (id: string, rating: number) => void;
  onFavorite: (id: string) => void;
  onReadLater: (id: string) => void;
  onReport: (id: string) => void;
}

const PublicationCard: React.FC<PublicationCardProps> = ({
  publication,
  onRate,
  onFavorite,
  onReadLater,
  onReport,
}) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 flex flex-col space-y-4">
      <h3 className="text-xl font-semibold">{publication.title}</h3>
      <p className="text-gray-600">{publication.description}</p>
      <div className="flex justify-between text-sm text-gray-500">
        <span>Author: {publication.author}</span>
        <span>Year: {publication.year}</span>
      </div>
      <div className="flex justify-between text-sm text-gray-500">
        <span>Course: {publication.course}</span>
        <span>Category: {publication.category}</span>
      </div>
      <div className="flex items-center space-x-2">
        <span className="text-sm text-gray-500">Recommended by:</span>
        <div className="flex space-x-1">
          {publication.recommendedBy.map((teacher, index) => (
            <span key={index} className="bg-blue-100 text-blue-800 text-xs font-semibold px-2 py-1 rounded">
              {teacher}
            </span>
          ))}
        </div>
      </div>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-1">
          {[1, 2, 3, 4, 5].map((star) => (
            <Star
              key={star}
              className={`h-5 w-5 cursor-pointer ${
                star <= publication.rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
              }`}
              onClick={() => onRate(publication.id, star)}
            />
          ))}
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => onFavorite(publication.id)}
            className="p-2 rounded-full hover:bg-red-100"
            title="Add to favorites"
          >
            <Heart className="h-5 w-5 text-red-500" />
          </button>
          <button
            onClick={() => onReadLater(publication.id)}
            className="p-2 rounded-full hover:bg-blue-100"
            title="Read later"
          >
            <Clock className="h-5 w-5 text-blue-500" />
          </button>
          <button
            onClick={() => onReport(publication.id)}
            className="p-2 rounded-full hover:bg-yellow-100"
            title="Report broken link"
          >
            <Flag className="h-5 w-5 text-yellow-500" />
          </button>
        </div>
      </div>
      <a
        href={publication.pdfUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition duration-300 text-center"
      >
        View PDF
      </a>
    </div>
  );
};

export default PublicationCard;