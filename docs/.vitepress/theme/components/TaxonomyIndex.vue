<script setup lang="ts">
import { withBase } from 'vitepress'
import { data as posts } from '../posts.data'
import { computed } from 'vue'

type TaxType = 'tags' | 'categories'

const props = defineProps<{ type: TaxType }>()

const items = computed(() => {
  const map = new Map<string, { slug: string; label: string; count: number }>()

  for (const p of posts) {
    for (const item of p[props.type]) {
      const existing = map.get(item.slug)
      if (existing) existing.count += 1
      else map.set(item.slug, { slug: item.slug, label: item.label, count: 1 })
    }
  }

  return Array.from(map.values()).sort((a, b) => b.count - a.count || a.slug.localeCompare(b.slug))
})
</script>

<template>
  <div>
    <ul>
      <li v-for="item in items" :key="item.slug">
        <a :href="withBase(`/${props.type}/${item.slug}/`)" >{{ item.label }}</a>
        <span style="margin-left: 8px; opacity: 0.7">({{ item.count }})</span>
      </li>
    </ul>
  </div>
</template>
