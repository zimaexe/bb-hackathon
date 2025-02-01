'use client';

import React from "react";
import QRCode from "react-qr-code";
import '../../app/globals.css';
import Sidebar from '../../components/sidebar';
import { NextRouter, useRouter } from 'next/router';
import { UUID } from 'crypto';

class PaymentType {
  description: string;
  amount: number;
  status: string;
  date: string;
  id: UUID;

  statusColor: string;
  statusText: string;

  constructor(description: string, amount: number, status: string, date: string, id: UUID) {
    this.description = description;
    this.amount = amount;
    this.status = status;
    this.date = date;
    this.id = id;

    switch (this.status) {
      case 'paid': {
        this.statusColor = '#4E9014';
        this.statusText = 'zaplatené';
        break;
      }
      case 'unpaid': {
        this.statusColor = '#A32D2D';
        this.statusText = 'nezaplatené';
        break;
      }
      default: {
        this.statusColor = '#DA8B2A';
        this.statusText = 'spracovanie';
        break;
      }
    }
  }
};

interface PaymentProps {
  payment: PaymentType;
  router: NextRouter;
}

function Payment({ payment, router } : PaymentProps) {
  return (
    <div
      className="
        bg-[#D9D9D9] shadow-[0px_4px_4px_rgba(0,0,0,0.25)]
        flex justify-between
        cursor-pointer hover:bg-opacity-[0.5]
        px-[20px] py-[20px] rounded-[20px_0px_20px_20px] w-full"
      onClick={() => router.push(`/user/payments?paymentID=${payment.id}`)}
    >
      <div className='flex gap-[15px]'>
        <div 
          className={`w-[140px] py-[5px] flex font-bold shadow-[0px_2px_2px_rgba(0,0,0,0.25)] justify-center rounded-[10px] bg-[#BFBFBF]`}
          style={{ color: payment.statusColor }}
        >
          {payment.statusText}
        </div>
        <p className='text-[24px]'>{payment.description}</p>
        <p className='text-[24px] font-bold text-[#479327]'>{payment.amount}€</p>
      </div>
      <p className='text-[#606060]'>{payment.date}</p>
    </div>
  )
}

function PaymentList({ payments, router } : { payments: PaymentType[], router: NextRouter }) {
  return (
    <>
      <h1 className="font-bold text-[48px]">Moje platby</h1>
      <div className="flex flex-col gap-[30px] w-full">
        {payments.map((payment, index) => (<Payment key={index} router={router} payment={payment} />))}
      </div>
    </>
  )
}

function PaymentDetail({ payments, paymentID } : { payments: PaymentType[], paymentID: string }) {  
  return (
    <>
      <h1 className="font-bold text-[48px]">Detail platby</h1>
      <div className="
        flex flex-col gap-[30px]
        w-full
      ">
        <p>paymentID: {paymentID}</p>
        <p>nazov: {payments.filter((payment) => payment.id === paymentID)[0]?.description}</p>
        <QRCode value={`http://0.0.0.0:1488/get_reservation/${paymentID}`} />
      </div>
    </>
  )
}

export default function Payments() {
  const router = useRouter();

  const payments = [
    new PaymentType('Rezervácia stánku 4 metrov', 8, 'processing', '01.02.2025', 'a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5r'),
    new PaymentType('Rezervácia stánku 10 metrov', 20, 'paid', '12.12.2024', 'a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p'),
    new PaymentType('Rezervácia stánku 10 metrov', 20, 'unpaid', '12.10.2023', 'a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5q'),
  ];

  const paymentID = router.query.paymentID as string;

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
          {!paymentID && <PaymentList payments={payments} router={router} />}
          {paymentID && <PaymentDetail payments={payments} paymentID={paymentID} />}
        </div>
      </div>
    </div>
  )
}
