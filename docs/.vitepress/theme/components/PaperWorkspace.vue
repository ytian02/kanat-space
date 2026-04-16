<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { withBase } from 'vitepress'

type KeyPage = {
  page: number
  label: string
  image: string
  prompt: string
}

type KeyFigure = {
  id: string
  image: string
  prompt: string
}

type ReadingMap = {
  summary?: string
  suggested_route?: string[]
  questions?: string[]
}

type WorkspaceData = {
  paperSlug: string
  title?: string
  source?: string
  pdf?: string
  arxiv?: string
  sourcePdf?: string
  draftNotePath?: string
  readingMap?: ReadingMap
  keyPages?: KeyPage[]
  keyFigures?: KeyFigure[]
  pageTextPath?: string
}

type PageTextItem = {
  page: number
  text: string
}

type NoteItem = {
  id: string
  type: 'page' | 'figure' | 'excerpt'
  target: string
  note: string
  excerpt?: string
}

const labels = {
  loading: '\u6b63\u5728\u52a0\u8f7d\u5171\u8bfb\u5de5\u4f5c\u53f0\u2026',
  source: '\u539f\u6587',
  localPdf: '\u672c\u5730 PDF\uff1a',
  draftPath: '\u8349\u7a3f\u8def\u5f84\uff1a',
  readingMap: '\u9605\u8bfb\u5730\u56fe',
  keyPages: '\u5173\u952e\u9875',
  keyFigures: '\u5173\u952e\u56fe\u8868',
  suggestedQuestions: '\u5efa\u8bae\u5148\u95ee\u7684\u95ee\u9898',
  currentPage: '\u5f53\u524d\u9875\u56fe',
  currentFigure: '\u5f53\u524d\u56fe\u8868\u533a\u57df',
  currentText: '\u5f53\u524d\u9875\u6587\u672c',
  noFigure: '\u5148\u4ece\u5de6\u4fa7\u9009\u62e9\u4e00\u4e2a\u5173\u952e\u56fe\u8868\u3002',
  captureSelection: '\u8bfb\u53d6\u5f53\u524d\u9009\u4e2d\u6587\u672c',
  selectionPrefix: '\u5f53\u524d\u9009\u4e2d\uff1a',
  notesTitle: '\u672c\u5730\u6279\u6ce8',
  noNotes: '\u8fd8\u6ca1\u6709\u6279\u6ce8\u3002\u53ef\u4ee5\u5148\u5bf9\u9875\u3001\u56fe\u8868\u6216\u6587\u672c\u6458\u5f55\u5199\u4e00\u6761\u3002',
  pendingTitle: '\u5f85\u540c\u6b65\u5230\u8349\u7a3f',
  pendingHint: '\u5148\u52fe\u9009\u9700\u8981\u6c89\u6dc0\u7684\u6279\u6ce8\uff0c\u518d\u590d\u5236\u4e0b\u9762\u7684\u6574\u7406\u7ed3\u679c\u4ea4\u7ed9\u6211\u5199\u56de\u8349\u7a3f\u3002',
  copySync: '\u590d\u5236\u540c\u6b65\u6458\u8981',
  copyChat: '\u590d\u5236\u804a\u5929\u6307\u4ee4',
  copyPagePrompt: '\u590d\u5236\u672c\u9875\u63d0\u95ee',
  copyFigurePrompt: '\u590d\u5236\u56fe\u8868\u63d0\u95ee',
  pagePlaceholder: '\u7ed9\u8fd9\u4e00\u9875\u5199\u4e00\u6761\u6279\u6ce8',
  figurePlaceholder: '\u7ed9\u8fd9\u4e2a\u56fe\u8868\u533a\u57df\u5199\u4e00\u6761\u6279\u6ce8',
  excerptPlaceholder: '\u7ed9\u8fd9\u6bb5\u6458\u5f55\u5199\u4e00\u6761\u6279\u6ce8',
  savePageNote: '\u4fdd\u5b58\u9875\u7ea7\u6279\u6ce8',
  saveFigureNote: '\u4fdd\u5b58\u533a\u57df\u6279\u6ce8',
  saveExcerptNote: '\u4fdd\u5b58\u6458\u5f55\u6279\u6ce8',
  excerptHint: '\u5728\u4e0b\u9762\u9009\u62e9\u4e00\u6bb5\u6587\u5b57\uff0c\u7136\u540e\u4e3a\u8fd9\u6bb5\u6458\u5f55\u5199\u6279\u6ce8\u3002',
  syncCommandPrefix: '\u628a\u4e0b\u9762\u8fd9\u4e9b\u5185\u5bb9\u5199\u56de\u8349\u7a3f\u7684\u201c\u8ba8\u8bba\u540e\u66f4\u65b0\u7684\u7406\u89e3\u201d\u533a\u5757\uff1a',
  noteLabel: '\u6279\u6ce8\uff1a',
  excerptLabel: '\u6458\u5f55\uff1a',
}

