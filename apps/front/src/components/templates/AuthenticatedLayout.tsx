

export function AuthenticatedLayout({ children }: { children: React.ReactNode }) {
    const { user } = useAuthStore()
  
    if (!user) return <div>Chargement de la session...</div>
  
    return <>{children}</>
  }
