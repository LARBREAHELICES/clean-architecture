import  Layout  from "@/components/templates/Layout"
import {ThemeProvider} from "@/providers/theme-provider"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return  (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <Layout>{children}</Layout>
    </ThemeProvider>
  )
}