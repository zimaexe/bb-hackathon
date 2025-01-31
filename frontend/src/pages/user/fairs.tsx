'use client';

import React from 'react';
import '../../app/globals.css';
import Sidebar from '../../components/sidebar';
import { UUID } from 'crypto';
import { NextRouter, useRouter } from 'next/router';

class EventType {
  eventName: string;
  eventDates: { from: string; to: string; };
  eventID: UUID;

  constructor(
    eventName: string,
    eventDates: { from: string; to: string; },
    eventID: UUID
  ) {
    this.eventName = eventName;
    this.eventDates = eventDates;
    this.eventID = eventID;
  }

  from() { return this.eventDates.from; }

  to() { return this.eventDates.to; }

  deadline() {
    const threeWeeks = 1000 * 60 * 60 * 24 * 21;
    return new Date(new Date(this.to()).getTime() - threeWeeks);
  }
};

interface EventProps {
  event: EventType;
  router: NextRouter;
}

function Event({ event, router } : EventProps) {
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
      onClick={() => router.push(`/user/fairs?eventID=${event.eventID}`)}
    >
      <p className='text-[24px]'>{event.eventName}</p>
      <div className='flex flex-col gap-[10px] items-end text-[18px]'>
        <p className='text-[#606060]'>{eventDatesText}</p>
        <p className='text-[#D36262]'>{deadlineText}</p>
      </div>
    </div>
  )
}

export default function Fairs() {
  const router = useRouter();

  const events: EventType[] = [
    new EventType(
      'zimny revucky jarmok 2024',
      {
        from: '2024-11-15',
        to: '2024-11-17'
      },
      'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'
    ),
    new EventType(
      'letny revucky jarmok 2024',
      {
        from: '2024-06-15',
        to: '2024-06-17'
      },
      'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12'
    )
  ];

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
          {eventID && (
            <>
              <h1 className="font-bold text-[48px]">Detail jarmoku</h1>
              <div className="
                flex flex-col gap-[30px]
                w-full
              ">
                <p>eventID: {eventID}</p>
                <p>nazov: {events.filter((event) => event.eventID === eventID)[0]?.eventName}</p>
              </div>
            </>
          )}
          {!eventID && (
            <>
              <h1 className="font-bold text-[48px]">Aktualne jarmoky</h1>
              <div className="
                flex flex-col gap-[30px]
                w-full
              ">
                {events.map((event, index) => (<Event key={index} router={router} event={event} />))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
