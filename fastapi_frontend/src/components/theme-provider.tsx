import {  useState } from "react"
import { ThemeProviderContext, ThemeContextType  } from "./theme-context"




type ThemeProviderProps = {
  children: React.ReactNode
  defaultTheme?: ThemeContextType["theme"]
  storageKey?: string
}




export function ThemeProvider({
  children,
  defaultTheme = "light",
  storageKey = "theme",
}: ThemeProviderProps) {
  const [theme, setTheme] = useState<ThemeContextType["theme"]>(
    (localStorage.getItem(storageKey) as ThemeContextType["theme"]) || defaultTheme
  )

  const toggleTheme = () => {
    setTheme((prev) => {
      const newTheme = prev === "light" ? "dark" : "light"
      localStorage.setItem(storageKey, newTheme)
      document.documentElement.classList.toggle("dark")
      return newTheme
    })
  }
    return (
    <ThemeProviderContext.Provider value={{ theme, setTheme: toggleTheme as ThemeContextType["setTheme"], resolvedTheme: theme }}>
      {children}
    </ThemeProviderContext.Provider>
  )
}


