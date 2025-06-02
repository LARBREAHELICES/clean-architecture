import { createRootRouteWithContext, Outlet } from "@tanstack/react-router"
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'
import { ThemeProvider } from "@/providers/theme-provider"
import { type RouterContext} from "../router"

export const Route = createRootRouteWithContext<RouterContext>()({

  component: () => {

    return (
      <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
          <Outlet />
        <TanStackRouterDevtools />
      </ThemeProvider>
    )
  },
})
