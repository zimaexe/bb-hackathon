'use client';

import React from 'react';
import "../app/globals.css";
import InputField from '../components/inputField';
import Button from '../components/button';

export function loginRequest({ email, password } : { email: string, password: string }) {
  const form = document.createElement("form");
  form.className = "hidden";

  const emailInput = document.createElement("input");
  emailInput.type = "text";
  emailInput.name = "username";
  emailInput.value = email;
  form.appendChild(emailInput);

  const passwordInput = document.createElement("input");
  passwordInput.type = "password";
  passwordInput.name = "password";
  passwordInput.value = password;
  form.appendChild(passwordInput);

  const formData = new FormData(form);
  const endpoint = "http://localhost:8000";

  fetch(`${endpoint}/login`, {
    method: "POST",
    body: formData,
  })
  .then((res) => res.json())
  .then((token) => {
    console.log("Token", token)
    localStorage.setItem("token", JSON.stringify(token))
    window.location.href = "/user/fairs"
  })
  .catch((err) => {
    console.log("Error", err)
  })
}

export default function Login() {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');

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
          <InputField onChange={setEmail} type='text' placeholder='email' />
          <InputField onChange={setPassword} type='password' placeholder='password' />
          <Button variant='action' onClick={() => loginRequest({ email, password })}>sign in</Button>
        </div>
      </div>
    </div>
  )
}
