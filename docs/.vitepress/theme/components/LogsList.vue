<script setup lang="ts">
import { withBase } from 'vitepress'
import { data as logs } from '../logs.data'

const toSlashUrl = (url: string) => (url.endsWith('/') ? url : `${url}/`)
</script>

<template>
  <div class="logs-list">
    <article v-for="log in logs" :key="log.url" class="log-card">
      <a class="log-title" :href="withBase(toSlashUrl(log.url))">{{ log.title }}</a>
      <div v-if="log.date" class="log-date">{{ log.date }}</div>
      <p v-if="log.summary" class="log-summary">{{ log.summary }}</p>
      <div v-if="log.tags.length" class="log-tags">
        <span v-for="tag in log.tags" :key="tag">#{{ tag }}</span>
      </div>
    </article>
  </div>
</template>
