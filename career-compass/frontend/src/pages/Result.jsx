import { useLocation, Link } from 'react-router-dom'

export default function Result() {
  const location = useLocation()
  const result = location.state

  if (!result) {
    return (
      <div className="card">
        <p>No result found. Please take the quiz first.</p>
        <Link to="/quiz" className="btn">Take Quiz</Link>
      </div>
    )
  }

  const { info, scores } = result

  return (
    <div className="card">
      <h2>Your Recommended Path</h2>
      <h1 className="result-title">{info.title}</h1>
      <p>{info.description}</p>

      <h3>Suggested Careers</h3>
      <ul className="pill-list">
        {info.careers.map((c, i) => (
          <li key={i} className="pill">{c}</li>
        ))}
      </ul>

      <h3>Next Steps</h3>
      <ul>
        {info.next_steps.map((step, i) => (
          <li key={i}>{step}</li>
        ))}
      </ul>

      <h3>Your Interest Breakdown</h3>
      <div className="score-bars">
        {Object.entries(scores).map(([cat, score]) => (
          <div key={cat} className="score-row">
            <span className="score-label">{cat}</span>
            <div className="score-bar-track">
              <div
                className="score-bar-fill"
                style={{ width: `${(score / 8) * 100}%` }}
              />
            </div>
            <span>{score}</span>
          </div>
        ))}
      </div>

      <Link to="/quiz" className="btn secondary">Retake Quiz</Link>
    </div>
  )
}
