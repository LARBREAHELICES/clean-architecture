import {create} from "zustand"

const apiUrl = import.meta.env.VITE_API_URL

type CertificationTotal = {
  total_hours: number;
  total_students: number;
  group_count: number;
}

type TotalsByCertification = {
  certifying: CertificationTotal;
  not_certifying: CertificationTotal;
  number_of_teachers: number;
}

type TotalsState = {
  total: TotalsByCertification | null;
  loading: boolean;
  error: string | null;
  fetchTotals: () => Promise<void>;
}

export const useTotalsStore = create<TotalsState>((set) => ({
  total: null,
  loading: false,
  error: null,
  fetchTotal: async () => {
    set({ loading: true, error: null });
    try {
      const res = await fetch(`${apiUrl}/reporting-summary/totals-by-certification`);
      if (!res.ok) throw new Error(`Erreur ${res.status}`);
      const data: TotalsByCertification = await res.json();
      set({ total: data, loading: false });
    } catch (e: any) {
      set({ error: e.message || "Erreur inconnue", loading: false });
    }
  },
}));
