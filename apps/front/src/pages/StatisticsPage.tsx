import React, { useEffect } from "react";
import { useGroupedInvoices } from "@/store/useGroupedInvoices";
import { Card, CardContent } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";  // <-- import Button

export default function StatisticsPage() {
  const { groupedData, currentPage, itemsPerPage, setPage, fetchGroupedInvoices } = useGroupedInvoices();

  useEffect(() => {
    fetchGroupedInvoices();
  }, []);

  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const currentData = groupedData.slice(startIndex, endIndex)

  const totalPages = Math.ceil(groupedData.length / itemsPerPage)

  return (
    <Card className="mt-8 max-w-4xl mx-auto">
      <CardContent className="p-4">
         {/* Pagination */}
         <div className="flex justify-center gap-2 mt-4">
          <Button
            onClick={() => setPage(currentPage - 1)}
            disabled={currentPage === 1}
            variant="outline"
          >
            Précédent
          </Button>

          {[...Array(totalPages)].map((_, i) => {
            const pageNum = i + 1;
            return (
              <Button
                key={pageNum}
                onClick={() => setPage(pageNum)}
                variant={pageNum === currentPage ? "default" : "outline"}
              >
                {pageNum}
              </Button>
            );
          })}

          <Button
            onClick={() => setPage(currentPage + 1)}
            disabled={currentPage === totalPages}
            variant="outline"
          >
            Suivant
          </Button>
        </div>
        <h2 className="text-xl font-semibold mb-4">Invoices Summary</h2>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>School</TableHead>
              <TableHead>Class</TableHead>
              <TableHead className="text-right">Total Hours</TableHead>
              <TableHead className="text-right">Students</TableHead>
              <TableHead className="text-right">Number invoicies</TableHead>
              <TableHead className="text-right">Certifying</TableHead>

            </TableRow>
          </TableHeader>
          <TableBody>
            {currentData.map((item, index) => (
              <TableRow key={index}>
                <TableCell>{item.school_name}</TableCell>
                <TableCell>{item.class_name}</TableCell>
                <TableCell className="text-right">{item.total_hours}</TableCell>
                <TableCell className="text-right">{item.total_students}</TableCell>
                <TableCell className="text-right">{item.summary_count}</TableCell>
                <TableCell className="text-right">#</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        {/* Pagination */}
        <div className="flex justify-center gap-2 mt-4">
          <Button
            onClick={() => setPage(currentPage - 1)}
            disabled={currentPage === 1}
            variant="outline"
          >
            Précédent
          </Button>

          {[...Array(totalPages)].map((_, i) => {
            const pageNum = i + 1;
            return (
              <Button
                key={pageNum}
                onClick={() => setPage(pageNum)}
                variant={pageNum === currentPage ? "default" : "outline"}
              >
                {pageNum}
              </Button>
            );
          })}

          <Button
            onClick={() => setPage(currentPage + 1)}
            disabled={currentPage === totalPages}
            variant="outline"
          >
            Suivant
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
