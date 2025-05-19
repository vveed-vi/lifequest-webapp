import { useEffect, useState } from 'react'

const HABITS = [
  { name: 'бритье+умыт+зубы', icon: '🛁' },
  { name: 'английский', icon: '📚' },
  { name: 'медитация', icon: '🧘' },
  { name: 'прогулка', icon: '🚶' },
  { name: 'ужин', icon: '🍽️' },
  { name: 'гитара+чтение', icon: '🎸' },
  { name: 'зарядка', icon: '🏋️' },
  { name: 'вода 1.5л', icon: '💧' },
  { name: 'дневник', icon: '📝' },
  { name: 'душ', icon: '🧼' }
]

const DAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

function getWeekDates() {
  const today = new Date()
  const day = today.getDay()
  const mondayOffset = day === 0 ? -6 : 1 - day

  return Array.from({ length: 7 }, (_, i) => {
    const date = new Date(today)
    date.setDate(today.getDate() + mondayOffset + i)
    return date.toISOString().slice(0, 10)
  })
}

function HabitTracker() {
  const [data, setData] = useState<{ [date: string]: { [habit: string]: boolean } }>({})

  const weekDates = getWeekDates()

  useEffect(() => {
    const raw = localStorage.getItem('habits')
    if (raw) setData(JSON.parse(raw))
  }, [])

  useEffect(() => {
    localStorage.setItem('habits', JSON.stringify(data))
  }, [data])

  const toggleHabit = (date: string, habit: string) => {
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
    <div className="min-h-screen bg-gray-950 text-white p-4">
      <h1 className="text-2xl font-bold mb-4">🧩 Привычки на неделю</h1>
      <ul className="space-y-4">
        {HABITS.map(({ name, icon }) => (
          <li key={name}>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xl">{icon}</span>
              <span className="font-medium">{name}</span>
            </div>
            <div className="flex gap-2 pl-7">
              {weekDates.map((date, i) => (
                <button
                  key={date}
                  onClick={() => toggleHabit(date, name)}
                  className="text-xl"
                >
                  {data[date]?.[name] ? '🔥' : '⚫'}
                </button>
              ))}
            </div>
          </li>
        ))}
      </ul>
      <div className="flex gap-2 mt-6 pl-8 text-xs text-gray-400">
        {DAYS.map(day => (
          <span key={day} className="w-6 text-center">{day}</span>
        ))}
      </div>
    </div>
  )
}

export default HabitTracker
