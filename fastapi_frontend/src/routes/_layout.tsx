import { createFileRoute, Outlet, redirect } from '@tanstack/react-router'
import { isLoggedIn } from "@/hooks/useAuth"

export const Route = createFileRoute('/_layout')({
  component: Layout,
  beforeLoad: async () => {
    if(!isLoggedIn()) {
      throw redirect({ to: '/login' })
    }
  }
})

function Layout() {
  return (
     <main className="flex-1 p-6 md:p-8">
          <div className="mx-auto max-w-7xl">
            <Outlet />
          </div>
        </main>
  )
}

export default Layout
