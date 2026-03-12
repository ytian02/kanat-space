import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'

import 'katex/dist/katex.min.css'

import Layout from './Layout.vue'
import PostsList from './components/PostsList.vue'
import TaxonomyIndex from './components/TaxonomyIndex.vue'
import TaxonomyPage from './components/TaxonomyPage.vue'

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    app.component('PostsList', PostsList)
    app.component('TaxonomyIndex', TaxonomyIndex)
    app.component('TaxonomyPage', TaxonomyPage)
  }
} satisfies Theme
