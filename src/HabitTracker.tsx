import { useEffect, useState } from 'react'

const habitsList = [
  "бритье+умывться+зубы",
  "английский",
  "медитация",
  "прогулка",
  "ужин"
]

function HabitTracker() {
  const [checked, setChecked] = useState<{ [key: string]: boolean }>({})

  // Загружаем состояние при загрузке страницы
  useEffect(() => {
    const saved = localStorage.getItem('habit-checks')
    if (saved) setChecked(JSON.parse(saved))
  }, [])

  // Сохраняем состояние при каждом изменении
  useEffect(() => {
    localStorage.setItem('habit-checks', JSON.stringify(checked))
  }, [checked])

  const toggle = (habit: string) => {
    setChecked(prev => ({
      ...prev,
      [habit]: !prev[habit]
    }))
  }

  return (
    <div className="p-4 text-white">
      <h1 className="text-2xl font-bold mb-4">🧩 Привычки на сегодня</h1>
      <ul className="space-y-2">
        {habitsList.map(habit => (
          <li key={habit} className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={checked[habit] || false}
              onChange={() => toggle(habit)}
              className="w-4 h-4"
            />
            <span>{habit}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default HabitTracker
