

import { createContext } from "react"




export type ThemeContextType = {
  theme: "light" | "dark" 
  resolvedTheme: "light" | "dark"
  setTheme: (theme: "light" | "dark" ) => void
}

type ThemeProviderState = {
  theme: ThemeContextType["theme"]
  resolvedTheme: "dark" | "light"
  setTheme: (theme: ThemeContextType["theme"]) => void
}

const initialState: ThemeProviderState = {
  theme: "light",
  resolvedTheme: "light",
  setTheme: () => {}
}


export const ThemeProviderContext = createContext<ThemeContextType | undefined>(initialState)