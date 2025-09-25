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
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)' }}>
      {/* 背景装饰 */}
      <div style={{ position: 'fixed', inset: 0, overflow: 'hidden', pointerEvents: 'none' }}>
        <div style={{
          position: 'absolute',
          top: '-160px',
          right: '-160px',
          width: '320px',
          height: '320px',
          background: 'purple',
          borderRadius: '50%',
          opacity: 0.2,
          animation: 'float 6s ease-in-out infinite'
        }}></div>
        <div style={{
          position: 'absolute',
          bottom: '-160px',
          left: '-160px',
          width: '320px',
          height: '320px',
          background: 'cyan',
          borderRadius: '50%',
          opacity: 0.2,
          animation: 'float 6s ease-in-out infinite 2s'
        }}></div>
        <div style={{
          position: 'absolute',
          top: '160px',
          left: '50%',
          width: '320px',
          height: '320px',
          background: 'pink',
          borderRadius: '50%',
          opacity: 0.2,
          animation: 'float 6s ease-in-out infinite 4s'
        }}></div>
      </div>

      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass"
        style={{ position: 'relative', zIndex: 10, borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}
      >
        <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '80px' }}>
            <motion.div 
              style={{ display: 'flex', alignItems: 'center', gap: '16px' }}
              whileHover={{ scale: 1.05 }}
            >
              <div style={{ position: 'relative' }}>
                <BarChart3 size={40} color="#22d3ee" style={{ filter: 'drop-shadow(0 0 10px #22d3ee)' }} />
                <Sparkles size={16} color="#fbbf24" style={{ position: 'absolute', top: '-4px', right: '-4px', animation: 'pulse 2s infinite' }} />
              </div>
              <div>
                <h1 style={{ fontSize: '32px', fontWeight: 'bold', background: 'linear-gradient(135deg, #22d3ee 0%, #8b5cf6 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                  本地向量知识库
                </h1>
                <p style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)' }}>AI驱动的智能文档检索系统</p>
              </div>
            </motion.div>
            
            <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
              {stats && (
                <motion.div 
                  className="glass"
                  style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)', padding: '8px 16px', borderRadius: '8px' }}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Zap size={16} color="#fbbf24" />
                    <span>向量: {stats.total_vectors.toLocaleString()}</span>
                    <span style={{ color: 'rgba(255, 255, 255, 0.5)' }}>|</span>
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
      <div style={{ position: 'relative', zIndex: 10, maxWidth: '1280px', margin: '0 auto', padding: '0 16px' }}>
        <div className="glass" style={{ borderRadius: '16px', padding: '8px', marginTop: '32px' }}>
          <nav style={{ display: 'flex', gap: '8px' }}>
            {tabs.map((tab, index) => {
              const Icon = tab.icon
              const isActive = activeTab === tab.id
              return (
                <motion.button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  style={{
                    position: 'relative',
                    display: 'flex',
                    alignItems: 'center',
                    padding: '16px 24px',
                    borderRadius: '12px',
                    fontWeight: '500',
                    fontSize: '14px',
                    transition: 'all 0.3s',
                    color: isActive ? 'white' : 'rgba(255, 255, 255, 0.6)',
                    background: isActive ? `linear-gradient(135deg, ${tab.color.split(' ')[1]} 0%, ${tab.color.split(' ')[3]} 100%)` : 'transparent'
                  }}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Icon size={20} style={{ marginRight: '12px' }} />
                  <span>{tab.label}</span>
                </motion.button>
              )
            })}
          </nav>
        </div>

        {/* Tab Content */}
        <motion.div 
          style={{ marginTop: '32px' }}
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