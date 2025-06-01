import { create } from "zustand";
import { devtools } from "zustand/middleware";

const apiUrl = import.meta.env.VITE_API_URL;

export type DataGrouped = {
  id?: string; // généré par FastAPI
  school_name?: string;
  class_name?: string;
  total_hours?: number;
  total_students?: number;
  summary_count?: number;
  is_certifying: boolean;
};

type GroupedInvoiceStore = {
  groupedData: DataGrouped[];
  current: DataGrouped;
  currentPage: number;
  itemsPerPage: number;
  setPage: (page: number) => void;
  setItemsPerPage: (items: number) => void;
  setCurrent: (partial: Partial<DataGrouped>) => void;
  fetchGroupedInvoices: () => Promise<void>;
};

const emptyInvoiceGrouped: DataGrouped = {
  school_name: "",
  class_name: "",
  total_hours: 0,
  total_students: 0,
  summary_count: 0,
  is_certifying: true
};

export const useGroupedInvoices = create<GroupedInvoiceStore>()(
  devtools((set, get) => ({
    groupedData: [],
    current: emptyInvoiceGrouped,
    currentPage: 1,
    itemsPerPage: 10,

    setPage: (page) => set({ currentPage: page }),
    setItemsPerPage: (items) => set({ itemsPerPage: items }),

    setCurrent: (partial) =>
      set((state) => ({
        current: { ...state.current, ...partial },
      })),

    fetchGroupedInvoices: async () => {
      try {
        const response = await fetch(`${apiUrl}/reporting-summary/regrouped`);
        if (!response.ok) {
          throw new Error(`Erreur API: ${response.statusText}`);
        }
        const invoices: DataGrouped[] = await response.json();
        set({ groupedData: invoices, currentPage: 1 });
      } catch (error) {
        console.error("Erreur lors du chargement des factures :", error);
      }
    },
  }))
);
