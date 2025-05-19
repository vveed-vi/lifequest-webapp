import { useEffect, useState } from 'react'

const HABITS = [
  { name: 'бритье+умыт+зубы', icon: '🧼' },
  { name: 'английский', icon: '📚' },
  { name: 'медитация', icon: '🧘' },
  { name: 'прогулка', icon: '🚶' },
  { name: 'ужин', icon: '🍽️' },
  { name: 'гитара+чтение', icon: '🎸' },
  { name: 'зарядка', icon: '🏋️' },
  { name: 'вода 1.5л', icon: '💧' },
  { name: 'дневник', icon: '📝' },
  { name: 'душ', icon: '🛁' }
]

const WEEK_DAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

function getWeekKey(index: number) {
  const baseDate = new Date('2025-05-19')
  const day = new Date(baseDate)
  day.setDate(baseDate.getDate() + index)
  return day.toISOString().slice(0, 10)
}

function HabitTracker() {
  const [data, setData] = useState<{ [date: string]: { [habit: string]: boolean } }>({})

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
    <div className="min-h-screen bg-gray-950 text-white p-4">
      <h1 className="text-3xl font-bold mb-6">🧩 Привычки на неделю</h1>
      <div className="grid grid-cols-[auto_repeat(7,_minmax(0,_1fr))] gap-4 text-center items-center">
        <div></div>
        {WEEK_DAYS.map((d, i) => (
          <div key={i} className="font-semibold text-sm text-gray-300">{d}</div>
        ))}

        {HABITS.map(habit => (
          <>
            <div key={habit.name} className="flex items-center gap-2 justify-start">
              <span>{habit.icon}</span>
              <span>{habit.name}</span>
            </div>
            {WEEK_DAYS.map((_, i) => {
              const dateKey = getWeekKey(i)
              const done = data[dateKey]?.[habit.name] || false
              return (
                <div
                  key={dateKey + habit.name}
                  onClick={() => toggleHabit(habit.name, dateKey)}
                  className={`cursor-pointer w-6 h-6 rounded-full mx-auto border border-gray-500 flex items-center justify-center ${done ? 'bg-orange-500' : 'bg-gray-700'}`}
                ></div>
              )
            })}
          </>
        ))}
      </div>
    </div>
  )
}

export default HabitTracker
