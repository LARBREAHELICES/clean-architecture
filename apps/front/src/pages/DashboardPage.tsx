// src/pages/dashboard/index.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

import { Overview } from "@/components/organismes/dashboard/statistics/overview";
import { RecentSales } from "@/components/organismes/dashboard/statistics/recent-sales";

export default function DashboardPage() {
  return (
    <div className="flex flex-col space-y-4 p-4">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader>
            <CardTitle>Total Revenue</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">$45,231.89</p>
            <p className="text-xs text-muted-foreground">+20.1% from last month</p>
          </CardContent>
        </Card>
        {/* Ajoute d'autres cartes similaires pour Subscriptions, Sales, etc. */}
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <Overview />
          </CardContent>
        </Card>
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Recent Sales</CardTitle>
          </CardHeader>
          <CardContent>
            <RecentSales />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
