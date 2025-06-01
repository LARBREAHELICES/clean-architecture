import { createFileRoute } from '@tanstack/react-router'

import CalendarPage  from '@/pages/plannings/CalendarPage'

export const Route = createFileRoute('/_authenticated/agenda')({
  component: RouteComponent,
})

function RouteComponent() {
  return (
    <CalendarPage />
  )
    
}