const props = defineProps<{
  paperSlug: string
}>()

const workspace = ref<WorkspaceData | null>(null)
const pageText = ref<PageTextItem[]>([])
const activePage = ref<number | null>(null)
const activeFigure = ref<string | null>(null)
const notes = ref<NoteItem[]>([])
const pendingIds = ref<string[]>([])
const pageNoteDraft = ref('')
const figureNoteDraft = ref('')
const excerptNoteDraft = ref('')
const selectedExcerpt = ref('')
const loading = ref(true)

const storageKey = computed(() => `paper-workspace:${props.paperSlug}`)

const currentPageData = computed(() => pageText.value.find((item) => item.page === activePage.value) || null)
const currentPageMeta = computed(() => workspace.value?.keyPages?.find((item) => item.page === activePage.value) || null)
const currentFigureMeta = computed(() => workspace.value?.keyFigures?.find((item) => item.id === activeFigure.value) || null)
const currentPageTarget = computed(() => (activePage.value ? `\u7b2c ${activePage.value} \u9875` : ''))

function restoreState() {
  const raw = localStorage.getItem(storageKey.value)
  if (!raw) return
  try {
    const parsed = JSON.parse(raw)
    activePage.value = parsed.activePage ?? activePage.value
    activeFigure.value = parsed.activeFigure ?? null
    notes.value = Array.isArray(parsed.notes) ? parsed.notes : []
    pendingIds.value = Array.isArray(parsed.pendingIds) ? parsed.pendingIds : []
  } catch {
    // Ignore corrupted local state.
  }
}

function persistState() {
  localStorage.setItem(
    storageKey.value,
    JSON.stringify({
      activePage: activePage.value,
      activeFigure: activeFigure.value,
      notes: notes.value,
      pendingIds: pendingIds.value,
    })
  )
}

async function loadWorkspace() {
  loading.value = true
  const workspaceUrl = withBase(`/papers/${props.paperSlug}/workspace-data.json`)
  const workspaceResp = await fetch(workspaceUrl)
  workspace.value = await workspaceResp.json()
  const textResp = await fetch(withBase(workspace.value?.pageTextPath || `/papers/${props.paperSlug}/page-text.json`))
  const textJson = await textResp.json()
  pageText.value = Array.isArray(textJson.pages) ? textJson.pages : []
  if (!activePage.value && workspace.value?.keyPages?.length) {
    activePage.value = workspace.value.keyPages[0].page
  }
  loading.value = false
}

function setActivePage(page: number) {
  activePage.value = page
}

function setActiveFigure(figureId: string) {
  activeFigure.value = figureId
}

function addPageNote() {
  if (!activePage.value || !pageNoteDraft.value.trim()) return
  notes.value.unshift({
    id: `page-${activePage.value}-${Date.now()}`,
    type: 'page',
    target: `\u7b2c ${activePage.value} \u9875`,
    note: pageNoteDraft.value.trim(),
  })
  pageNoteDraft.value = ''
}

function addFigureNote() {
  if (!activeFigure.value || !figureNoteDraft.value.trim()) return
  notes.value.unshift({
    id: `figure-${activeFigure.value}-${Date.now()}`,
    type: 'figure',
    target: activeFigure.value,
    note: figureNoteDraft.value.trim(),
  })
  figureNoteDraft.value = ''
}

