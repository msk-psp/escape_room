import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import SearchPage from './SearchPage';
import MainPage from './MainPage';
import "./index.css";

export function App() {
  return (
    <Router>
      <div className="max-w-7xl mx-auto p-8">
        <nav className="mb-8">
          <ul className="flex justify-center gap-8">
            <li><Link to="/" className="text-lg hover:underline">Home</Link></li>
            <li><Link to="/search" className="text-lg hover:underline">Search</Link></li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/search" element={<SearchPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
