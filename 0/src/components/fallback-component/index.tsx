import { useEffect, useState } from 'react'
const Fallback = () => {
  const [counter, setCounter] = useState(5)

  useEffect(() => {
    // decrease counter by 1 every 1 second
    const interval = setInterval(() => {
      setCounter(counter - 1)
    }, 1000)
    if (counter === 0) {
      window.location.href = '/login'
    }
    return () => clearInterval(interval)
  }, [counter])

  return (
    <div>
      <div className="flex flex-col items-center justify-center h-screen">
        <h1 className="text-2xl font-bold text-red-500    ">
          Something went wrong
        </h1>
        <p className="text-sm">
          Redirecting to login page in {counter} seconds
        </p>
      </div>
    </div>
  )
}

export default Fallback
