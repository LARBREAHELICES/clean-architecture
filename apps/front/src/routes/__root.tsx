import { createRootRoute, Link, Outlet } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'

export const Route = createRootRoute({
  component: () => (
    <>
      <div className="p-2 flex gap-2">
        <Link to="/" className="[&.active]:font-bold">
          Home
        </Link>{' '}
        <Link to="/invoices" className="[&.active]:font-bold">
          Invoices
        </Link>{' '}
        <Link to="/statistic" className="[&.active]:font-bold">
          Statistics
        </Link>{' '}
        <Link to="/bilan" className="[&.active]:font-bold">
          Total
        </Link>{' '}
      </div>
      <hr />
      <Outlet />
      <TanStackRouterDevtools />
    </>
  ),
})