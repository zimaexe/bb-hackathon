'use client';

import React from 'react';
import '../../app/globals.css';
import Sidebar from '../../components/sidebar';

export default function Payments() {
  return (
    <div className="
      font-sans h-screen w-full flex justify-center items-center
      bg-white text-black
    ">
      <Sidebar />
      <div className='flex w-full justify-center items-center'>
        payments
      </div>
    </div>
  )
}
