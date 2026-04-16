<script setup lang="ts">
import { withBase } from 'vitepress'
import { data as logs } from '../logs.data'

const props = withDefaults(defineProps<{ limit?: number }>(), {
  limit: 3
})

const toSlashUrl = (url: string) => (url.endsWith('/') ? url : `${url}/`)
</script>

<template>
  <div class="recent-logs">
    <article v-for="log in logs.slice(0, props.limit)" :key="log.url" class="recent-log">
      <a :href="withBase(toSlashUrl(log.url))">{{ log.title }}</a>
      <span v-if="log.date">{{ log.date }}</span>
      <p v-if="log.summary">{{ log.summary }}</p>
    </article>
  </div>
</template>
