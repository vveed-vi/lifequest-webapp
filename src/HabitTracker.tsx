import { useEffect, useState } from 'react'

const HABITS = [
  { key: 'бритье+умыт+зубы', label: '🧼 бритье+умыт+зубы' },
  { key: 'английский', label: '📚 английский' },
  { key: 'медитация', label: '🧘 медитация' },
  { key: 'прогулка', label: '🚶 прогулка' },
  { key: 'ужин', label: '🍽️ ужин' },
  { key: 'гитара+чтение', label: '🎸 гитара+чтение' },
  { key: 'зарядка', label: '🏋️ зарядка' },
  { key: 'вода 1.5л', label: '💧 вода 1.5л' },
  { key: 'дневник', label: '📓 дневник' },
  { key: 'душ', label: '🚿 душ' }
]

function getToday() {
  return new Date().toISOString().slice(0, 10)
}

export default function HabitTracker() {
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
      if (data[date]?.[habit]) {
        streak++
      } else {
        break
      }
    }
    return streak
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-4">
      <h1 className="text-3xl font-extrabold mb-6 flex items-center gap-2">
        <span>🧩</span> <span>Привычки на сегодня</span>
      </h1>
      <div className="space-y-3">
        {HABITS.map(habit => (
          <div
            key={habit.key}
            className="flex justify-between items-center bg-gray-800 rounded-xl p-4 shadow"
          >
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={data[today]?.[habit.key] || false}
                onChange={() => toggleHabit(habit.key)}
                className="w-5 h-5 accent-green-500"
              />
              <span className="text-base">{habit.label}</span>
            </label>
            <span className="text-lg text-orange-400 font-semibold">
              🔥 {getStreak(habit.key)}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
