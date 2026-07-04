import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="card home-card">
      <h1>Find Direction for Your Future</h1>
      <p>
        Career Compass is a simple guidance tool that helps school students
        discover career paths that match their interests through a short quiz.
      </p>
      <Link to="/quiz" className="btn">Start the Quiz →</Link>

      <div className="feature-grid">
        <div className="feature">
          <h3>🎯 Quick Quiz</h3>
          <p>Just 8 simple questions about your interests.</p>
        </div>
        <div className="feature">
          <h3>💡 Instant Guidance</h3>
          <p>Get a personalised career category with suggested paths.</p>
        </div>
        <div className="feature">
          <h3>📊 For Counsellors</h3>
          <p>Track all student results from one dashboard.</p>
        </div>
      </div>
    </div>
  )
}
