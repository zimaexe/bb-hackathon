'use server';

import React, { useEffect, useState } from 'react';
import '../../app/globals.css';
import Sidebar from '../../components/sidebar';
import Button from '../../components/button';

interface ProfileFieldProps {
  idx: number;
  label: string;
  value: string | number;
  changeField: (index: number, value: string) => void;
}

function ProfileField({ idx, label, value, changeField } : ProfileFieldProps) {
  return (
    <div className="
      flex gap-[5px]
      w-full
    ">
      <div className="
        w-[170px]
        font-bold text-[20px] text-white
        bg-[#ADADAD]
        flex items-center
        p-[10px] rounded-[10px_0_0_10px]
      ">
        {label}
      </div>
      <input
        type='text'
        placeholder={label}
        value={value}
        onChange={(e) => changeField(idx, e.target.value)}
        className="
          w-full px-[20px] py-[10px] rounded-[0_10px_10px_0]
          text-[24px]
          bg-[#cccccc] bg-opacity-[0.7]
          placeholder-[#7e7e7e] text-[#000000]
          focus:outline-none
        "
      />
    </div>
  )
}

export default function Profile() {
  const [wasChanged, setWasChanged] = useState(false);
  const [fields, setFields] = useState([
    { label: 'meno', value: 'Janko' },
    { label: 'priezvisko', value: 'Hraško' },
    { label: 'nazov firmy', value: 'NazovFirmy' },
    { label: 'telefon', value: '0904123456' },
    { label: 'email', value: 'something@gmail.com' },
    { label: 'ICO', value: 123123123123 },
    { label: 'rodne cislo', value: '123456/7890' }
  ]);
  const [initialFields,] = useState(structuredClone(fields));

  useEffect(() => {
    const changed = fields.some((field, index) => field.value !== initialFields[index].value);
    setWasChanged(changed);
  }, [fields, initialFields]);

  const changeField = (index: number, value: string) => {
    const tmpFields = fields;
    tmpFields[index].value = value;
    setFields([...tmpFields]);
  }

  return (
    <div className="
      font-sans h-screen w-full flex justify-center items-center
      bg-white text-black
    ">
      <Sidebar />
      <div className="
        flex w-full flex-col h-screen
        px-[70px] pt-[150px]
      ">
        <div className="
          flex flex-col gap-[30px]
          w-full
        ">
          <h1 className="font-bold text-[48px]">Profil</h1>
          <div className="
            flex flex-col gap-[20px]
            w-[800px]
          ">
            {fields.map((field, index) => (
              <ProfileField key={index} idx={index} changeField={changeField} label={field.label} value={field.value} />
            ))}
          </div>
        </div>
        {wasChanged && <Button variant='action' additionalClasses='mt-[30px]'>ulozit</Button>}
      </div>
    </div>
  )
}
