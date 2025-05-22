// atoms/InputText.tsx
import React from "react"

interface InputTextProps {
  label: string;
  value: string;
  onChange: (v: string) => void
}

export const InputText: React.FC<InputTextProps> = ({ label, value, onChange }) => (
  <label>
    {label}
    <input type="text" value={value} onChange={e => onChange(e.target.value)} />
  </label>
)
