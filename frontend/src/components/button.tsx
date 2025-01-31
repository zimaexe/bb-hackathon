'use client';

import React from 'react';

interface ButtonProps {
  variant: 'primary' | 'secondary' | 'action';
  children: React.ReactNode;
  additionalClasses?: string;
  onClick?: () => void;
}

export default function Button({ variant = 'secondary', children, additionalClasses, onClick }: ButtonProps) {
  const defaultStyle = " \
    px-[20px] py-[10px] rounded-[40px] \
    transition-all duration-200 ease-in-out \
    focus:outline-none \
  ";

  let className = '';

  switch (variant) {
    case 'primary':
      className = 'primary bg-blue-500 text-white hover:shadow-blue-500';
      break;
    case 'secondary':
      className = 'secondary bg-gray-500 text-white hover:shadow-gray-500';
      break;
    case 'action':
      className = 'bg-[#EDB744] text-black text-[24px] hover:shadow-[0px_0px_8px_#EDB744] w-[150px]';
      break;
    default:
      className = '';
  }
  
  return (
    <button
      className={defaultStyle + ' ' + className + ' ' + additionalClasses}
      onClick={onClick}
    >
      {children}
    </button>
  )
}
