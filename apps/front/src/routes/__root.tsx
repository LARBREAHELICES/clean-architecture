import { createRootRouteWithContext, Outlet, Link } from "@tanstack/react-router"
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'
import type { AuthContext } from '@/hooks/useAuth'
import { useAuthStore } from '@/stores/useAuthStore'
import {ThemeProvider} from "@/providers/theme-provider"
import { NavigationMenuMain } from '@/components/molecules/NavigationMenuMain'

import  DashboardLayout  from '@/components/templates/dashboard/DashboardLayout'

import { UserCircle } from 'lucide-react' 

type RootContext ={
    authentication : AuthContext
}

export const Route = createRootRouteWithContext<RootContext>()({

  component: () => {
    const { user, logout } = useAuthStore()

    return (
      <DashboardLayout>
          <Outlet />
          <TanStackRouterDevtools />
      </DashboardLayout>
    )
  },
})
