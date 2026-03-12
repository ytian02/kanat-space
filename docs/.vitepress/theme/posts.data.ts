import { createContentLoader } from 'vitepress'

type TaxItem = { slug: string; label: string }

export type PostItem = {
  title: string
  url: string
  date?: string
  tags: TaxItem[]
  categories: TaxItem[]
}

function asStringArray(v: unknown): string[] {
  if (!v) return []
  if (Array.isArray(v)) return v.map(String).filter(Boolean)
  return [String(v)].filter(Boolean)
}

function slugify(input: string): string {
  return input
    .trim()
    .toLowerCase()
    .replace(/[_\s]+/g, '-')
    .replace(/[^\p{L}\p{N}\-\u4E00-\u9FFF]+/gu, '')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
}

function toTaxItems(values: unknown): TaxItem[] {
  const seen = new Set<string>()
  const items: TaxItem[] = []

  for (const label of asStringArray(values)) {
    const slug = slugify(label)
    if (!slug || seen.has(slug)) continue
    seen.add(slug)
    items.push({ slug, label })
  }

  return items
}

function dateValue(dateLike: unknown): number {
  if (!dateLike) return 0
  const d = new Date(String(dateLike))
  const t = d.getTime()
  return Number.isFinite(t) ? t : 0
}

export default createContentLoader('posts/*.md', {
  excerpt: false,
  transform(raw): PostItem[] {
    return raw
      .filter((p) => p.url !== '/posts/')
      .filter((p) => !p.frontmatter?.draft)
      .sort((a, b) => dateValue(b.frontmatter?.date) - dateValue(a.frontmatter?.date))
      .map((p) => ({
        title: p.frontmatter?.title || p.title,
        url: p.url,
        date: p.frontmatter?.date,
        tags: toTaxItems(p.frontmatter?.tags),
        categories: toTaxItems(p.frontmatter?.categories)
      }))
  }
})
