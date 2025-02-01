'use client';

import { useRouter } from 'next/router';
import React, { useEffect, useState } from 'react';
import { NextRouter } from 'next/router';
import { getUserData } from 'serverutils';

interface MenuOptionProps {
    icon?: React.ReactNode;
    text: string;
    route: string;
    router: NextRouter;
}

function MenuOption({ icon = null, route, router, text } : MenuOptionProps) {
  const currentRoute = router.pathname;
  const isActive =  route === currentRoute;
  return (
    <div
      onClick={() => router.push(route)}
      className={" \
        flex items-start gap-[10px] \
        px-[30px] py-[10px] w-full rounded-[10px] \
        cursor-pointer \
      " + (isActive ? ' bg-[#E8C871]' : 'hover:bg-[#E8C871] hover:bg-opacity-[0.5]')}
    >
      {icon}
      <p className="text-[24px]">{text}</p>
    </div>
  )
}

export default function Sidebar() {
  const router = useRouter();
  const [username, setUsername] = useState("");

  useEffect(() => {
    console.log(localStorage.getItem("token"))
    getUserData(localStorage.getItem("token"))
      .then((data) => {
        console.log(data);
        try {
          setUsername(data.split("@")[0]);
        } catch (e) {
          console.error(e);
          window.location.href = "/login";
        }
      });
  }, []);

  const routes = [
    { route: "/user/fairs", text: "Jarmoky" },
    { route: "/user/reservationRules", text: "Rezervacne pokyny" },
    { route: "/user/organizationRules", text: "Organizacne pokyny" },
    { route: "/user/myFair", text: "Moj jarmok" },
    { route: "/user/payments", text: "Moje platby" },
    { route: "/user/profile", text: "Profil" }
  ]

  return (
    <div className="
      w-[450px] h-screen
      bg-[#eeeeee]
      flex flex-col gap-[25px]
      px-[20px] pt-[150px]
      rounded-[0px_20px_20px_0px]
    ">
        <div className="flex items-center px-[30px] py-[20px] w-full justify-between">
          <h1 className="text-[36px] font-bold">Menu</h1>
          <p className='text-[18px] text-[goldenrod] font-bold'>{username}</p>
        </div>
        {routes.map((route, index) => (
          <MenuOption key={index} router={router} route={route.route} text={route.text} />
        ))}
    </div>
  )
}
