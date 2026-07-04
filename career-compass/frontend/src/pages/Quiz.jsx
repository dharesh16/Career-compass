import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getQuestions, submitQuiz } from '../api.js'

export default function Quiz() {
  const [questions, setQuestions] = useState([])
  const [step, setStep] = useState(-1) // -1 = intro form, 0..n-1 = questions
  const [studentName, setStudentName] = useState('')
  const [studentClass, setStudentClass] = useState('')
  const [answers, setAnswers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    getQuestions()
      .then(setQuestions)
      .catch(() => setError('Could not reach the backend. Is it running on port 8000?'))
      .finally(() => setLoading(false))
  }, [])

  const handleStart = (e) => {
    e.preventDefault()
    if (!studentName.trim()) return
    setStep(0)
  }

  const handleAnswer = async (category) => {
    const question = questions[step]
    const newAnswers = [...answers, { question_id: question.id, category }]
    setAnswers(newAnswers)

    if (step + 1 < questions.length) {
      setStep(step + 1)
    } else {
      // last question answered -> submit
      try {
        const result = await submitQuiz({
          student_name: studentName,
          student_class: studentClass,
          answers: newAnswers,
        })
        navigate('/result', { state: result })
      } catch (err) {
        setError('Could not submit quiz. Please try again.')
      }
    }
  }

  if (loading) return <div className="card">Loading quiz…</div>
  if (error) return <div className="card error">{error}</div>

  // Intro form to collect name before starting
  if (step === -1) {
    return (
      <div className="card">
        <h2>Before we start…</h2>
        <form onSubmit={handleStart} className="form">
          <label>
            Your Name
            <input
              value={studentName}
              onChange={(e) => setStudentName(e.target.value)}
              placeholder="e.g. Dharesh"
              required
            />
          </label>
          <label>
            Class / Grade (optional)
            <input
              value={studentClass}
              onChange={(e) => setStudentClass(e.target.value)}
              placeholder="e.g. 11th Grade"
            />
          </label>
          <button className="btn" type="submit">Begin Quiz</button>
        </form>
      </div>
    )
  }

  const question = questions[step]

  return (
    <div className="card">
      <div className="progress">
        Question {step + 1} of {questions.length}
      </div>
      <h2>{question.text}</h2>
      <div className="options">
        {question.options.map((opt, i) => (
          <button
            key={i}
            className="option-btn"
            onClick={() => handleAnswer(opt.category)}
          >
            {opt.label}
          </button>
        ))}
      </div>
    </div>
  )
}
