import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { createBrowserRouter } from "@tanstack/router"
import { ThemeProvider } from './components/theme-provider'
import { createRouter, RouterProvider } from '@tanstack/react-router'


const router = createRouter({routeTree})
declare module Register {
  interface Register {
    router: typeof router
  }

}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
        <RouterProvider router={router} />
      <App />
    </ThemeProvider>

  </StrictMode>,
)
