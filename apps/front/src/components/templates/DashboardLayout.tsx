// components/layouts/DashboardLayout.tsx

import { AppSidebar } from "@/components/organismes/dashboard/sidebars/AppSidebar"
import { SiteHeader } from "@/components/organismes/dashboard/hearders/SiteHeader"
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider
      style={{
        "--sidebar-width": "calc(var(--spacing) * 72)",
        "--header-height": "calc(var(--spacing) * 12)",
      }}
    >
      <AppSidebar variant="inset" />
      <SidebarInset>
        <SiteHeader />
        <main className="flex flex-col flex-1">{children}</main>
      </SidebarInset>
    </SidebarProvider>
  )
}
