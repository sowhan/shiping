import React, { useCallback, useEffect, useRef, useState } from 'react';

interface LoadingProps {
  size?: 'sm' | 'md' | 'lg';
  variant?: 'spinner' | 'dots' | 'pulse' | 'ship';
  text?: string;
  fullScreen?: boolean;
  className?: string;
}

/**
 * Loading component with maritime-themed animations.
 * Provides multiple variants for different loading contexts.
 */
export const Loading: React.FC<LoadingProps> = ({
  size = 'md',
  variant = 'spinner',
  text,
  fullScreen = false,
  className = ''
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  const textSizeClasses = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base'
  };

  const renderSpinner = () => (
    <div className={`${sizeClasses[size]} animate-spin rounded-full border-2 border-gray-300 border-t-maritime-blue`} />
  );

  const renderDots = () => (
    <div className="flex space-x-1">
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          className={`${size === 'sm' ? 'w-1.5 h-1.5' : size === 'md' ? 'w-2 h-2' : 'w-3 h-3'} bg-maritime-blue rounded-full animate-bounce`}
          style={{ animationDelay: `${i * 0.15}s` }}
        />
      ))}
    </div>
  );

  const renderPulse = () => (
    <div className={`${sizeClasses[size]} bg-maritime-blue rounded-full animate-pulse`} />
  );

  const renderShip = () => (
    <div className={`${sizeClasses[size]} relative`}>
      <svg viewBox="0 0 24 24" fill="none" className="animate-bounce">
        <path
          d="M3 17H21L19 21H5L3 17Z"
          fill="currentColor"
          className="text-maritime-blue"
        />
        <path
          d="M5 17V13L12 10L19 13V17"
          fill="currentColor"
          className="text-maritime-blue opacity-80"
        />
        <path
          d="M12 10V6M12 6L9 9M12 6L15 9"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="text-maritime-blue"
        />
      </svg>
    </div>
  );

  const renderVariant = () => {
    switch (variant) {
      case 'dots': return renderDots();
      case 'pulse': return renderPulse();
      case 'ship': return renderShip();
      default: return renderSpinner();
    }
  };

  const content = (
    <div className={`flex flex-col items-center justify-center gap-3 ${className}`}>
      {renderVariant()}
      {text && (
        <p className={`${textSizeClasses[size]} text-gray-600 animate-pulse`}>
          {text}
        </p>
      )}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-white/80 backdrop-blur-sm flex items-center justify-center z-50">
        {content}
      </div>
    );
  }

  return content;
};

export default Loading;