function captureSelection() {
  const selection = window.getSelection()?.toString().trim() || ''
  selectedExcerpt.value = selection
}

function addExcerptNote() {
  if (!selectedExcerpt.value || !excerptNoteDraft.value.trim() || !activePage.value) return
  notes.value.unshift({
    id: `excerpt-${activePage.value}-${Date.now()}`,
    type: 'excerpt',
    target: `\u7b2c ${activePage.value} \u9875`,
    note: excerptNoteDraft.value.trim(),
    excerpt: selectedExcerpt.value,
  })
  excerptNoteDraft.value = ''
  selectedExcerpt.value = ''
}

function togglePending(id: string) {
  if (pendingIds.value.includes(id)) {
    pendingIds.value = pendingIds.value.filter((item) => item !== id)
  } else {
    pendingIds.value = [...pendingIds.value, id]
  }
}

const pendingNotes = computed(() => notes.value.filter((item) => pendingIds.value.includes(item.id)))

const syncPreview = computed(() => {
  if (!pendingNotes.value.length) return ''
  return pendingNotes.value
    .map((item) => {
      const excerptPart = item.excerpt ? `\n${labels.excerptLabel}${item.excerpt}` : ''
      return `- [${item.type}] ${item.target}\n${labels.noteLabel}${item.note}${excerptPart}`
    })
    .join('\n\n')
})

async function copyText(text: string) {
  if (!text) return
  await navigator.clipboard.writeText(text)
}

const promptForPage = computed(() => currentPageMeta.value?.prompt || '')
const promptForFigure = computed(() => currentFigureMeta.value?.prompt || '')

function escapeHtml(value: string) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

