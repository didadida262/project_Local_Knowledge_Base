import React, { useState, useEffect } from 'react'
import { Search, MessageCircle, FileText, BarChart3, Sparkles, Zap } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import StatsCard from './components/StatsCard'
import SearchTab from './components/SearchTab'
import QATab from './components/QATab'
import DocumentsTab from './components/DocumentsTab'
import { getStats } from './services/api'

interface Stats {
  total_vectors: number
  total_documents: number
  unique_files: number
}

function App() {
  const [activeTab, setActiveTab] = useState<'search' | 'qa' | 'documents'>('search')
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)
  const [isDark, setIsDark] = useState(true)

  useEffect(() => {
    // 强制暗黑模式
    document.documentElement.classList.add('dark')
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const data = await getStats()
      setStats(data)
    } catch (error) {
      console.error('Failed to load stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const tabs = [
    { id: 'search', label: '智能搜索', icon: Search, color: 'from-blue-500 to-cyan-500' },
    { id: 'qa', label: 'AI问答', icon: MessageCircle, color: 'from-purple-500 to-pink-500' },
    { id: 'documents', label: '文档管理', icon: FileText, color: 'from-green-500 to-emerald-500' },
  ] as const

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 dark">
      {/* 背景装饰 */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-cyan-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>
        <div className="absolute top-40 left-1/2 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '4s' }}></div>
      </div>

      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative z-10 glass border-b border-white/10"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            <motion.div 
              className="flex items-center space-x-4"
              whileHover={{ scale: 1.05 }}
            >
              <div className="relative">
                <BarChart3 className="h-10 w-10 text-cyan-400 glow" />
                <Sparkles className="h-4 w-4 text-yellow-400 absolute -top-1 -right-1 animate-pulse" />
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                  本地向量知识库
                </h1>
                <p className="text-sm text-muted-foreground">AI驱动的智能文档检索系统</p>
              </div>
            </motion.div>
            
            <div className="flex items-center space-x-6">
              {stats && (
                <motion.div 
                  className="text-sm text-muted-foreground glass px-4 py-2 rounded-lg"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <div className="flex items-center space-x-2">
                    <Zap className="h-4 w-4 text-yellow-400" />
                    <span>向量: {stats.total_vectors.toLocaleString()}</span>
                    <span className="text-white/50">|</span>
                    <span>文档: {stats.unique_files}</span>
                  </div>
                </motion.div>
              )}
            </div>
          </div>
        </div>
      </motion.div>

      {/* Stats Card */}
      <AnimatePresence>
        {stats && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <StatsCard stats={stats} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Tabs */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="glass rounded-2xl p-2 mt-8">
          <nav className="flex space-x-2">
            {tabs.map((tab, index) => {
              const Icon = tab.icon
              const isActive = activeTab === tab.id
              return (
                <motion.button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`relative flex items-center py-4 px-6 rounded-xl font-medium text-sm transition-all duration-300 ${
                    isActive
                      ? 'text-white'
                      : 'text-muted-foreground hover:text-white'
                  }`}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  {isActive && (
                    <motion.div
                      className={`absolute inset-0 bg-gradient-to-r ${tab.color} rounded-xl`}
                      layoutId="activeTab"
                      initial={false}
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                    />
                  )}
                  <Icon className={`h-5 w-5 mr-3 relative z-10 ${isActive ? 'text-white' : ''}`} />
                  <span className="relative z-10">{tab.label}</span>
                </motion.button>
              )
            })}
          </nav>
        </div>

        {/* Tab Content */}
        <motion.div 
          className="mt-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              {activeTab === 'search' && <SearchTab />}
              {activeTab === 'qa' && <QATab />}
              {activeTab === 'documents' && <DocumentsTab onUpload={loadStats} />}
            </motion.div>
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  )
}

export default App