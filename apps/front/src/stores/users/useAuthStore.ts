import { create } from "zustand"

export type Permission = {
  id: string;
  name: string;
};

export type Role = {
  id: string;
  name: string;
  permissions: Permission[];
};

export type User = {
  id: string
  username: string
  email: string
  role: {
    name: string | null;
    permissions: {
      name: string;
    }[];
  };// optionnel, si vous avez besoin de gérer les rôles
}

export type AuthState = {
  user: User | null
  accessToken: string | null
  error: string | null
  hasCheckedAuth: boolean
  isLoadingAuth: boolean // ← nouvelle clé pour gérer l'état de chargement
  login: (username: string, password: string) => Promise<boolean>
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
  refresh: () => Promise<boolean>
}

const apiUrl = import.meta.env.VITE_API_URL

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  accessToken: null,
  error: null,
  hasCheckedAuth: false,
  isLoadingAuth: true, // ← nouvelle clé

  login: async (username: string, password: string) => {
    try {
      const res = await fetch(`${apiUrl}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
        credentials: "include", // pour récupérer cookie refresh_token
      })

      if (!res.ok) throw new Error("Identifiants incorrects")
      const data = await res.json()

      // data.user doit être un objet { id, username, email }
      console.log(data)
      set({
        user: {
          id: data.user.id,
          username: data.user.username,
          email: data.user.email,
          role: data.user.role || null, // si vous gérez les rôles
        },
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
      set({ user: null, accessToken: null, error: null, hasCheckedAuth: false })
    } catch {
      set({ user: null, accessToken: null, error: "Erreur lors de la déconnexion", hasCheckedAuth: false })
    }
  },

  checkAuth: async () => {
    let accessToken = get().accessToken

    if (!accessToken) {
      const refreshed = await get().refresh()
      if (!refreshed) {
        set({ user: null, error: "Non authentifié" })
        return null
      }
      accessToken = get().accessToken
    }

    try {
      const res = await fetch(`${apiUrl}/auth/me`, {
        credentials: "include",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })

      if (!res.ok) {
        throw new Error("Unauthorized")
      }

      const data = await res.json()

      const userAuth = {
        id: data.id,
        username: data.username,
        email: data.email,
        role : data.role || null, // si vous gérez les rôles
      }

      set({
        user: userAuth,
        error: null,
        isLoadingAuth: false
      })

      return userAuth

    } catch (err) {
      console.error("Erreur dans checkAuth", err)
      set({
        user: null,
        accessToken: null,
        hasCheckedAuth: false,
        error: "Échec de l'authentification"
      })
    }
  },

  refresh: async () => {
    try {
      const res = await fetch(`${apiUrl}/auth/refresh`, {
        method: "POST",
        credentials: "include",
      })

      if (!res.ok) return false

      const data = await res.json() // data.access_token, data.user

      set({
        accessToken: data.access_token,
        user: {
          id: data.user.id,
          username: data.user.username,
          email: data.user.email,
        },
        error: null,
      })

      return true

    } catch (err) {
      set({ user: null, accessToken: null, error: "Échec du refresh", hasCheckedAuth: false })
      return false
    }
  },
}))
