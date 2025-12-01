/**
 * Button Component
 * Reusable button with maritime theme variants
 */

import React from 'react';
import { Loader2 } from 'lucide-react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  children: React.ReactNode;
}

const variantStyles = {
  primary: 'bg-maritime-blue-500 hover:bg-maritime-blue-600 text-white border-transparent',
  secondary: 'bg-slate-100 hover:bg-slate-200 text-slate-700 border-transparent',
  outline: 'bg-transparent hover:bg-maritime-blue-50 text-maritime-blue-500 border-maritime-blue-500',
  danger: 'bg-red-500 hover:bg-red-600 text-white border-transparent',
};

const sizeStyles = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg',
};

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  children,
  className = '',
  disabled,
  ...props
}) => {
  const baseStyles = `
    inline-flex items-center justify-center
    font-medium rounded-lg
    border transition-colors duration-200
    focus:outline-none focus:ring-2 focus:ring-maritime-blue-400 focus:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
  `;

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
      ) : leftIcon ? (
        <span className="mr-2">{leftIcon}</span>
      ) : null}
      {children}
      {rightIcon && !isLoading && <span className="ml-2">{rightIcon}</span>}
    </button>
  );
};

export default Button;
