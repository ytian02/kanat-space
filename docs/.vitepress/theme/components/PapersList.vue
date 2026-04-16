<script setup lang="ts">
import { withBase } from 'vitepress'
import { data as papers } from '../papers.data'

const toSlashUrl = (url: string) => (url.endsWith('/') ? url : `${url}/`)
</script>

<template>
  <div v-if="papers.length" class="papers-list">
    <article v-for="paper in papers" :key="paper.url" class="paper-card">
      <div class="paper-card-header">
        <a class="paper-title" :href="withBase(toSlashUrl(paper.url))">{{ paper.title }}</a>
        <span v-if="paper.readingStatus" class="paper-status">{{ paper.readingStatus }}</span>
      </div>
      <div class="paper-meta-line">
        <span v-if="paper.year">{{ paper.year }}</span>
        <span v-if="paper.venue">{{ paper.venue }}</span>
        <span v-if="paper.authors.length">{{ paper.authors.join(', ') }}</span>
      </div>
      <p v-if="paper.summary" class="paper-summary">{{ paper.summary }}</p>
      <div v-if="paper.tags.length" class="paper-tags">
        <span v-for="tag in paper.tags" :key="tag">#{{ tag }}</span>
      </div>
      <div class="paper-links">
        <a v-if="paper.source" :href="paper.source" target="_blank" rel="noreferrer">来源</a>
        <a v-if="paper.pdf" :href="paper.pdf" target="_blank" rel="noreferrer">PDF</a>
        <a v-if="paper.arxiv" :href="paper.arxiv" target="_blank" rel="noreferrer">arXiv</a>
      </div>
    </article>
  </div>
  <div v-else class="paper-empty">
    目前还没有已发布的论文笔记。新的草稿会先放在 <code>docs/papers/drafts/</code> 中整理。
  </div>
</template>
