import { createContentLoader } from 'vitepress'

export type LocalPanelItem = {
  title: string
  url: string
  date?: string
  summary?: string
  paperSlug?: string
  source?: string
}

function dateValue(dateLike: unknown): number {
  if (!dateLike) return 0
  const d = new Date(String(dateLike))
  const t = d.getTime()
  return Number.isFinite(t) ? t : 0
}

export default createContentLoader('papers/local/*.md', {
  excerpt: false,
  transform(raw): LocalPanelItem[] {
    return raw
      .filter((p) => p.url !== '/papers/local/')
      .sort((a, b) => dateValue(b.frontmatter?.date) - dateValue(a.frontmatter?.date))
      .map((p) => ({
        title: p.frontmatter?.title || p.title,
        url: p.url,
        date: p.frontmatter?.date,
        summary: p.frontmatter?.summary,
        paperSlug: p.frontmatter?.paper_slug ? String(p.frontmatter.paper_slug) : undefined,
        source: p.frontmatter?.source ? String(p.frontmatter.source) : undefined
      }))
  }
})
