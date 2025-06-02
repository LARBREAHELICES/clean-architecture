// RouterProviderWithAuth.tsx
import { createRouter, RouterProvider } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'
import { useAuth } from '@/hooks/AuthProvider'
import { CustomErrorPage } from '@/pages/errors/CustomErrorPage'

export type RouterContext = {
  authentication: ReturnType<typeof useAuth>
}

// Register things for typesafety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}

const router = createRouter({
  routeTree,
  defaultNotFoundComponent: () => <CustomErrorPage />,
  context: {
    authentication: undefined!,
  },
})

export default function InnerApp() {
  const auth = useAuth()

  return <RouterProvider router={router} context={{ authentication : auth }} />
}

