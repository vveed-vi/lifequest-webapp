import { useEffect, useState } from 'react'

const HABITS = [
  'бритье+умыт+зубы',
  'английский',
  'медитация',
  'прогулка',
  'ужин',
  'гитара+чтение',
  'зарядка',
  'вода 1.5л',
  'дневник',
  'душ'
]

function getToday() {
  return new Date().toISOString().slice(0, 10) // "2025-05-19"
}

function HabitTracker() {
  const [data, setData] = useState<{ [date: string]: { [habit: string]: boolean } }>({})

  const today = getToday()

  useEffect(() => {
    const raw = localStorage.getItem('habits')
    if (raw) setData(JSON.parse(raw))
  }, [])

  useEffect(() => {
    localStorage.setItem('habits', JSON.stringify(data))
  }, [data])

  const toggleHabit = (habit: string) => {
    setData(prev => {
      const todayData = prev[today] || {}
      return {
        ...prev,
        [today]: {
          ...todayData,
          [habit]: !todayData[habit]
        }
      }
    })
  }

  const getStreak = (habit: string) => {
    const dates = Object.keys(data).sort((a, b) => b.localeCompare(a))
    let streak = 0
    for (const date of dates) {
      if (data[date][habit]) {
        streak++
      } else {
        break
      }
    }
    return streak
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-4">
      <h1 className="text-2xl font-bold mb-4">🧩 Привычки на сегодня</h1>
      <ul className="space-y-3">
        {HABITS.map(habit => (
          <li key={habit} className="flex items-center gap-4">
            <input
              type="checkbox"
              checked={data[today]?.[habit] || false}
              onChange={() => toggleHabit(habit)}
              className="w-5 h-5"
            />
            <span className="flex-1">{habit}</span>
            <span className="text-sm text-gray-400">🔥 {getStreak(habit)}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default HabitTracker
