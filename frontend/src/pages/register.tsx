'use client';

import React from 'react';
import "../app/globals.css";
import InputField from '../components/inputField';
import Button from '../components/button';

export default function Register() {
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
          px-[100px] py-[100px] rounded-[50px]
          w-[750px]
        ">
          <h1 className="
            text-[64px] text-center text-white opacity-[0.7] font-bold          
          ">
            Sign up
          </h1>
          <InputField type='text' placeholder='name of business' />
          <InputField type='text' placeholder='email' />
          <InputField type='phone' placeholder='phone number' />
          <InputField type='password' placeholder='password' />
          <Button variant='action'>sign up</Button>
        </div>
      </div>
    </div>
  )
}