function escapeRegExp(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

const currentPageHtml = computed(() => {
  const text = currentPageData.value?.text || ''
  let html = escapeHtml(text)
  const excerpts = notes.value
    .filter((item) => item.type === 'excerpt' && item.target === currentPageTarget.value && item.excerpt)
    .map((item) => item.excerpt as string)
    .sort((a, b) => b.length - a.length)
  for (const excerpt of excerpts) {
    html = html.replace(new RegExp(escapeRegExp(escapeHtml(excerpt)), 'g'), `<mark>${escapeHtml(excerpt)}</mark>`)
  }
  return html.replace(/\n/g, '<br>')
})

watch([activePage, activeFigure, notes, pendingIds], persistState, { deep: true })

onMounted(async () => {
  restoreState()
  await loadWorkspace()
})
</script>

<template>
  <div class="paper-workspace">
    <div v-if="loading" class="paper-empty">{{ labels.loading }}</div>
    <template v-else-if="workspace">
      <section class="paper-reading-map">
        <h2>{{ workspace.title }}</h2>
        <p class="reading-note">{{ workspace.readingMap?.summary }}</p>
        <div class="reading-links">
          <a v-if="workspace.source" :href="workspace.source" target="_blank" rel="noreferrer">{{ labels.source }}</a>
        </div>
        <p class="reading-note">{{ labels.localPdf }}<code>{{ workspace.sourcePdf }}</code></p>
        <p class="reading-note">{{ labels.draftPath }}<code>{{ workspace.draftNotePath }}</code></p>
      </section>

      <section class="paper-workspace-grid">
        <aside class="paper-workspace-sidebar">
          <div class="paper-reading-map">
            <h3>{{ labels.readingMap }}</h3>
            <ol>
              <li v-for="item in workspace.readingMap?.suggested_route || []" :key="item">{{ item }}</li>
            </ol>
          </div>
          <div class="paper-reading-map">
            <h3>{{ labels.keyPages }}</h3>
            <button
              v-for="item in workspace.keyPages || []"
              :key="item.page"
              class="workspace-chip"
              :class="{ active: item.page === activePage }"
              type="button"
              @click="setActivePage(item.page)"
            >
              第 {{ item.page }} 页
            </button>
          </div>
          <div class="paper-reading-map">
            <h3>{{ labels.keyFigures }}</h3>
            <button
              v-for="item in workspace.keyFigures || []"
              :key="item.id"
              class="workspace-chip"
              :class="{ active: item.id === activeFigure }"
              type="button"
              @click="setActiveFigure(item.id)"
            >
              {{ item.id }}
            </button>
          </div>
          <div class="paper-reading-map">
            <h3>{{ labels.suggestedQuestions }}</h3>
            <ul>
              <li v-for="item in workspace.readingMap?.questions || []" :key="item">{{ item }}</li>
            </ul>
          </div>
        </aside>

        <main class="paper-workspace-main">
          <section class="paper-reading-map">
            <h3>{{ labels.currentPage }}</h3>
            <div v-if="currentPageMeta">
              <p class="reading-note">{{ currentPageMeta.label }}</p>
              <img :src="withBase(currentPageMeta.image)" :alt="`第 ${currentPageMeta.page} 页`">
              <div class="reading-links">
                <button type="button" class="workspace-action" @click="copyText(promptForPage)">{{ labels.copyPagePrompt }}</button>
              </div>
              <textarea v-model="pageNoteDraft" class="workspace-textarea" :placeholder="labels.pagePlaceholder"></textarea>
              <button type="button" class="workspace-action" @click="addPageNote">{{ labels.savePageNote }}</button>
            </div>
          </section>

          <section class="paper-reading-map">
            <h3>{{ labels.currentFigure }}</h3>
            <div v-if="currentFigureMeta">
              <img :src="withBase(currentFigureMeta.image)" :alt="currentFigureMeta.id">
              <div class="reading-links">
                <button type="button" class="workspace-action" @click="copyText(promptForFigure)">{{ labels.copyFigurePrompt }}</button>
              </div>
              <textarea v-model="figureNoteDraft" class="workspace-textarea" :placeholder="labels.figurePlaceholder"></textarea>
              <button type="button" class="workspace-action" @click="addFigureNote">{{ labels.saveFigureNote }}</button>
            </div>
            <p v-else class="reading-note">{{ labels.noFigure }}</p>
          </section>

          <section class="paper-reading-map">
            <h3>{{ labels.currentText }}</h3>
            <p class="reading-note">{{ labels.excerptHint }}</p>
            <div class="reading-links">
              <button type="button" class="workspace-action" @click="captureSelection">{{ labels.captureSelection }}</button>
            </div>
            <div class="workspace-selection" v-if="selectedExcerpt">
              <strong>{{ labels.selectionPrefix }}</strong>
              <p>{{ selectedExcerpt }}</p>
              <textarea v-model="excerptNoteDraft" class="workspace-textarea" :placeholder="labels.excerptPlaceholder"></textarea>
              <button type="button" class="workspace-action" @click="addExcerptNote">{{ labels.saveExcerptNote }}</button>
            </div>
            <article class="workspace-text" v-html="currentPageHtml"></article>
          </section>
        </main>

        <aside class="paper-workspace-sidebar">
          <section class="paper-reading-map">
            <h3>{{ labels.notesTitle }}</h3>
            <div v-if="notes.length" class="workspace-notes">
              <article v-for="item in notes" :key="item.id" class="workspace-note">
                <label class="workspace-note-toggle">
                  <input type="checkbox" :checked="pendingIds.includes(item.id)" @change="togglePending(item.id)">
                  <span>[{{ item.type }}] {{ item.target }}</span>
                </label>
                <p>{{ item.note }}</p>
                <blockquote v-if="item.excerpt">{{ item.excerpt }}</blockquote>
              </article>
            </div>
            <p v-else class="reading-note">{{ labels.noNotes }}</p>
          </section>

          <section class="paper-reading-map">
            <h3>{{ labels.pendingTitle }}</h3>
            <p class="reading-note">{{ labels.pendingHint }}</p>
            <textarea :value="syncPreview" class="workspace-textarea" readonly></textarea>
            <div class="reading-links">
              <button type="button" class="workspace-action" @click="copyText(syncPreview)">{{ labels.copySync }}</button>
              <button
                type="button"
                class="workspace-action"
                @click="copyText(`${labels.syncCommandPrefix}\n\n${syncPreview}`)"
              >
                {{ labels.copyChat }}
              </button>
            </div>
          </section>
        </aside>
      </section>
    </template>
  </div>
</template>
