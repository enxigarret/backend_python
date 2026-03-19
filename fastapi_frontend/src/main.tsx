import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'


import { ThemeProvider } from './components/theme-provider'
import { createRouter, RouterProvider } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'
import { MutationCache, QueryCache, QueryClient, QueryClientProvider } from '@tanstack/react-query'

const router = createRouter({routeTree})
declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router
  }
}
const queryClient = new QueryClient({
  queryCache:new QueryCache({
    onError: (error) => {
      console.error('Query error:', error)
    }}),
    mutationCache: new MutationCache({
      onError: (error) => {
        console.error('Mutation error:', error)
      },
  })
}
)




createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
     
      </QueryClientProvider>
    </ThemeProvider>

  </StrictMode>,
)
