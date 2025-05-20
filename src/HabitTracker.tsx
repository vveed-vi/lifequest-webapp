import { useEffect, useState } from 'react'

const HABITS = [
  { name: 'бритье+умыт+зубы', icon: '🧼' },
  { name: 'английский', icon: '📖' },
  { name: 'медитация', icon: '🧩' },
  { name: 'прогулка', icon: '🧘‍' },
  { name: 'ужин', icon: '🍽️' },
  { name: 'гитара+чтение', icon: '🎸' },
  { name: 'зарядка', icon: '🏋️' },
  { name: 'вода 1.5л', icon: '💧' },
  { name: 'дневник', icon: '📄' },
  { name: 'душ', icon: '🧧' }
]

const days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

function getThisWeekDates() {
  const now = new Date()
  const monday = new Date(now.setDate(now.getDate() - now.getDay() + 1))
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(monday)
    d.setDate(monday.getDate() + i)
    return d.toISOString().slice(0, 10)
  })
}

function HabitTracker() {
  const [data, setData] = useState<{ [date: string]: { [habit: string]: boolean } }>({})

  const weekDates = getThisWeekDates()
  const today = new Date().toISOString().slice(0, 10)

  useEffect(() => {
    const raw = localStorage.getItem('habits')
    if (raw) setData(JSON.parse(raw))
  }, [])

  useEffect(() => {
    localStorage.setItem('habits', JSON.stringify(data))
  }, [data])

  const toggle = (date: string, habit: string) => {
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
    <div className="min-h-screen bg-zinc-900 text-white p-6 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-6 flex items-center gap-2">
        🧩 Привычки на неделю
      </h1>

      <div className="w-full max-w-4xl overflow-x-auto">
        <table className="w-full text-left border-separate border-spacing-y-2">
          <thead>
            <tr>
              <th className="p-2">Привычка</th>
              {days.map(day => (
                <th key={day} className="p-2 text-center text-sm text-gray-400">{day}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {HABITS.map(habit => (
              <tr key={habit.name} className="bg-zinc-800 rounded-xl">
                <td className="p-2 font-medium flex items-center gap-2">
                  <span>{habit.icon}</span>
                  <span>{habit.name}</span>
                </td>
                {weekDates.map(date => (
                  <td key={date} className="text-center">
                    <button
                      onClick={() => toggle(date, habit.name)}
                      className={`w-8 h-8 rounded-full transition duration-200 flex items-center justify-center 
                        ${data[date]?.[habit.name] ? 'bg-orange-500' : 'bg-zinc-700 hover:bg-zinc-600'}`}
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
  )
}

export default HabitTracker
