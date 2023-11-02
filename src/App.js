import Home from './pages/home/Home';
import Results from './pages/results/Results';
import { Routes, Route } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <div className="container">

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/results" element={<Results />} />
        </Routes>

    </div>
  );
}

export default App;
