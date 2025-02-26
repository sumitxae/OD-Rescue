import { BrowserRouter } from 'react-router-dom'
import { ErrorBoundary } from 'react-error-boundary'
import Fallback from './components/fallback-component'
import Router from '@/router'
const App = () => {
  return (
    <ErrorBoundary FallbackComponent={Fallback}>
      <BrowserRouter>
        <Router />
      </BrowserRouter>
    </ErrorBoundary>
  )
}

export default App
