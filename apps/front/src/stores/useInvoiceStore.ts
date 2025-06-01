import { create } from "zustand";
import { devtools } from "zustand/middleware";

const apiUrl = import.meta.env.VITE_API_URL;

export type Invoice = {
  loading?: boolean;  // loading dans le store, pas dans chaque facture
  invoice_name: number;
  school_name?: string;
  class_name?: string;
  nb_hours?: number;
  nb_students?: number;
  teacher_name?: string;
  id?: string;          
  billed_at?: string;   
  created_at?: string;  
  is_certifying?: boolean | null;
};

type InvoiceStore = {
  data: Invoice[];
  current: Invoice;
  currentPage: number;
  itemsPerPage: number;
  setPage: (page: number) => void;
  setCurrent: (partial: Partial<Invoice>) => void;
  addInvoiceLocal: () => void;
  resetCurrent: () => void;
  createInvoiceOnApi: () => Promise<void>;
  fetchAllInvoices: () => Promise<void>;
  loading: boolean;
};

const emptyInvoice: Invoice = {
  invoice_name: 0,
  school_name: "",
  class_name: "",
  nb_hours: 1,
  nb_students: 1,
  billed_at: "",
  teacher_name: "",
  is_certifying: true,
};

export const useInvoiceStore = create<InvoiceStore>()(
  devtools(
    (set, get) => ({
      data: [],
      current: emptyInvoice,
      currentPage: 1,
      itemsPerPage: 20,
      loading: false,
      lastInvoice: "",

      setPage: (page) => set({ currentPage: page }),

      setCurrent: (partial) =>
        set((state) => ({
          current: { ...state.current, ...partial },
        })),

      addInvoiceLocal: () =>
        set((state) => ({
          data: [...state.data, state.current],
          current: emptyInvoice,
        })),

      resetCurrent: () => set({ current: emptyInvoice }),

      createInvoiceOnApi: async () => {
        const current = get().current;
        try {
          const response = await fetch(`${apiUrl}/reporting-summary`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(current),
          });

          if (!response.ok) {
            throw new Error(`Erreur API: ${response.statusText}`);
          }

          const saved = await response.json();

          set((state) => ({
            data: [...state.data, saved],
            current: emptyInvoice,
          }));
        } catch (error) {
          console.error("Erreur lors de la création de la facture :", error);
        }
      },

      fetchAllInvoices: async () => {
        set({ loading: true });
        try {
          const response = await fetch(`${apiUrl}/reporting-summary/all`);
          if (!response.ok) {
            throw new Error(`Erreur API: ${response.statusText}`);
          }
          const invoices = await response.json();
          set({ data: invoices, loading: false });
        } catch (error) {
          console.error("Erreur lors du chargement des factures :", error);
          set({ loading: false });
        }
      },

      fetchLastInvoice: async () => {  
        try {
          const response = await fetch(`${apiUrl}/reporting-summary/last-invoice-name`);
          if (!response.ok) {
            throw new Error(`Erreur API: ${response.statusText}`);
          }
          const lastInvoice = await response.json();
          set({ lastInvoice: lastInvoice });
        } catch (error) {
          console.error("Erreur lors du chargement de la dernière facture :", error);
        }
      }
    })
  )
);
