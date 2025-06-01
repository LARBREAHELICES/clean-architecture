import { createFileRoute, redirect } from "@tanstack/react-router"
import DashboardPage from "@/pages/DashboardPage"

export const Route = createFileRoute("/_authenticated/dashboard")({
  beforeLoad: async ({ context }) => {
    await context.authentication?.checkAuth();
    const user = context.authentication?.user;
    if (!user) {
      throw redirect({ to: "/login" });
    }
  },
  component: DashboardPage,
});