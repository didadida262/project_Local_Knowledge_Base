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
      gradient: 'from-cyan-500 to-blue-500',
      bgGradient: 'from-cyan-500/20 to-blue-500/20',
      borderColor: 'border-cyan-500/30',
      glowColor: 'shadow-cyan-500/25'
    },
    {
      label: '总文档数',
      value: stats.total_documents.toLocaleString(),
      icon: FileText,
      gradient: 'from-emerald-500 to-green-500',
      bgGradient: 'from-emerald-500/20 to-green-500/20',
      borderColor: 'border-emerald-500/30',
      glowColor: 'shadow-emerald-500/25'
    },
    {
      label: '唯一文件数',
      value: stats.unique_files.toLocaleString(),
      icon: BarChart3,
      gradient: 'from-purple-500 to-pink-500',
      bgGradient: 'from-purple-500/20 to-pink-500/20',
      borderColor: 'border-purple-500/30',
      glowColor: 'shadow-purple-500/25'
    }
  ]

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <motion.div 
        className="glass rounded-2xl p-8 border border-white/10"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <TrendingUp className="h-8 w-8 text-cyan-400 glow" />
              <Sparkles className="h-4 w-4 text-yellow-400 absolute -top-1 -right-1 animate-pulse" />
            </div>
            <div>
              <h2 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                知识库统计
              </h2>
              <p className="text-sm text-muted-foreground">实时数据概览</p>
            </div>
          </div>
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Zap className="h-4 w-4 text-yellow-400" />
            <span>实时更新</span>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {statItems.map((item, index) => {
            const Icon = item.icon
            return (
              <motion.div
                key={index}
                className={`relative glass rounded-xl p-6 border ${item.borderColor} ${item.glowColor} shadow-2xl hover:shadow-3xl transition-all duration-300 group`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: 1.05, y: -5 }}
              >
                {/* 背景渐变 */}
                <div className={`absolute inset-0 bg-gradient-to-br ${item.bgGradient} rounded-xl opacity-50 group-hover:opacity-70 transition-opacity duration-300`} />
                
                {/* 内容 */}
                <div className="relative z-10">
                  <div className="flex items-center justify-between mb-4">
                    <div className={`p-3 rounded-lg bg-gradient-to-r ${item.gradient} shadow-lg`}>
                      <Icon className="h-6 w-6 text-white" />
                    </div>
                    <div className="text-right">
                      <motion.div
                        className="text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent"
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: index * 0.1 + 0.3, type: "spring", bounce: 0.4 }}
                      >
                        {item.value}
                      </motion.div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <h3 className="text-sm font-medium text-muted-foreground">{item.label}</h3>
                    <div className="flex items-center space-x-2">
                      <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${item.gradient} animate-pulse`} />
                      <span className="text-xs text-muted-foreground">活跃状态</span>
                    </div>
                  </div>
                </div>
                
                {/* 装饰性元素 */}
                <div className="absolute top-4 right-4 opacity-20">
                  <div className={`w-8 h-8 rounded-full bg-gradient-to-r ${item.gradient} animate-pulse`} />
                </div>
              </motion.div>
            )
          })}
        </div>
      </motion.div>
    </div>
  )
}

export default StatsCard
