import { createFileRoute, redirect } from '@tanstack/react-router'

export const Route = createFileRoute('/_authenticated')({
  beforeLoad: async ({ context }) => {
    // 1. On exécute checkAuth (peut mettre à jour l’état user)
    await context.authentication?.checkAuth()

    // 2. On lit l’état après avoir vérifié
    const user = context.authentication?.user ?? null

    // 3. Si pas d’utilisateur, on redirige
    if (!user) {
      throw redirect({
        to: '/login',
      })
    }
  },
})
