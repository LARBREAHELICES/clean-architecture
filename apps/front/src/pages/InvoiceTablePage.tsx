import React, { useEffect } from "react"
import { useInvoiceStore } from "@/store/useInvoiceStore"
import { Card, CardContent } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"

export default function InvoiceTablePage() {
  const {
    loading,
    data,
    currentPage,
    itemsPerPage,
    setPage,
    fetchAllInvoices,
    current,
    setCurrent,
  } = useInvoiceStore()


  useEffect(() => {
    fetchAllInvoices();
  }, []);

  if (loading) {
    return <div>Chargement en cours...</div>
  }
  
  if (!loading && data.length === 0) {
    return <div>Aucune donnée disponible</div>
  }

const startIndex = (currentPage - 1) * itemsPerPage
const endIndex = startIndex + itemsPerPage
const currentData = data.slice(startIndex, endIndex)

const totalPages = Math.ceil(data.length / itemsPerPage)

  return (
    <Card className="mt-8 max-w-5xl mx-auto">
       <div className="flex justify-center gap-2 pt-4">
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
      <CardContent className="p-6 space-y-6">
        <h2 className="text-xl font-semibold">Invoices Summary</h2>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>School</TableHead>
              <TableHead>Class</TableHead>
              <TableHead className="text-right">Total Hours</TableHead>
              <TableHead className="text-right">Students</TableHead>
              <TableHead className="text-right">Invoices</TableHead>
              <TableHead className="text-right">Certifying</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {currentData.map((item, index) => (
              <TableRow key={index}>
                <TableCell>{item.school_name}</TableCell>
                <TableCell>{item.class_name}</TableCell>
                <TableCell className="text-right">{item.nb_hours}</TableCell>
                <TableCell className="text-right">{item.nb_students}</TableCell>
                <TableCell className="text-right">{item.invoice_name}</TableCell>
                <TableCell className="text-right">{item.is_certifying == true ? 'yes' : 'no'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        {/* Pagination */}
        <div className="flex justify-center gap-2 pt-4">
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
