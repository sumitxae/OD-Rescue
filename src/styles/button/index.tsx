'use client'
import { Link } from 'react-router-dom'
import React from 'react'
import { motion } from 'motion/react'
import { LoadingIcon } from '@/styles/icons'

type ButtonProps = {
  children: React.ReactNode
  theme?: 'primary' | 'secondary'
  size?: 'sm' | 'md' | 'lg'
  rounded?: boolean
  className?: string
  onClick?: () => void
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
  loading?: boolean
}

const getButtonClasses = (
  theme: 'primary' | 'secondary',
  size: 'sm' | 'md' | 'lg',
  disabled: boolean,
  className: string
) => {
  const baseClasses =
    'inline-flex items-center justify-center font-medium transition duration-200 focus:outline-none'
  const themeClasses =
    theme === 'primary'
      ? 'border-2 border-black text-white bg-gray-950 hover:bg-gray-900 '
      : 'border-2 border-c-yellow text-c-yellow hover:bg-c-yellow hover:text-black'
  const sizeClasses =
    size === 'sm'
      ? 'px-4 py-2 text-sm'
      : size === 'lg'
        ? 'px-8 py-4 text-lg'
        : 'px-6 py-3 text-base'
  const disabledClasses = disabled
    ? 'opacity-50 cursor-not-allowed'
    : 'hover:shadow-lg focus:ring-2 focus:ring-offset-2'

  return `${baseClasses} ${themeClasses} ${sizeClasses} ${disabledClasses} ${className} flex items-center justify-between gap-3`
}

const MotionButton = motion.create('button')
export const Button: React.FC<ButtonProps> = ({
  children,
  theme = 'primary',
  size = 'md',
  className = '',
  onClick,
  disabled = false,
  type = 'button',
  loading = false,
}) => {
  const buttonClasses = getButtonClasses(theme, size, disabled, className)

  return (
    <MotionButton
      className={`font-pop tracking-wider ${buttonClasses}`}
      onClick={onClick}
      disabled={disabled}
      type={type}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 1 }}
    >
      {loading ? <LoadingIcon /> : children}
    </MotionButton>
  )
}

type LinkButtonProps = ButtonProps & {
  href: string
}

const MotionLink = motion.create(Link)

export const LinkButton: React.FC<LinkButtonProps> = ({
  children,
  href,
  theme = 'primary',
  size = 'md',
  className = '',
  onClick,
  disabled = false,
  type = 'button',
  loading = false,
}) => {
  const buttonClasses = getButtonClasses(theme, size, disabled, className)

  return (
    <MotionLink
      to={href}
      className={`font-pop tracking-wider ${buttonClasses}`}
      onClick={onClick}
      type={type}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 1 }}
    >
      {loading ? <LoadingIcon /> : children}
    </MotionLink>
  )
}
