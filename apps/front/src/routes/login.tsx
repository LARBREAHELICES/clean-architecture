import LoginPage from '@/pages/registers/LoginPage'
import { createFileRoute, redirect } from '@tanstack/react-router'

export const Route = createFileRoute('/login')({
    beforeLoad: async ({ context }) => {
        const user = await context.authentication?.checkAuth()
        if (user) {
            return redirect({ to: '/dashboard' })
        }
        return { user }
    },
    component: RouteComponent,
})

function RouteComponent() {
    return <LoginPage />
}
