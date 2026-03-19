import { createFileRoute, redirect } from '@tanstack/react-router'

import { isLoggedIn } from '../hook/useAuth'
import { Login } from '../components/Admin/Login'


export const loginRoute = createFileRoute('/login') ({
  component: Login,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      throw redirect({ to: '/' })
    } 
  } ,
  head:()=>({

     meta: [
      {
        title: "Log In - FastAPI Template",
      },
    ],
  })

})


