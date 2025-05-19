import { useEffect, useState } from 'react'

const HABITS = [
  ['🪥', 'бритье+умыт+зубы'],
  ['📚', 'английский'],
  ['🧘', 'медитация'],
  ['🚶', 'прогулка'],
  ['🍽️', 'ужин'],
  ['🎸', 'гитара+чтение'],
  ['🏋️', 'зарядка'],
  ['💧', 'вода 1.5л'],
  ['📓', 'дневник'],
  ['🧼', 'душ'],
]

const WEEKDAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

function getWeekKey() {
  const d = new Date()
  const monday = new Date(d.setDate(d.getDate() - ((d.getDay() + 6) % 7)))
  return monday.toISOString().slice(0, 10)
}

function HabitTracker() {
  const [data, setData] = useState<{ [week: string]: { [habit: string]: boolean[] } }>({})
  const weekKey = getWeekKey()
  const today = new Date().getDay() || 7 // 1=Пн, 7=Вс

  useEffect(() => {
    const raw = localStorage.getItem('habit_week_data')
    if (raw) setData(JSON.parse(raw))
  }, [])

  useEffect(() => {
    localStorage.setItem('habit_week_data', JSON.stringify(data))
  }, [data])

  const toggle = (habit: string, dayIdx: number) => {
    setData(prev => {
      const week = prev[weekKey] || {}
      const days = week[habit] || Array(7).fill(false)
      days[dayIdx] = !days[dayIdx]
      return {
        ...prev,
        [weekKey]: {
          ...week,
          [habit]: days
        }
      }
    })
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4 flex justify-center items-start">
      <div className="w-full max-w-3xl">
        <h1 className="text-3xl font-bold mb-6">🧩 Привычки на неделю</h1>
        <div className="grid grid-cols-[auto_repeat(7,minmax(2rem,1fr))] gap-3">
          <div></div>
          {WEEKDAYS.map(day => (
            <div key={day} className="text-center font-bold">{day}</div>
          ))}
          {HABITS.map(([icon, name]) => (
            <>
              <div key={name} className="flex items-center gap-2 whitespace-nowrap">{icon} {name}</div>
              {WEEKDAYS.map((_, i) => {
                const checked = data?.[weekKey]?.[name]?.[i] ?? false
                const todayIdx = today - 1
                const isToday = i === todayIdx
                return (
                  <button
                    key={i}
                    onClick={() => toggle(name, i)}
                    className={`rounded-full w-6 h-6 flex items-center justify-center transition ${
                      checked ? 'bg-orange-500' : 'bg-gray-800'
                    } ${isToday ? 'ring-2 ring-yellow-400' : ''}`}
                  >
                    {checked ? '🔥' : ''}
                  </button>
                )
              })}
            </>
          ))}
        </div>
      </div>
    </div>
  )
}

export default HabitTracker
