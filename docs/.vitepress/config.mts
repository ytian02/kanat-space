import { defineConfig } from 'vitepress'
import { promises as fs } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

import texmath from 'markdown-it-texmath'
import katex from 'katex'

type SidebarItem = { text: string; link: string }

type SidebarGroup = {
  text: string
  collapsed?: boolean
  items: SidebarItem[]
}

function escapeHtml(html: string) {
  return html
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

function wrapH2Section(state: any, headingText: string, blockName: string, className: string) {
  const tokens = state.tokens
  const Token = state.Token

  let i = 0
  while (i < tokens.length) {
    const t = tokens[i]

    if (t.type === 'heading_open' && t.tag === 'h2') {
      const inline = tokens[i + 1]
      if (inline?.type === 'inline' && inline.content.trim() === headingText) {
        // Avoid double-wrapping (in case of multiple passes).
        const prev = tokens[i - 1]
        if (prev?.type === 'html_block' && typeof prev.content === 'string' && prev.content.includes(`data-block="${blockName}"`)) {
          i += 1
          continue
        }

        const open = new Token('html_block', '', 0)
        open.content = `<div class="${className}" data-block="${blockName}">\n`
        tokens.splice(i, 0, open)
        i += 1

        // Close before the next H1/H2 (so we don't accidentally wrap the whole document).
        let end = i + 1
        for (; end < tokens.length; end++) {
          const tt = tokens[end]
          if (tt.type === 'heading_open' && (tt.tag === 'h1' || tt.tag === 'h2')) break
        }

        const close = new Token('html_block', '', 0)
        close.content = `</div>\n`
        tokens.splice(end, 0, close)

        return
      }
    }

    i += 1
  }
}

function extractFrontmatterBlock(md: string): string {
  if (!md.startsWith('---')) return ''
  const end = md.indexOf('\n---', 3)
  if (end === -1) return ''
  return md.slice(0, end + '\n---'.length)
}

function parseFrontmatterTitle(frontmatterBlock: string): string {
  const m = frontmatterBlock.match(/^title:\s*(.+)\s*$/m)
  if (!m) return ''
  return m[1].trim().replace(/^['"]|['"]$/g, '')
}

function parseFrontmatterList(frontmatterBlock: string, key: string): string[] {
  const lines = frontmatterBlock.split(/\r?\n/)
  const idx = lines.findIndex((l) => new RegExp(`^${key}:\\s*$`).test(l.trim()))
  if (idx === -1) return []

  const items: string[] = []
  for (let i = idx + 1; i < lines.length; i++) {
    const raw = lines[i]
    if (!raw) break

    // Next key
    if (/^[A-Za-z0-9_\-]+:\s*/.test(raw) && !/^\s*-\s+/.test(raw)) break

    const m = raw.match(/^\s*-\s*(.+?)\s*$/)
    if (!m) continue

    const val = m[1].trim().replace(/^['"]|['"]$/g, '')
    if (val) items.push(val)
  }
  return items
}

async function walkHtmlFiles(dir: string, acc: string[] = []): Promise<string[]> {
  const entries = await fs.readdir(dir, { withFileTypes: true })
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name)
    if (entry.isDirectory()) {
      await walkHtmlFiles(fullPath, acc)
      continue
    }
    if (entry.isFile() && entry.name.endsWith('.html')) {
      acc.push(fullPath)
    }
  }
  return acc
}

async function createCleanUrlCopies(outDir: string) {
  const htmlFiles = await walkHtmlFiles(outDir)

  await Promise.all(
    htmlFiles.map(async (file) => {
      const base = path.basename(file)
      if (base === 'index.html' || base === '404.html') return

      const targetDir = file.slice(0, -'.html'.length)
      await fs.mkdir(targetDir, { recursive: true })
      await fs.copyFile(file, path.join(targetDir, 'index.html'))
    })
  )
}

async function buildSidebar(docsDir: string) {
  // Posts: group by first collection (fallback: 其他)
  const postsDir = path.join(docsDir, 'posts')
  const postEntries = await fs.readdir(postsDir, { withFileTypes: true })

  const groups = new Map<string, SidebarItem[]>()

  for (const entry of postEntries) {
    if (!entry.isFile() || !entry.name.endsWith('.md')) continue
    if (entry.name === 'index.md') continue

    const fileBase = entry.name.slice(0, -'.md'.length)
    const fullPath = path.join(postsDir, entry.name)
    const content = await fs.readFile(fullPath, 'utf8')
    const fm = extractFrontmatterBlock(content)

    const title = parseFrontmatterTitle(fm) || fileBase
    const collections = parseFrontmatterList(fm, 'collections')
    const group = collections[0] || '其他'

    const link = `/posts/${fileBase}`
    const item: SidebarItem = { text: title, link }

    const list = groups.get(group) ?? []
    list.push(item)
    groups.set(group, list)
  }

  const postsSidebar: SidebarGroup[] = [{ text: '文章', collapsed: false, items: [{ text: '全部文章', link: '/posts/' }] }]

  for (const [group, items] of Array.from(groups.entries()).sort(([a], [b]) => a.localeCompare(b))) {
    postsSidebar.push({ text: group, collapsed: true, items })
  }

  // Tags & Categories: list pages in sidebar
  async function buildTaxSidebar(dirName: 'tags' | 'categories', label: string): Promise<SidebarGroup[]> {
    const dir = path.join(docsDir, dirName)
    const entries = await fs.readdir(dir, { withFileTypes: true })

    const items: SidebarItem[] = []
    for (const entry of entries) {
      if (!entry.isFile() || !entry.name.endsWith('.md')) continue
      if (entry.name === 'index.md') continue

      const fileBase = entry.name.slice(0, -'.md'.length)
      const fullPath = path.join(dir, entry.name)
      const content = await fs.readFile(fullPath, 'utf8')
      const fm = extractFrontmatterBlock(content)
      const title = parseFrontmatterTitle(fm) || fileBase

      items.push({ text: title, link: `/${dirName}/${fileBase}` })
    }

    items.sort((a, b) => a.text.localeCompare(b.text))

    return [
      { text: label, collapsed: false, items: [{ text: `全部${label}`, link: `/${dirName}/` }] },
      { text: `${label}列表`, collapsed: true, items }
    ]
  }

  const tagsSidebar = await buildTaxSidebar('tags', '标签')
  const categoriesSidebar = await buildTaxSidebar('categories', '分类')

  return {
    '/posts/': postsSidebar,
    '/tags/': tagsSidebar,
    '/categories/': categoriesSidebar
  }
}

export default defineConfig(async () => {
  const docsDir = fileURLToPath(new URL('..', import.meta.url))
  const sidebar = await buildSidebar(docsDir)

  return {
    lang: 'zh-CN',
    title: 'Kanat Space',
    description: '',

    // Clear the old Hugo favicon (browser tab icon).
    // `data:,` is an empty favicon.
    head: [['link', { rel: 'icon', href: 'data:,' }]],

    // GitHub Pages 项目站点： https://<用户名>.github.io/<仓库名>/
    // 你的远程仓库是 ytian02/kanat-space，所以 base 应为 /kanat-space/
    base: '/kanat-space/',
    cleanUrls: true,

    buildEnd: async (siteConfig) => {
      if (!siteConfig.cleanUrls) return
      await createCleanUrlCopies(siteConfig.outDir)
    },

    themeConfig: {
      nav: [
        { text: '首页', link: '/' },
        { text: '文章', link: '/posts/' },
        { text: '分类', link: '/categories/' },
        { text: '标签', link: '/tags/' }
      ],

      sidebar,

      outline: {
        level: [2, 3],
        label: '本页目录'
      },

      search: {
        provider: 'local'
      },

      docFooter: {
        prev: '上一页',
        next: '下一页'
      },

      returnToTopLabel: '回到顶部',
      sidebarMenuLabel: '菜单',
      darkModeSwitchLabel: '主题',
      lightModeSwitchTitle: '切换到浅色模式',
      darkModeSwitchTitle: '切换到深色模式',

      socialLinks: [{ icon: 'github', link: 'https://github.com/ytian02/kanat-space' }],

      editLink: {
        pattern: 'https://github.com/ytian02/kanat-space/edit/main/docs/:path',
        text: '在 GitHub 上编辑此页'
      },

      footer: {
        message: '基于 VitePress 构建',
        copyright: '内容采用 CC BY-NC-SA 4.0 许可'
      }
    },

    markdown: {
      config(md) {
        const texmathPlugin: any = (texmath as any).default ?? texmath
        const katexEngine: any = (katex as any).default ?? katex

        const katexOptions = { throwOnError: false }

        md.use(texmathPlugin, {
          engine: katexEngine,
          delimiters: 'dollars',
          katexOptions
        })

        // markdown-it-texmath 默认会输出 <eq>/<eqn> 标签；在 Vue 模板里会被当作组件，SSR 时变成空注释节点。
        // 这里显式重写 renderer，直接输出 KaTeX 的 HTML。
        const renderTex = (content: string, displayMode: boolean) =>
          texmathPlugin.render(content, displayMode, { ...katexOptions })

        md.renderer.rules.math_inline = (tokens, idx) => renderTex(tokens[idx].content, false)
        // `$$...$$` 可能会出现在段落内（inline token）。不要输出 block-level 标签（如 <section>），否则会出现无效嵌套导致局部不显示。
        md.renderer.rules.math_inline_double = (tokens, idx) => renderTex(tokens[idx].content, true)

        md.renderer.rules.math_block = (tokens, idx) => `<section>${renderTex(tokens[idx].content, true)}</section>`
        md.renderer.rules.math_block_eqno = (tokens, idx) => {
          const eqno = (tokens[idx].info || '').trim()
          const body = renderTex(tokens[idx].content, true)
          return `<section class="eqno">${body}${eqno ? `<span>(${escapeHtml(eqno)})</span>` : ''}</section>`
        }

        const defaultFence = md.renderer.rules.fence
        md.renderer.rules.fence = (tokens, idx, options, env, self) => {
          const token = tokens[idx]
          const info = (token.info || '').trim()

          if (info === 'mermaid') {
            // build 会压缩 HTML 的空白；用 <pre> 保留换行，否则 Mermaid 会把多行语句挤成一行导致解析报错。
            return `<pre class="mermaid">${escapeHtml(token.content)}</pre>`
          }

          return defaultFence
            ? defaultFence(tokens, idx, options, env, self)
            : self.renderToken(tokens, idx, options)
        }

        // Render special top-of-post blocks (pure Markdown in source, styled via global CSS).
        md.core.ruler.after('block', 'wrap-post-special-sections', (state) => {
          wrapH2Section(state, 'AI 含量说明', 'ai-disclosure', 'post-block post-ai-disclosure')
          wrapH2Section(state, '本文概览', 'post-overview', 'post-block post-overview')
        })
      }
    }
  }
})
