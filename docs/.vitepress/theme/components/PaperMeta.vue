<script setup lang="ts">
import { useData } from 'vitepress'

const { frontmatter } = useData()

const asArray = (value: unknown): string[] => {
  if (!value) return []
  if (Array.isArray(value)) return value.map(String).filter(Boolean)
  return [String(value)].filter(Boolean)
}
</script>

<template>
  <div class="paper-meta-panel">
    <div class="paper-meta-grid">
      <div v-if="frontmatter.year || frontmatter.venue">
        <strong>来源</strong>
        <span>{{ [frontmatter.venue, frontmatter.year].filter(Boolean).join(' · ') }}</span>
      </div>
      <div v-if="frontmatter.reading_status">
        <strong>阅读状态</strong>
        <span>{{ frontmatter.reading_status }}</span>
      </div>
      <div v-if="asArray(frontmatter.authors).length">
        <strong>作者</strong>
        <span>{{ asArray(frontmatter.authors).join(', ') }}</span>
      </div>
      <div v-if="asArray(frontmatter.institutions).length">
        <strong>机构</strong>
        <span>{{ asArray(frontmatter.institutions).join(' / ') }}</span>
      </div>
    </div>
    <div class="paper-link-row">
      <a v-if="frontmatter.source" :href="String(frontmatter.source)" target="_blank" rel="noreferrer">原文</a>
    </div>
  </div>
</template>
