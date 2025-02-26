'use client'
import React, { FC } from 'react'
import { motion } from 'motion/react'

const PageLoadingAnimation: FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  return (
    <motion.section
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5, ease: 'easeInOut' }}
      className="w-full h-full"
    >
      {children}
    </motion.section>
  )
}

export default PageLoadingAnimation
