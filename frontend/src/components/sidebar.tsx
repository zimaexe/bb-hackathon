'use client';

import { useRouter } from 'next/router';
import React from 'react';
import { NextRouter } from 'next/router';

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
    ">
        <div className="flex items-center px-[30px] py-[20px]">
            <h1 className="text-[36px] font-bold">Menu</h1>
        </div>
        {routes.map((route, index) => (
          <MenuOption key={index} router={router} route={route.route} text={route.text} />
        ))}
    </div>
  )
}
