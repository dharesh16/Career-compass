import { Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home.jsx'
import Quiz from './pages/Quiz.jsx'
import Result from './pages/Result.jsx'
import Dashboard from './pages/Dashboard.jsx'

export default function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <Link to="/" className="brand">🧭 Career Compass</Link>
        <div className="nav-links">
          <Link to="/">Home</Link>
          <Link to="/quiz">Take Quiz</Link>
          <Link to="/dashboard">Counsellor Dashboard</Link>
        </div>
      </nav>

      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/quiz" element={<Quiz />} />
          <Route path="/result" element={<Result />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </main>
    </div>
  )
}
