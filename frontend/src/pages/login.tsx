'use client';

import React from 'react';
import "../app/globals.css";
import InputField from '../components/inputField';
import Button from '../components/button';

export default function Login() {
  return (
    <div className="
      font-sans h-screen w-full
      flex justify-center items-center
      bg-[url('/simple_back.png')] bg-cover bg-top
    ">
      <div className='h-screen w-full flex justify-center items-center bg-black bg-opacity-[0.6]'>
        <div className="
          flex flex-col gap-[30px] items-center
          bg-[#a3a3a3] bg-opacity-[0.15]  
          px-[100px] pt-[200px] pb-[150px] rounded-[50px]
          w-[650px]
        ">
          <h1 className="
            text-[64px] text-center text-white opacity-[0.7] font-bold          
          ">
            Sign in
          </h1>
          <InputField type='text' placeholder='email' />
          <InputField type='password' placeholder='password' />
          <Button variant='action'>sign in</Button>
        </div>
      </div>
    </div>
  )
}
