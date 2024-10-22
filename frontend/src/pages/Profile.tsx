import React, { useState, useEffect } from 'react';
import { User } from '../types';

const Profile: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/user/profile');
      if (!response.ok) {
        throw new Error('Failed to fetch user profile');
      }
      const data = await response.json();
      setUser(data);
      setLoading(false);
    } catch (err) {
      setError('An error occurred while fetching your profile. Please try again later.');
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center">Loading profile...</div>;
  }

  if (error) {
    return <div className="text-center text-red-600">{error}</div>;
  }

  if (!user) {
    return <div className="text-center">No user data available.</div>;
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold mb-8">User Profile</h2>
      <div className="bg-white shadow-md rounded-lg p-6">
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">Name</label>
          <p className="text-gray-900">{user.name}</p>
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">Email</label>
          <p className="text-gray-900">{user.email}</p>
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">Role</label>
          <p className="text-gray-900 capitalize">{user.role}</p>
        </div>
        {(user.role === 'teacher' || user.role === 'admin') && (
          <div className="mt-6">
            <h3 className="text-xl font-semibold mb-4">Management Options</h3>
            {user.role === 'admin' && (
              <button className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition duration-300 mr-4">
                Manage Users
              </button>
            )}
            <button className="bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700 transition duration-300">
              Manage Publications
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;