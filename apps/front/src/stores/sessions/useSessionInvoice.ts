import { create } from 'zustand'
import { persist } from 'zustand/middleware'

type InvoiceSession = {
  invoice_name: number
  nb_hours: number
  nb_students: number
  school_name: string
  class_name: string
  teacher_name?: string
  billed_at?: string // stockée en string ISO
  is_certifying: boolean
}

interface InvoiceSessionStore {
  sessionData: Partial<InvoiceSession>
  updateSession: (data: Partial<InvoiceSession>) => void
  clearSession: () => void
}

export const useInvoiceSessionStore = create<InvoiceSessionStore>()(
  persist(
    (set) => ({
      sessionData: {},
      updateSession: (data) =>
        set((state) => ({
          sessionData: { ...state.sessionData, ...data },
        })),
      clearSession: () => {
        set({ sessionData: {} })
        localStorage.removeItem('invoice-session-storage')
    },
    }),
    {
      name: 'invoice-session-storage', // clé dans localStorage
    }
  )
)
