import { DashboardSidebar } from "@/components/organismes/dashboard/sidebars/DashboardSidebar"
import { TopNav } from "@/components/organismes/dashboard/menus/TopNav" 
import React from "react"
// This file defines the main layout for the application, including a sidebar and top navigation.

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen">
      <DashboardSidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <TopNav />
        <main className="flex-1 overflow-y-auto p-4">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}