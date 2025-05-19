import { useState } from 'react'

function App() {
  const [morningDone, setMorningDone] = useState(true)
  const [coachDone, setCoachDone] = useState(false)
  const [habitsDone, setHabitsDone] = useState(3)
  const totalHabits = 5

  return (
    <div className="min-h-screen bg-gray-100 text-gray-800 p-4">
      <div className="max-w-md mx-auto">
        <h1 className="text-2xl font-bold mb-2">💡 Мой день</h1>
        <p className="text-sm text-gray-600 mb-6">
          Прогресс за сегодня
        </p>

        <div className="bg-white shadow rounded-2xl p-4 mb-6">
          <ul className="space-y-2 text-base">
            <li>☀️ Утро — {morningDone ? '✅' : '❌'}</li>
            <li>🧠 Коуч — {coachDone ? '✅' : '❌'}</li>
            <li>📋 Привычки — {habitsDone} / {totalHabits}</li>
          </ul>
        </div>

        <div className="grid grid-cols-1 gap-3">
          <button className="w-full bg-blue-600 text-white py-3 rounded-xl shadow active:scale-95 transition">
            🧠 Коуч
          </button>
          <button className="w-full bg-green-600 text-white py-3 rounded-xl shadow active:scale-95 transition">
            📋 Привычки
          </button>
          <button className="w-full bg-indigo-600 text-white py-3 rounded-xl shadow active:scale-95 transition">
            🌙 Вечерка
          </button>
        </div>
      </div>
    </div>
  )
}

export default App
<h1 className="text-2xl font-bold mb-2">🔥 Я реально обновил страницу!</h1>
