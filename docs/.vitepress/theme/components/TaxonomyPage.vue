<script setup lang="ts">
import { withBase } from 'vitepress'
import { data as posts } from '../posts.data'
import { computed } from 'vue'

const toSlashUrl = (url: string) => (url.endsWith('/') ? url : `${url}/`)

type TaxType = 'tags' | 'categories'

const props = defineProps<{ type: TaxType; slug: string }>()

const title = computed(() => {
  for (const p of posts) {
    const hit = p[props.type].find((x) => x.slug === props.slug)
    if (hit) return hit.label
  }
  return props.slug
})

const filtered = computed(() =>
  posts.filter((p) => p[props.type].some((x) => x.slug === props.slug))
)
</script>

<template>
  <div>
    <h1 style="margin-top: 0">{{ title }}</h1>

    <ul>
      <li v-for="post in filtered" :key="post.url">
        <a :href="withBase(toSlashUrl(post.url))">{{ post.title }}</a>
        <span v-if="post.date" style="margin-left: 8px; opacity: 0.7">{{ post.date }}</span>
      </li>
    </ul>

    <div style="margin-top: 16px">
      <a :href="withBase(`/${props.type}/`)">返回{{ props.type === 'tags' ? '标签' : '分类' }}列表</a>
    </div>
  </div>
</template>
