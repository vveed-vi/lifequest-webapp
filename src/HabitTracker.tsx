// src/HabitTracker.tsx
import { useEffect, useState } from 'react'

const HABITS = [
  { icon: '🧼', name: 'бритье+умыт+зубы' },
  { icon: '📚', name: 'английский' },
  { icon: '🧘', name: 'медитация' },
  { icon: '🧍', name: 'прогулка' },
  { icon: '🍽', name: 'ужин' },
  { icon: '🎸', name: 'гитара+чтение' },
  { icon: '🏋', name: 'зарядка' },
  { icon: '💧', name: 'вода 1.5л' },
  { icon: '📜', name: 'дневник' },
  { icon: '🧻', name: 'душ' },
]

const DAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

function getCurrentWeekDates() {
  const today = new Date()
  const monday = new Date(today)
  monday.setDate(today.getDate() - ((today.getDay() + 6) % 7))
  return DAYS.map((_, i) => {
    const date = new Date(monday)
    date.setDate(monday.getDate() + i)
    return date.toISOString().slice(0, 10)
  })
}

function HabitTracker() {
  const [data, setData] = useState<{ [date: string]: { [habit: string]: boolean } }>({})
  const weekDates = getCurrentWeekDates()
  const todayStr = new Date().toISOString().slice(0, 10)

  useEffect(() => {
    const raw = localStorage.getItem('habits')
    if (raw) setData(JSON.parse(raw))
  }, [])

  useEffect(() => {
    localStorage.setItem('habits', JSON.stringify(data))
  }, [data])

  const toggleHabit = (habit: string, date: string) => {
    setData(prev => {
      const dayData = prev[date] || {}
      return {
        ...prev,
        [date]: {
          ...dayData,
          [habit]: !dayData[habit]
        }
      }
    })
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white py-10 px-4 flex justify-center">
      <div className="w-full max-w-5xl">
        <h1 className="text-3xl font-extrabold mb-8 flex items-center gap-4">
          <img src="/favicon.ico" className="w-8 h-8" />
          Привычки на неделю
        </h1>
        <div className="overflow-x-auto">
          <table className="w-full text-center border-separate border-spacing-y-2">
            <thead>
              <tr>
                <th className="text-left px-2"> </th>
                {DAYS.map((day, idx) => (
                  <th key={day} className={`text-sm font-semibold px-2 ${weekDates[idx] === todayStr ? 'text-yellow-400' : 'text-gray-400'}`}>{day}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {HABITS.map(habit => (
                <tr key={habit.name} className="text-left">
                  <td className="whitespace-nowrap font-medium flex items-center gap-2 px-2">
                    <span className="text-xl">{habit.icon}</span>
                    <span>{habit.name}</span>
                  </td>
                  {weekDates.map(date => (
                    <td key={date}>
                      <button
                        onClick={() => toggleHabit(habit.name, date)}
                        className={`w-8 h-8 rounded-full transition-transform duration-150 flex items-center justify-center ${data[date]?.[habit.name] ? 'bg-orange-500' : 'bg-gray-800'} hover:scale-110`}
                      >
                        {data[date]?.[habit.name] ? '🔥' : ''}
                      </button>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default HabitTracker
