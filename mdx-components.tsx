import { useMDXComponents as getDocsThemeComponents } from 'nextra-theme-docs'

const docsThemeComponents = getDocsThemeComponents()

export function useMDXComponents(components?: Record<string, React.FC>) {
  return {
    ...docsThemeComponents,
    ...components
  }
}
