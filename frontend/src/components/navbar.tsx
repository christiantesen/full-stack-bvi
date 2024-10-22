import React from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, User } from 'lucide-react';

const Navbar: React.FC = () => {
  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-2">
            <BookOpen className="h-8 w-8" />
            <span className="text-xl font-bold">Virtual Library</span>
          </Link>
          <div className="flex items-center space-x-4">
            <Link to="/publications" className="hover:text-blue-200">Publications</Link>
            <Link to="/favorites" className="hover:text-blue-200">Favorites</Link>
            <Link to="/read-later" className="hover:text-blue-200">Read Later</Link>
            <Link to="/profile" className="flex items-center space-x-1 hover:text-blue-200">
              <User className="h-5 w-5" />
              <span>Profile</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;