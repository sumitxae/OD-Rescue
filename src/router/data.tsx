import { JSX } from 'react'
import Home from '@/pages/home'

export interface RoutesType {
  name: string
  path: string
  element: JSX.Element
  isProtected: boolean
}

export const routes: RoutesType[] = [
  {
    name: 'Home',
    path: '/',
    element: <Home />,
    isProtected: false,
  },
]
