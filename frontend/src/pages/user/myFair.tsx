'use client';

import React from 'react';
import '../../app/globals.css';
import Sidebar from '../../components/sidebar';
import 'leaflet/dist/leaflet.css';
import dynamic from "next/dynamic";
import { FairPoint } from '../../components/map';

const RevucaMap = dynamic(() => import("../../components/map"), { ssr: false });


export default function MyFair() {
  const [coords, setCoords] = React.useState<FairPoint[]>([]);

  // FIXME: fairData is hardcoded and should be fetched from the backend
  //        also change date format and take it from fairs list page
  const fairData = {
    name: 'zimny revucky jarmok 2024',
    status: 'prihlaseny',
    date: '15.11.2024 - 17.11.2024',
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
          <h1 className="font-bold text-[48px]">Moj jarmok</h1>
          <div className="
            flex flex-col gap-[20px]
            bg-[#eeeeee] rounded-[20px]
            w-full p-[20px]
          ">
            <div
              className="
                flex justify-between
                w-full
            ">
              <div className='flex gap-[10px] items-center'>
                <p className='text-[24px]'>{fairData.name}</p>
                <p className='text-[#67B64C] text-[18px]'>{fairData.status}</p>
              </div>
              <p className='text-[18px] text-[#606060]'>{fairData.date}</p>
            </div>
            <RevucaMap fairName="f" coords={coords} setCoords={setCoords}/>
          </div>
        </div>
      </div>
    </div>
  )
}
