import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Publications from './pages/Publications';
import Favorites from './pages/Favorites';
import ReadLater from './pages/ReadLater';
import Profile from './pages/Profile';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="publications" element={<Publications />} />
          <Route path="favorites" element={<Favorites />} />
          <Route path="read-later" element={<ReadLater />} />
          <Route path="profile" element={<Profile />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;