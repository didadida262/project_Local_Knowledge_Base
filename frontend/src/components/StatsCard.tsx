import React from 'react'
import { BarChart3, FileText, Hash, TrendingUp, Sparkles, Zap } from 'lucide-react'
import { motion } from 'framer-motion'

interface Stats {
  total_vectors: number
  total_documents: number
  unique_files: number
}

interface StatsCardProps {
  stats: Stats
}

const StatsCard: React.FC<StatsCardProps> = ({ stats }) => {
  const statItems = [
    {
      label: '总向量数',
      value: stats.total_vectors.toLocaleString(),
      icon: Hash,
      gradient: 'from-blue-500 to-cyan-500',
      bgGradient: 'from-blue-500/20 to-cyan-500/20'
    },
    {
      label: '总文档数',
      value: stats.total_documents.toLocaleString(),
      icon: FileText,
      gradient: 'from-green-500 to-emerald-500',
      bgGradient: 'from-green-500/20 to-emerald-500/20'
    },
    {
      label: '唯一文件数',
      value: stats.unique_files.toLocaleString(),
      icon: BarChart3,
      gradient: 'from-purple-500 to-pink-500',
      bgGradient: 'from-purple-500/20 to-pink-500/20'
    }
  ]

  return (
    <div className="max-w-7xl mx-auto px-6 mb-8 mt-8">
      <motion.div 
        className="relative p-8 rounded-3xl bg-white/5 backdrop-blur-xl border border-white/10"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* 背景装饰 */}
        <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-pink-500/10" />
        
        <div className="relative z-10">
          <div className="flex items-center gap-4 mb-8">
            <motion.div
              className="w-12 h-12 rounded-2xl bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center"
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            >
              <TrendingUp size={24} className="text-white" />
            </motion.div>
            <div>
              <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                知识库统计
              </h2>
              <p className="text-white/60 text-sm">实时数据概览</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {statItems.map((item, index) => {
              const Icon = item.icon
              return (
                <motion.div
                  key={index}
                  className="relative group"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.05, y: -5 }}
                >
                  <div className="relative p-6 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 overflow-hidden">
                    {/* 背景渐变 */}
                    <div className={`absolute inset-0 bg-gradient-to-r ${item.bgGradient} opacity-50`} />
                    
                    {/* 内容 */}
                    <div className="relative z-10">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                          <motion.div 
                            className={`w-10 h-10 rounded-xl bg-gradient-to-r ${item.gradient} flex items-center justify-center`}
                            whileHover={{ rotate: 360 }}
                            transition={{ duration: 0.5 }}
                          >
                            <Icon size={20} className="text-white" />
                          </motion.div>
                          <div>
                            <h3 className="text-sm font-medium text-white/80">{item.label}</h3>
                            <div className="flex items-center gap-2 mt-1">
                              <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                              <span className="text-xs text-white/60">活跃状态</span>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <motion.div
                        className="text-3xl font-bold text-white"
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: index * 0.1 + 0.3, type: "spring", bounce: 0.4 }}
                      >
                        {item.value}
                      </motion.div>
                    </div>
                    
                    {/* 装饰性光效 */}
                    <motion.div
                      className={`absolute top-4 right-4 w-8 h-8 rounded-full bg-gradient-to-r ${item.gradient} opacity-20`}
                      animate={{ 
                        scale: [1, 1.2, 1],
                        opacity: [0.2, 0.4, 0.2]
                      }}
                      transition={{ 
                        duration: 2,
                        repeat: Infinity,
                        ease: "easeInOut"
                      }}
                    />
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default StatsCard
