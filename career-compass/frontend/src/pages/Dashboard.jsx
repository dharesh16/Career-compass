import { useEffect, useState } from 'react'
import { getDashboard } from '../api.js'

export default function Dashboard() {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    getDashboard()
      .then(setRecords)
      .catch(() => setError('Could not load dashboard. Is the backend running?'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="card">Loading…</div>
  if (error) return <div className="card error">{error}</div>

  return (
    <div className="card">
      <h2>Counsellor Dashboard</h2>
      <p>All student quiz results, most recent first.</p>

      {records.length === 0 ? (
        <p>No submissions yet.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>#</th>
              <th>Name</th>
              <th>Class</th>
              <th>Recommended Category</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {records.map((r) => (
              <tr key={r.id}>
                <td>{r.id}</td>
                <td>{r.student_name}</td>
                <td>{r.student_class || '-'}</td>
                <td><span className="tag">{r.category}</span></td>
                <td>{r.created_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
