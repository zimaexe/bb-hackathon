'use client';

import React, { useEffect, useState } from 'react';
import '../../app/globals.css';
import Sidebar from '../../components/sidebar';
import { UUID } from 'crypto';
import { NextRouter, useRouter } from 'next/router';

class FairType {
  name: string;
  dates: { from: string; to: string; };
  id: UUID;

  constructor(
    eventName: string,
    eventDates: { from: string; to: string; },
    eventID: UUID
  ) {
    this.name = eventName;
    this.dates = eventDates;
    this.id = eventID;
  }

  from() { return this.dates.from; }

  to() { return this.dates.to; }

  deadline() {
    const threeWeeks = 1000 * 60 * 60 * 24 * 21;
    return new Date(new Date(this.to()).getTime() - threeWeeks);
  }
};

interface FairProps {
  event: FairType;
  router: NextRouter;
}

function Fair({ event, router } : FairProps) {
  const fromDate = new Date(event.from());
  const toDate = new Date(event.to());
  const months = [
    'januára', 'februára', 'marca', 'apríla', 'mája', 'júna',
    'júla', 'augusta', 'septembra', 'októbra', 'novembra', 'decembra'
  ];

  const deadline = event.deadline();
  const deadlineText = `registrácia do ${deadline.getDate()} ${months[deadline.getMonth()]} ${deadline.getFullYear()}`;

  const eventDatesText = fromDate.getMonth() === toDate.getMonth()
    ? `${fromDate.getDate()} - ${toDate.getDate()} ${months[fromDate.getMonth()]} ${fromDate.getFullYear()}`
    : `${fromDate.getDate()} ${fromDate.getMonth() + 1} - ${toDate.getDate()} ${toDate.getMonth() + 1} ${toDate.getFullYear()}`;

  return (
    <div
      className="
        bg-[#D9D9D9] shadow-[0px_4px_4px_rgba(0,0,0,0.25)]
        flex justify-between
        cursor-pointer hover:bg-opacity-[0.5]
        px-[20px] py-[20px] rounded-[20px_0px_20px_20px] w-full"
      onClick={() => router.push(`/user/fairs?eventID=${event.id}`)}
    >
      <p className='text-[24px]'>{event.name}</p>
      <div className='flex flex-col gap-[10px] items-end text-[18px]'>
        <p className='text-[#606060]'>{eventDatesText}</p>
        <p className='text-[#D36262]'>{deadlineText}</p>
      </div>
    </div>
  )
}

function FairList({ events, router } : { events: FairType[], router: NextRouter }) {
  return (
    <>
      <h1 className="font-bold text-[48px]">Aktualne jarmoky</h1>
      <div className="flex flex-col gap-[30px] w-full">
        {events.map((event, index) => (<Fair key={index} router={router} event={event} />))}
      </div>
    </>
  )
}

function FairDetail({ events, eventID } : { events: FairType[], eventID: string }) {
  return (
    <>
      <h1 className="font-bold text-[48px]">Detail jarmoku</h1>
      <div className="
        flex flex-col gap-[30px]
        w-full
      ">
        <p>eventID: {eventID}</p>
        <p>nazov: {events.filter((event) => event.id === eventID)[0]?.name}</p>
      </div>
    </>
  )
}

async function getFairs() {
  const fairsList: FairType[] = [];
  const endpoint = "http://192.168.1.85:1488";

  await fetch(`${endpoint}/get_all_active_fairs`, {
    method: "GET",
    headers: {
      "content-type": "application/json"
    }
  })
  .then((res) => {
    console.log("Response", res)
    return res.json()
  })
  .then((fairs) => {
    console.log("Fairs", fairs)
    fairs.forEach(({ name, start_day, end_day, id } : { name: string, start_day: string, end_day: string, id: UUID }) => {
      fairsList.push(new FairType(
        name,
        {
          from: new Date(start_day).toISOString(),
          to: new Date(end_day).toISOString()
        },
        id
      ));
    });
  })
  .catch((err) => {
    console.log("Error", err)
  });

  return fairsList;
}

export default function Fairs() {
  const router = useRouter();
  
  const [events, setEvents] = useState<FairType[]>([]);

  useEffect(() => {
    getFairs().then((fairs) => {
      setEvents(fairs);
    });
  }, []);
  
  const eventID = router.query.eventID as string;

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
          {eventID && <FairDetail events={events} eventID={eventID} />}
          {!eventID && <FairList events={events} router={router} />}
        </div>
      </div>
    </div>
  );
}
