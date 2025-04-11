import { Routes, Route } from 'react-router-dom'
import { routes, RoutesType } from '@/router/data'

export default function Router() {
  return (
    <Routes>
      {routes.map((route: RoutesType) => (
        <Route key={route.path} path={route.path} element={route.element} />
      ))}

      <Route path="*" element={<div>404 - Page Not Found</div>} />
    </Routes>
  )
}
