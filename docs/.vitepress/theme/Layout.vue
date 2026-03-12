<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import { nextTick, onMounted, watch } from 'vue'
import { useRoute } from 'vitepress'

const { Layout } = DefaultTheme

async function renderMermaid() {
  if (import.meta.env.SSR) return

  const nodes = Array.from(document.querySelectorAll<HTMLElement>('.mermaid')).filter(
    (el) => !el.dataset.mermaidRendered
  )
  if (nodes.length === 0) return

  const mermaidMod = await import('mermaid')
  const mermaid = mermaidMod.default

  mermaid.initialize({ startOnLoad: false })
  await mermaid.run({ nodes })

  for (const el of nodes) el.dataset.mermaidRendered = 'true'
}

const route = useRoute()

onMounted(async () => {
  await nextTick()
  await renderMermaid()
})

watch(
  () => route.path,
  async () => {
    await nextTick()
    await renderMermaid()
  }
)
</script>

<template>
  <Layout />
</template>
