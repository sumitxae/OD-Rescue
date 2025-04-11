import { FC, ReactNode } from 'react'
interface LayoutProps {
  children: ReactNode
}

const Layout: FC<LayoutProps> = ({ children }) => {
  return (
    <div className="max-w-screen-2xl mx-auto px-4 w-full h-full ">
      {children}
    </div>
  )
}

export default Layout
