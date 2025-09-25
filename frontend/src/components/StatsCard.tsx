import React from 'react'
import { BarChart3, FileText, Hash, TrendingUp, Sparkles, Zap } from 'lucide-react'
// import { motion } from 'framer-motion'

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
      color: '#22d3ee',
      bgColor: 'rgba(34, 211, 238, 0.2)'
    },
    {
      label: '总文档数',
      value: stats.total_documents.toLocaleString(),
      icon: FileText,
      color: '#10b981',
      bgColor: 'rgba(16, 185, 129, 0.2)'
    },
    {
      label: '唯一文件数',
      value: stats.unique_files.toLocaleString(),
      icon: BarChart3,
      color: '#8b5cf6',
      bgColor: 'rgba(139, 92, 246, 0.2)'
    }
  ]

  return (
    <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 16px 24px' }}>
      <div 
        className="glass"
        style={{ borderRadius: '16px', padding: '32px', border: '1px solid rgba(255, 255, 255, 0.1)' }}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '32px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ position: 'relative' }}>
              <TrendingUp size={32} color="#22d3ee" style={{ filter: 'drop-shadow(0 0 10px #22d3ee)' }} />
              <Sparkles size={16} color="#fbbf24" style={{ position: 'absolute', top: '-4px', right: '-4px', animation: 'pulse 2s infinite' }} />
            </div>
            <div>
              <h2 style={{ fontSize: '24px', fontWeight: 'bold', background: 'linear-gradient(135deg, #22d3ee 0%, #8b5cf6 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                知识库统计
              </h2>
              <p style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)' }}>实时数据概览</p>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)' }}>
            <Zap size={16} color="#fbbf24" />
            <span>实时更新</span>
          </div>
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
          {statItems.map((item, index) => {
            const Icon = item.icon
            return (
              <div
                key={index}
                className="glass"
                style={{
                  position: 'relative',
                  borderRadius: '12px',
                  padding: '24px',
                  border: `1px solid ${item.color}40`,
                  boxShadow: `0 0 20px ${item.color}40`,
                  background: item.bgColor
                }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: 1.05, y: -5 }}
              >
                <div style={{ position: 'relative', zIndex: 10 }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <div style={{ padding: '12px', borderRadius: '8px', background: `linear-gradient(135deg, ${item.color} 0%, ${item.color}80 100%)`, boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)' }}>
                        <Icon size={24} color="white" />
                      </div>
                      <div>
                        <h3 style={{ fontSize: '14px', fontWeight: '500', color: 'rgba(255, 255, 255, 0.6)' }}>{item.label}</h3>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '8px' }}>
                          <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: `linear-gradient(135deg, ${item.color} 0%, ${item.color}80 100%)`, animation: 'pulse 2s infinite' }} />
                          <span style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.6)' }}>活跃状态</span>
                        </div>
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div
                        style={{ fontSize: '32px', fontWeight: 'bold', background: 'linear-gradient(135deg, white 0%, rgba(255, 255, 255, 0.8) 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: index * 0.1 + 0.3, type: "spring", bounce: 0.4 }}
                      >
                        {item.value}
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* 装饰性元素 */}
                <div style={{ position: 'absolute', top: '16px', right: '16px', opacity: 0.2 }}>
                  <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: `linear-gradient(135deg, ${item.color} 0%, ${item.color}80 100%)`, animation: 'pulse 2s infinite' }} />
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default StatsCard