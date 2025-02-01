'use client';

import React, { Dispatch, SetStateAction } from 'react';

interface InputFieldProps {
    type: string;
    placeholder: string;
    value?: string;
    onChange?: Dispatch<SetStateAction<string>>;
}

export default function InputField({ type, placeholder, value, onChange } : InputFieldProps) {
  return (
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={(e) => {
        if (onChange) onChange(e.target.value)
      }}
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
