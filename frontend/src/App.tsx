import React, { useState, useEffect } from 'react'
import { Search, MessageCircle, FileText, BarChart3, Sparkles, Zap } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import StatsCard from './components/StatsCard'
import SearchTab from './components/SearchTab'
import QATab from './components/QATab'
import DocumentsTab from './components/DocumentsTab'
import LoadingScreen from './components/LoadingScreen'
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
  const [loadingMessage, setLoadingMessage] = useState('正在连接服务器...')
  const [loadingProgress, setLoadingProgress] = useState(0)
  const [retryCount, setRetryCount] = useState(0)

  useEffect(() => {
    // 强制暗黑模式
    document.documentElement.classList.add('dark')
    loadStatsWithRetry()
  }, [])

  const loadStatsWithRetry = async () => {
    const maxRetries = 30  // 增加重试次数，因为模型加载需要时间
    let currentRetry = 0
    
    while (currentRetry < maxRetries) {
      try {
        setLoadingMessage('正在连接服务器...')
        setLoadingProgress(10)
        
        const data = await getStats()
        setStats(data)
        setLoading(false)
        return
      } catch (error: any) {
        currentRetry++
        setRetryCount(currentRetry)
        
        if (currentRetry < maxRetries) {
          if (currentRetry < 10) {
            setLoadingMessage(`等待AI模型加载中... (${currentRetry}/${maxRetries})`)
            setLoadingProgress(Math.min(10 + currentRetry * 3, 70))
          } else {
            setLoadingMessage(`模型初始化中... (${currentRetry}/${maxRetries})`)
            setLoadingProgress(Math.min(70 + (currentRetry - 10) * 1, 95))
          }
          
          // 等待一段时间后重试
          await new Promise(resolve => setTimeout(resolve, 3000))
        } else {
          setLoadingMessage('连接失败，请检查服务器状态')
          setLoadingProgress(100)
          console.error('Failed to load stats after retries:', error)
        }
      }
    }
  }

  const tabs = [
    { id: 'search', label: '智能搜索', icon: Search, gradient: 'from-blue-500 to-cyan-500' },
    { id: 'qa', label: 'AI问答', icon: MessageCircle, gradient: 'from-purple-500 to-pink-500' },
    { id: 'documents', label: '文档管理', icon: FileText, gradient: 'from-green-500 to-emerald-500' },
  ] as const

  // 显示加载屏幕
  if (loading) {
    return (
      <LoadingScreen 
        message={loadingMessage}
        progress={loadingProgress}
      />
    )
  }

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Aceternity风格背景 */}
      <div className="absolute inset-0">
        {/* 主背景渐变 */}
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900" />
        
        {/* 动态光效 */}
        <motion.div
          className="absolute top-0 left-1/4 w-96 h-96 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-full blur-3xl"
          animate={{
            x: [0, 100, 0],
            y: [0, -50, 0],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        <motion.div
          className="absolute bottom-0 right-1/4 w-96 h-96 bg-gradient-to-r from-pink-500/20 to-cyan-500/20 rounded-full blur-3xl"
          animate={{
            x: [0, -100, 0],
            y: [0, 50, 0],
            scale: [1, 1.1, 1],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 2
          }}
        />
        
        {/* 网格背景 */}
        <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2260%22%20height%3D%2260%22%20viewBox%3D%220%200%2060%2060%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%239C92AC%22%20fill-opacity%3D%220.1%22%3E%3Ccircle%20cx%3D%2230%22%20cy%3D%2230%22%20r%3D%221%22/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-30" />
      </div>

      {/* 主内容区域 */}
      <div className="relative z-10">
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="border-b border-white/10 backdrop-blur-xl bg-white/5"
        >
          <div className="max-w-7xl mx-auto px-6">
            <div className="flex items-center justify-between h-20">
              <motion.div 
                className="flex items-center gap-6"
                whileHover={{ scale: 1.02 }}
              >
                <div className="relative">
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                    className="w-12 h-12 rounded-2xl bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center"
                  >
                    <BarChart3 size={24} className="text-white" />
                  </motion.div>
                  <motion.div 
                    className="absolute -top-1 -right-1 w-6 h-6 rounded-full bg-gradient-to-r from-yellow-400 to-orange-400 flex items-center justify-center"
                    animate={{ 
                      scale: [1, 1.2, 1],
                      rotate: [0, 180, 360]
                    }}
                    transition={{ 
                      duration: 2,
                      repeat: Infinity,
                      ease: "easeInOut"
                    }}
                  >
                    <Sparkles size={12} className="text-white" />
                  </motion.div>
                </div>
                <div>
                  <motion.h1 
                    className="text-3xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent"
                    animate={{ 
                      backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"]
                    }}
                    transition={{ 
                      duration: 3,
                      repeat: Infinity,
                      ease: "linear"
                    }}
                  >
                    本地向量知识库
                  </motion.h1>
                  <p className="text-white/60 text-sm">AI驱动的智能文档检索系统</p>
                </div>
              </motion.div>
              
              {stats && (
                <motion.div 
                  className="flex items-center gap-4 px-6 py-3 rounded-2xl bg-white/10 backdrop-blur-xl border border-white/20"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.5 }}
                >
                  <div className="flex items-center gap-2">
                    <Zap size={16} className="text-yellow-400" />
                    <span className="text-white/80 text-sm">
                      <span className="text-blue-400 font-bold">{stats.total_vectors.toLocaleString()}</span>
                      <span className="text-white/50 mx-2">|</span>
                      <span className="text-purple-400 font-bold">{stats.unique_files}</span>
                    </span>
                  </div>
                </motion.div>
              )}
            </div>
          </div>
        </motion.div>

        {/* Stats Card */}
        <AnimatePresence>
          {stats && (
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -30 }}
              transition={{ delay: 0.3 }}
              className="mt-8"
            >
              <StatsCard stats={stats} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* 主内容区域 */}
        <div className="max-w-7xl mx-auto px-6 py-8">
          {/* 导航标签 */}
          <motion.div 
            className="flex gap-2 mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            {tabs.map((tab, index) => {
              const Icon = tab.icon
              const isActive = activeTab === tab.id
              return (
                <motion.button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`relative flex items-center gap-3 px-6 py-3 rounded-xl font-medium text-sm transition-all duration-300 ${
                    isActive 
                      ? 'text-white shadow-lg' 
                      : 'text-white/60 hover:text-white hover:bg-white/5'
                  }`}
                  style={{
                    background: isActive 
                      ? `linear-gradient(135deg, ${tab.gradient.split(' ')[1]} 0%, ${tab.gradient.split(' ')[3]} 100%)` 
                      : 'transparent'
                  }}
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.6 + index * 0.1 }}
                >
                  <Icon size={18} />
                  <span>{tab.label}</span>
                  {isActive && (
                    <motion.div
                      className="absolute inset-0 rounded-xl border-2 border-white/30"
                      layoutId="activeTab"
                      transition={{ type: "spring", stiffness: 300, damping: 30 }}
                    />
                  )}
                </motion.button>
              )
            })}
          </motion.div>

          {/* 内容区域 */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
          >
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, x: 20, scale: 0.95 }}
                animate={{ opacity: 1, x: 0, scale: 1 }}
                exit={{ opacity: 0, x: -20, scale: 0.95 }}
                transition={{ duration: 0.3, ease: "easeInOut" }}
              >
                {activeTab === 'search' && <SearchTab />}
                {activeTab === 'qa' && <QATab />}
                {activeTab === 'documents' && <DocumentsTab onUpload={loadStats} />}
              </motion.div>
            </AnimatePresence>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default App
