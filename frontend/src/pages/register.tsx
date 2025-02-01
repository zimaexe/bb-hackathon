'use client';

import React from 'react';
import "../app/globals.css";
import InputField from '../components/inputField';
import Button from '../components/button';
import { loginRequest } from './login';

interface RegisterProps {
  email: string;
  password: string;
  businessName: string;
  phoneNumber: string;
}

async function registerRequest({ email, password, businessName, phoneNumber } : RegisterProps) {
  const endpoint = "http://192.168.1.85:1488";
  await fetch(`${endpoint}/register`, {
    method: "POST",
    headers: {
      "content-type": "application/json"
    },
    body: JSON.stringify({
      email: email,
      phone: phoneNumber,
      business_name: businessName,
      password: password,
    }),
  })
  .then((res) => {
    console.log("Response", res)
    return res.json()
  })
  .catch((err) => {
    console.log("Error", err)
  });

  loginRequest({ email, password });
}

export default function Register() {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [businessName, setBusinessName] = React.useState('');
  const [phoneNumber, setPhoneNumber] = React.useState('');

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
          <InputField onChange={setBusinessName} type='text' placeholder='name of business' />
          <InputField onChange={setEmail} type='text' placeholder='email' />
          <InputField onChange={setPhoneNumber} type='phone' placeholder='phone number' />
          <InputField onChange={setPassword} type='password' placeholder='password' />
          <Button variant='action' onClick={() => registerRequest({ email, password, businessName, phoneNumber })}>sign up</Button>
        </div>
      </div>
    </div>
  )
}
