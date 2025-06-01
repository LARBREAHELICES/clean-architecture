import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { RouterProviderWithAuth } from './router'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProviderWithAuth />
  </StrictMode>,
)
