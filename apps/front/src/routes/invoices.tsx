import { createFileRoute } from '@tanstack/react-router'

import  InvoiceTablePage  from '@/pages/InvoiceTablePage'

export const Route = createFileRoute('/invoices')({
  component: RouteComponent,
})

function RouteComponent() {
  return <InvoiceTablePage />
}
