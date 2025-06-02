import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import  RouterProviderWithAuth  from './router'

import { AuthProvider } from './hooks/AuthProvider'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
      <AuthProvider>
          <RouterProviderWithAuth />
      </AuthProvider>
  </StrictMode>,
)
