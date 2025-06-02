// routes/_authenticated.tsx
import { createFileRoute, redirect } from '@tanstack/react-router'

export const Route = createFileRoute('/_authenticated')({
  beforeLoad: async ({ context }) => {
    // Appelle la logique de vérification centrale
    const user = await context.authentication?.checkAuth()

    // Redirige si l'utilisateur n'est pas connecté
    if (!user) {
      throw redirect({ to: '/login' })
    }

    return { user } // Tu peux passer le user dans le loader si tu veux
  },
})