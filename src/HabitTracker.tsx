import { useEffect, useState } from 'react'

const WEEKDAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
const HABITS = [
  { name: 'бритье+умыт+зубы', icon: '🧼' },
  { name: 'английский', icon: '📖' },
  { name: 'медитация', icon: '🧘‍♂️' },
  { name: 'прогулка', icon: '🚶‍♂️' },
  { name: 'ужин', icon: '🍽️' },
  { name: 'гитара+чтение', icon: '🎸' },
  { name: 'зарядка', icon: '🏋️‍♂️' },
  { name: 'вода 1.5л', icon: '💧' },
  { name: 'дневник', icon: '📄' },
  { name: 'душ', icon: '🟥' }
]

function getToday() {
  return new Date().toISOString().slice(0, 10)
}

function getWeekDates() {
  const today = new Date()
  const monday = new Date(today)
  monday.setDate(today.getDate() - today.getDay() + 1)
  return WEEKDAYS.map((_, i) => {
    const date = new Date(monday)
    date.setDate(monday.getDate() + i)
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

  const toggle = (habit: string, date: string) => {
    setData(prev => {
      const prevDay = prev[date] || {}
      return {
        ...prev,
        [date]: {
          ...prevDay,
          [habit]: !prevDay[habit]
        }
      }
    })
  }

  return (
    <div className="min-h-screen bg-[#111] text-white p-6 flex justify-center">
      <div className="w-full max-w-5xl">
        <h1 className="text-4xl font-extrabold mb-8 flex items-center gap-4">
          <span>🧩</span> Привычки на неделю
        </h1>

        <div className="grid grid-cols-8 gap-3">
          <div className="font-bold">Привычка</div>
          {WEEKDAYS.map(d => (
            <div key={d} className="text-center font-bold">{d}</div>
          ))}

          {HABITS.map(habit => (
            <>
              <div className="flex items-center gap-2 font-medium">
                <span>{habit.icon}</span>
                {habit.name}
              </div>
              {weekDates.map(date => (
                <button
                  key={date}
                  onClick={() => toggle(habit.name, date)}
                  className={`rounded-full w-8 h-8 flex items-center justify-center transition-all
                    ${data?.[date]?.[habit.name] ? 'bg-orange-500' : 'bg-gray-800 hover:bg-gray-700'}`}
                />
              ))}
            </>
          ))}
        </div>
      </div>
    </div>
  )
}

export default HabitTracker
