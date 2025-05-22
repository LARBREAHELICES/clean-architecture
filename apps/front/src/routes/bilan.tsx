import { createFileRoute } from '@tanstack/react-router'

import  TotalsByCertificationPage  from '@/pages/TotalsByCertificationPage'

export const Route = createFileRoute('/bilan')({
  component: RouteComponent,
})

function RouteComponent() {
  return <TotalsByCertificationPage />
}
