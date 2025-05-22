import { createFileRoute } from '@tanstack/react-router'

import '../index.css'
import  App  from '../App'

export const Route = createFileRoute('/')({
  component: Index,
})

function Index() {
  return (
    <div className="p-2">
        <App />
    </div>
  )
}