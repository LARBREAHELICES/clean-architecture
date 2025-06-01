// RouterProviderWithAuth.tsx
import { useAuthStore } from '@/stores/useAuthStore'
import { createRouter, RouterProvider } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'
import { CustomErrorPage } from '@/pages/CustomErrorPage'

export function RouterProviderWithAuth() {
  const user = useAuthStore((state) => state.user)
  const checkAuth = useAuthStore((state) => state.checkAuth)
  const logout = useAuthStore((state) => state.logout)

  const router = createRouter({
    routeTree,
    defaultNotFoundComponent: () => <CustomErrorPage />,
    context: {
      authentication: {
        user,
        checkAuth,
        logout,
      },
    },
  })

  return <RouterProvider router={router} />
}
