'use client';

import Button from "../components/button";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  return (
    <div className="
      font-sans h-screen w-full pt-[30px] pb-[200px]
      flex flex-col gap-[150px] justify-between
      bg-[url('/background.png')] bg-cover bg-top
    ">
      <div className="flex w-full justify-end gap-[20px] px-[50px]">
        <Button additionalClasses="text-[24px]" variant="primary" onClick={() => router.push('/register')}>sign up</Button>
        <Button additionalClasses="text-[24px]" variant="secondary" onClick={() => router.push('/login')}>sign in</Button>
      </div>
      <div className="flex flex-col items-center gap-[25px] text-gray-300 text-[28px]">
        <h1 className="text-[64px]/[75px] font-bold text-center shadow-xl text-white">Digitálny jarmočný portál<br/>mesta <span className="text-red-600">Revuca</span></h1>
        <p>some text for dummies</p>
      </div>
    </div>
  );
}
