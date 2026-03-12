<script setup lang="ts">
import { withBase } from 'vitepress'
import { data as posts } from '../posts.data'

const toSlashUrl = (url: string) => (url.endsWith('/') ? url : `${url}/`)
</script>

<template>
  <div>
    <ul>
      <li v-for="post in posts" :key="post.url">
        <a :href="withBase(toSlashUrl(post.url))">{{ post.title }}</a>
        <span v-if="post.date" style="margin-left: 8px; opacity: 0.7">{{ post.date }}</span>
        <div v-if="post.tags.length || post.categories.length" style="margin-top: 4px">
          <span v-if="post.categories.length" style="margin-right: 10px">
            <span style="opacity: 0.7">分类：</span>
            <a
              v-for="c in post.categories"
              :key="c.slug"
              :href="withBase(`/categories/${c.slug}/`)"
              style="margin-right: 6px"
            >
              {{ c.label }}
            </a>
          </span>
          <span v-if="post.tags.length">
            <span style="opacity: 0.7">标签：</span>
            <a
              v-for="t in post.tags"
              :key="t.slug"
              :href="withBase(`/tags/${t.slug}/`)"
              style="margin-right: 6px"
            >
              {{ t.label }}
            </a>
          </span>
        </div>
      </li>
    </ul>

    <div style="margin-top: 16px">
      <a :href="withBase('/posts/mermaid-test/')">Mermaid 渲染测试页</a>
    </div>
  </div>
</template>
