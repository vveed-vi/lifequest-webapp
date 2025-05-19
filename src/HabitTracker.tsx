import { useState } from 'react'

const habits = [
  { id: 1, name: 'бритье+умыться+зубы', category: 'Утро' },
  { id: 2, name: 'английский', category: 'Фокус' },
  { id: 3, name: 'медитация', category: 'Фокус' },
  { id: 4, name: 'прогулка', category: 'Фокус' },
  { id: 5, name: 'ужин', category: 'Завершение дня' },
]

function HabitTracker() {
  const [completed, setCompleted] = useState<number[]>([])

  const toggleHabit = (id: number) => {
    setCompleted(prev =>
      prev.includes(id) ? prev.filter(hid => hid !== id) : [...prev, id]
    )
  }

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">🧩 Привычки на сегодня</h2>
      <ul className="space-y-3">
        {habits.map(habit => (
          <li
            key={habit.id}
            className="flex justify-between items-center bg-white rounded-xl shadow p-3"
          >
            <span>{habit.name}</span>
            <input
              type="checkbox"
              checked={completed.includes(habit.id)}
              onChange={() => toggleHabit(habit.id)}
              className="w-5 h-5"
            />
          </li>
        ))}
      </ul>
    </div>
  )
}

export default HabitTracker
