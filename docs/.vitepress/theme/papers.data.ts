import { createContentLoader } from 'vitepress'

export type PaperItem = {
  title: string
  url: string
  date?: string
  summary?: string
  year?: string
  venue?: string
  readingStatus?: string
  tags: string[]
  authors: string[]
  institutions: string[]
  source?: string
  pdf?: string
  arxiv?: string
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

export default createContentLoader('papers/*.md', {
  excerpt: false,
  transform(raw): PaperItem[] {
    return raw
      .filter((p) => p.url !== '/papers/')
      .filter((p) => !p.frontmatter?.draft)
      .sort((a, b) => dateValue(b.frontmatter?.date) - dateValue(a.frontmatter?.date))
      .map((p) => ({
        title: p.frontmatter?.title || p.title,
        url: p.url,
        date: p.frontmatter?.date,
        summary: p.frontmatter?.summary,
        year: p.frontmatter?.year ? String(p.frontmatter.year) : undefined,
        venue: p.frontmatter?.venue ? String(p.frontmatter.venue) : undefined,
        readingStatus: p.frontmatter?.reading_status ? String(p.frontmatter.reading_status) : undefined,
        tags: asStringArray(p.frontmatter?.tags),
        authors: asStringArray(p.frontmatter?.authors),
        institutions: asStringArray(p.frontmatter?.institutions),
        source: p.frontmatter?.source ? String(p.frontmatter.source) : undefined,
        pdf: p.frontmatter?.pdf ? String(p.frontmatter.pdf) : undefined,
        arxiv: p.frontmatter?.arxiv ? String(p.frontmatter.arxiv) : undefined
      }))
  }
})
