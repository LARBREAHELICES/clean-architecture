import React, { useEffect } from "react"
import { useTotalsStore } from "@/store/useTotalsStore"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export default function TotalsByCertificationPage() {
  const { total, loading, error, fetchTotal } = useTotalsStore();

  useEffect(() => {
    fetchTotal();
  }, [fetchTotal]);

  if (loading) return <p className="text-center mt-8">Chargement...</p>;
  if (error) return (
    <div className="text-center mt-8 text-red-600">
      Erreur : {error}
      <div className="mt-4">
        <Button onClick={fetchTotal} variant="outline">Réessayer</Button>
      </div>
    </div>
  );
  if (!total) return null;

  const renderCard = (title: string, stats: typeof totals.certifying) => (
    <Card className="w-80">
      <CardContent>
        <h3 className="text-lg font-semibold mb-4">{title}</h3>
        <p><strong>Heures totales :</strong> {stats.total_hours}</p>
        <p><strong>Nombre d'étudiants :</strong> {stats.total_students}</p>
        <p><strong>Nombre de groupes :</strong> {stats.group_count}</p>
      </CardContent>
    </Card>
  );

  return (
    <div className="max-w-4xl mx-auto mt-10 flex justify-center gap-8">
      <Card className="w-80">
        <CardContent>
          <h2 className="text-xl font-semibold mb-4">Total Teachers</h2>
          <p><strong>Number teachers :</strong> {total.number_of_teachers}</p> 
        </CardContent>
      </Card>     
      {renderCard("Certifying", total.certifying)}
      {renderCard("Not Certifying", total.not_certifying)}
    </div>
  );
}
