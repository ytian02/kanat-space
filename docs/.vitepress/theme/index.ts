import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'

import 'katex/dist/katex.min.css'
import './style.css'

import Layout from './Layout.vue'
import PostsList from './components/PostsList.vue'
import TaxonomyIndex from './components/TaxonomyIndex.vue'
import TaxonomyPage from './components/TaxonomyPage.vue'
import LogsList from './components/LogsList.vue'
import RecentLogs from './components/RecentLogs.vue'
import PapersList from './components/PapersList.vue'
import PaperMeta from './components/PaperMeta.vue'
import LocalPaperPanelsList from './components/LocalPaperPanelsList.vue'
import PaperWorkspace from './components/PaperWorkspace.vue'

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    app.component('PostsList', PostsList)
    app.component('TaxonomyIndex', TaxonomyIndex)
    app.component('TaxonomyPage', TaxonomyPage)
    app.component('LogsList', LogsList)
    app.component('RecentLogs', RecentLogs)
    app.component('PapersList', PapersList)
    app.component('PaperMeta', PaperMeta)
    app.component('LocalPaperPanelsList', LocalPaperPanelsList)
    app.component('PaperWorkspace', PaperWorkspace)
  }
} satisfies Theme
