// components/top-nav.tsx
import { createRootRouteWithContext, Outlet, Link } from "@tanstack/react-router"

import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle
} from "@/components/ui/navigation-menu"

import { Menu,  UserCircle, LogOut, Sun, Moon } from "lucide-react"
import { useAuthStore } from '@/stores/useAuthStore'

import { useTheme } from "@/providers/theme-provider"

export function TopNav() {
  const { user, logout } = useAuthStore()
  const { theme, setTheme } = useTheme()

  return (
    <header className="sticky top-0 z-10 border-b bg-background">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">

          <Button variant="ghost" size="icon" className="md:hidden">
            <Menu className="h-5 w-5" />
          </Button>
          <h1 className="text-lg font-semibold">L'Arbre à Hélices</h1>
          <span>OF</span>
        </div>
        <NavigationMenu>
          <NavigationMenuList>
            <NavigationMenuItem>
              <NavigationMenuLink asChild className={navigationMenuTriggerStyle()}>
                <Link to="/" >
                  Home
                </Link>
              </NavigationMenuLink>
            </NavigationMenuItem>
            {user ? (
              <>
                <NavigationMenuItem>
                  <NavigationMenuLink asChild>
                    <Link to="/dashboard" className={navigationMenuTriggerStyle()}>
                      Dashboard
                    </Link>
                  </NavigationMenuLink>
                </NavigationMenuItem>
                <NavigationMenuItem >
                  <NavigationMenuLink asChild className={navigationMenuTriggerStyle()}>

                    <Link to="/agenda" >
                      Agenda
                    </Link>
                  </NavigationMenuLink>

                </NavigationMenuItem>
              </>) : (
              <NavigationMenuItem>
                <NavigationMenuLink asChild>
                  <Link to="/login" className={navigationMenuTriggerStyle()}>
                    Login
                  </Link>
                </NavigationMenuLink>
              </NavigationMenuItem>
            )}

          </NavigationMenuList>
        </NavigationMenu>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => {
              setTheme(theme == 'light' ? "dark" : "light")
            }}
          >
            {theme === "light" ? (
              <Moon className="h-4 w-4" />
            ) : (
              <Sun className="h-4 w-4" />
            )}
          </Button>
          {user && (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon">
                  <span>{user?.username ?? ''}</span>
                  <UserCircle className="w-4 h-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem>Profile</DropdownMenuItem>
                <DropdownMenuItem>Settings</DropdownMenuItem>
                <DropdownMenuItem
                  className="flex items-center gap-2 text-red-500 focus:text-red-500"
                  onClick={logout}
                >
                  <LogOut className="h-4 w-4" />
                  <span>Déconnexion</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          )}
        </div>
      </div>
    </header>
  )
}