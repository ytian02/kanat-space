import { createContentLoader } from 'vitepress'

export type LogItem = {
  title: string
  url: string
  date?: string
  summary?: string
  tags: string[]
}

function asStringArray(v: unknown): string[] {
  if (!v) return []
  if (Array.isArray(v)) return v.map(String).filter(Boolean)
  return [String(v)].filter(Boolean)
}

function dateValue(dateLike: unknown): number {
  if (!dateLike) return 0
  const d = new Date(String(dateLike))
  const t = d.getTime()
  return Number.isFinite(t) ? t : 0
}

export default createContentLoader('logs/*.md', {
  excerpt: false,
  transform(raw): LogItem[] {
    return raw
      .filter((p) => p.url !== '/logs/')
      .filter((p) => !p.frontmatter?.draft)
      .sort((a, b) => dateValue(b.frontmatter?.date) - dateValue(a.frontmatter?.date))
      .map((p) => ({
        title: p.frontmatter?.title || p.title,
        url: p.url,
        date: p.frontmatter?.date,
        summary: p.frontmatter?.summary,
        tags: asStringArray(p.frontmatter?.tags)
      }))
  }
})
