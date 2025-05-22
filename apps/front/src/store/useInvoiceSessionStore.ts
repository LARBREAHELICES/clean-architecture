import { create } from "zustand"
import { persist } from "zustand/middleware"

type InvoiceForm = {
  invoice_name: number;
  school_name: string;
  class_name: string;
  nb_hours: number;
  nb_students: number;
  teacher_name: string;
  is_certifying: boolean | null;
};

type InvoiceFormStore = {
  form: InvoiceForm;
  setFormField: (field: keyof InvoiceForm, value: any) => void;
  resetForm: () => void;
};

const emptyInvoiceForm: InvoiceForm = {
  invoice_name: 0,
  school_name: "",
  class_name: "",
  nb_hours: 1,
  nb_students: 1,
  teacher_name: "",
  is_certifying: null,
};

xport const useInvoiceSessionStore = create<InvoiceFormStore>()(
    persist(
      (set) => ({
        form: emptyInvoiceForm,
        setFormField: (field, value) =>
          set((state) => ({
            form: { ...state.form, [field]: value },
          })),
        resetForm: () => set({ form: emptyInvoiceForm }),
      }),
      {
        name: "invoice-form-session", // clé dans localStorage
        // tu peux ajouter serialize/deserialize si besoin
      }
    )
  );
