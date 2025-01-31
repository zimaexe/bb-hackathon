'use client';

import React from 'react';

interface InputFieldProps {
    type: string;
    placeholder: string;
    value?: string;
}

export default function InputField({ type, placeholder, value } : InputFieldProps) {
  return (
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      className="
        w-full px-[20px] py-[15px] rounded-[20px]
        text-center text-[24px]
        bg-white bg-opacity-[0.7]
        placeholder-[#7e7e7e] text-[#363636]
        focus:outline-none
      "
    />
  )
}
