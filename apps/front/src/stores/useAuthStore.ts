import { create } from "zustand"

export type User = {
  id: string
  username: string
  email: string
}

export type AuthState = {
  user: User | null
  accessToken: string | null
  error: string | null
  login: (username: string, password: string) => Promise<void>
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
  refresh: () => Promise<boolean>
}

const apiUrl = import.meta.env.VITE_API_URL

let hasCheckedAuth = false

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  accessToken: null,
  error: null,

  login: async (username, password) => {
    try {
      const res = await fetch(`${apiUrl}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
        credentials: "include", // pour récupérer cookie refresh_token
      })

      if (!res.ok) throw new Error("Identifiants incorrects")
      const data = await res.json()

      set({
        user: { username: data.user, email: "", id: "" },
        accessToken: data.access_token,
        error: null,
      })
      return true

    } catch (err: any) {
      set({ error: err.message || "Erreur lors de la connexion" })

      return false
    }
  },

  logout: async () => {
    try {
      await fetch(`${apiUrl}/auth/logout`, {
        method: "POST",
        credentials: "include",
      })
      set({ user: null, accessToken: null, error: null })
    } catch {
      set({ user: null, accessToken: null, error: "Erreur lors de la déconnexion" })
    }
  },
  checkAuth: async () => {
    if( hasCheckedAuth ) {
      console.log("checkAuth déjà effectué, on ne refait pas")
      return;
    }
    hasCheckedAuth = true; // On marque que l'authentification a été vérifiée
    try {
      let { accessToken } = get()
  
      let res = await fetch(`${apiUrl}/auth/me`, {
        headers: {
          Authorization: `Bearer ${accessToken ?? ""}`,
        },
      })
  
      if (res.ok) {
        const data = await res.json();
        set({ user: data, error: null });
        return;
      }
  
      if (res.status === 401) {
        console.log("401, tentative de refresh")
        const refreshSuccess = await get().refresh()
  
        if (refreshSuccess) {
          accessToken = get().accessToken
          res = await fetch(`${apiUrl}/auth/me`, {
            headers: {
              Authorization: `Bearer ${accessToken ?? ""}`,
            },
          });
  
          if (res.ok) {
            const data = await res.json();
            set({ user: data, error: null });
            return;
          }
        }
  
        set({ user: null, accessToken: null });
      }
    } catch (err) {
      console.error("Erreur dans checkAuth", err);
      set({ user: null, accessToken: null });
    }
  }  
,  
  refresh: async () => {
    try {
      const res = await fetch(`${apiUrl}/auth/refresh`, {
        method: "POST",
        credentials: "include",
      });
  
      if (!res.ok) return false;
  
      const data = await res.json(); // data.access_token, data.user
  
      set({ accessToken: data.access_token, user: data.user, error: null });
  
      return true;
    } catch (err) {
      set({ user: null, accessToken: null, error: "Échec du refresh" });
      return false;
    }
  },
}))
