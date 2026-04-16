<script setup lang="ts">
import { withBase } from 'vitepress'
import { data as panels } from '../local-panels.data'

const toSlashUrl = (url: string) => (url.endsWith('/') ? url : `${url}/`)
</script>

<template>
  <div v-if="panels.length" class="papers-list">
    <article v-for="panel in panels" :key="panel.url" class="paper-card">
      <div class="paper-card-header">
        <a class="paper-title" :href="withBase(toSlashUrl(panel.url))">{{ panel.title }}</a>
        <span v-if="panel.paperSlug" class="paper-status">local</span>
      </div>
      <div class="paper-meta-line">
        <span v-if="panel.date">{{ panel.date }}</span>
        <span v-if="panel.paperSlug">{{ panel.paperSlug }}</span>
      </div>
      <p v-if="panel.summary" class="paper-summary">{{ panel.summary }}</p>
      <div class="paper-links">
        <a v-if="panel.source" :href="panel.source" target="_blank" rel="noreferrer">原文入口</a>
      </div>
    </article>
  </div>
  <div v-else class="paper-empty">
    目前还没有本地共读面板。先运行 <code>paper_session.py prepare</code> 为某篇论文生成一份。
  </div>
</template>
