import { createFileRoute, redirect } from '@tanstack/react-router'
import { LoginPage } from '@/pages/LoginPage'

export const Route = createFileRoute('/login')({
  beforeLoad: async ({ context }) => {
    // Si déjà authentifié, on redirige vers /dashboard
    await context.authentication?.checkAuth()
    const user = context.authentication?.user

    console.log('user', user)
    if (user) {
      throw redirect({ to: '/dashboard' })
    }
  },
  component: LoginPage,
})