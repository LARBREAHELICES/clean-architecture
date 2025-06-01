import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

const sales = [
  {
    name: "Olivia Martin",
    email: "olivia.martin@example.com",
    amount: "$1,999.00",
  },
  {
    name: "Jackson Lee",
    email: "jackson.lee@example.com",
    amount: "$39.00",
  },
  // Ajoute d'autres ventes récentes ici
];

export function RecentSales() {
  return (
    <div className="space-y-8">
      {sales.map((sale, index) => (
        <div key={index} className="flex items-center">
          <Avatar className="h-9 w-9">
            <AvatarImage src="/avatars/placeholder.png" alt={sale.name} />
            <AvatarFallback>{sale.name.charAt(0)}</AvatarFallback>
          </Avatar>
          <div className="ml-4 space-y-1">
            <p className="text-sm font-medium leading-none">{sale.name}</p>
            <p className="text-sm text-muted-foreground">{sale.email}</p>
          </div>
          <div className="ml-auto font-medium">{sale.amount}</div>
        </div>
      ))}
    </div>
  );
}
