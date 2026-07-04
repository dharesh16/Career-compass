const BASE_URL = "http://127.0.0.1:8000";

export async function getQuestions() {
  const res = await fetch(`${BASE_URL}/api/questions`);
  if (!res.ok) throw new Error("Failed to load questions");
  return res.json();
}

export async function submitQuiz(payload) {
  const res = await fetch(`${BASE_URL}/api/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to submit quiz");
  return res.json();
}

export async function getDashboard() {
  const res = await fetch(`${BASE_URL}/api/dashboard`);
  if (!res.ok) throw new Error("Failed to load dashboard");
  return res.json();
}
