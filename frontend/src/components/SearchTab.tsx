import React, { useState } from 'react'
import { Search, FileText, TrendingUp, Sparkles, Zap, Filter } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { searchDocuments } from '../services/api'

interface SearchResult {
  file_path: string
  max_similarity: number
  preview: string
}

const SearchTab: React.FC = () => {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setError(null)

    try {
      const data = await searchDocuments(query, 10)
      setResults(data.results || [])
    } catch (err) {
      setError('搜索失败，请稍后重试')
      console.error('Search error:', err)
    } finally {
      setLoading(false)
    }
  }

  const getFileName = (filePath: string) => {
    return filePath.split('/').pop() || filePath
  }

  const getSimilarityColor = (similarity: number) => {
    if (similarity > 0.8) return '#10b981'
    if (similarity > 0.6) return '#f59e0b'
    return '#ef4444'
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      {/* Search Form */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass"
        style={{ borderRadius: '16px', padding: '32px', border: '1px solid rgba(255, 255, 255, 0.1)' }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
          <div style={{ position: 'relative' }}>
            <Search size={32} color="#22d3ee" style={{ filter: 'drop-shadow(0 0 10px #22d3ee)' }} />
            <Sparkles size={16} color="#fbbf24" style={{ position: 'absolute', top: '-4px', right: '-4px', animation: 'pulse 2s infinite' }} />
          </div>
          <div>
            <h2 style={{ fontSize: '24px', fontWeight: 'bold', background: 'linear-gradient(135deg, #22d3ee 0%, #3b82f6 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              智能搜索
            </h2>
            <p style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)' }}>基于语义相似度的文档检索</p>
          </div>
        </div>

        <form onSubmit={handleSearch} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ position: 'relative' }}>
            <Search style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)', color: 'rgba(255, 255, 255, 0.6)' }} size={20} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="输入关键词搜索相关文档..."
              className="input"
              style={{ paddingLeft: '48px' }}
            />
          </div>
          
          <motion.button
            type="submit"
            disabled={loading || !query.trim()}
            className="btn"
            style={{
              width: '100%',
              padding: '16px',
              background: 'linear-gradient(135deg, #22d3ee 0%, #3b82f6 100%)',
              color: 'white',
              borderRadius: '12px',
              border: 'none',
              cursor: 'pointer',
              fontSize: '16px',
              fontWeight: '500',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '12px',
              opacity: (loading || !query.trim()) ? 0.5 : 1,
              pointerEvents: (loading || !query.trim()) ? 'none' : 'auto'
            }}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {loading ? (
              <div style={{ width: '20px', height: '20px', border: '2px solid white', borderTop: '2px solid transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
            ) : (
              <>
                <Search size={20} />
                开始搜索
                <Zap size={16} />
              </>
            )}
          </motion.button>
        </form>
      </motion.div>

      {/* Error Message */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="glass"
            style={{ borderRadius: '12px', padding: '16px', border: '1px solid rgba(239, 68, 68, 0.3)', background: 'rgba(239, 68, 68, 0.1)' }}
          >
            <p style={{ color: '#f87171', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Filter size={16} />
              {error}
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Search Results */}
      <AnimatePresence>
        {results.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <TrendingUp size={24} color="#10b981" />
              <h3 style={{ fontSize: '20px', fontWeight: 'bold', background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                搜索结果
              </h3>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)' }}>
                <div style={{ width: '8px', height: '8px', background: '#10b981', borderRadius: '50%', animation: 'pulse 2s infinite' }} />
                <span>找到 {results.length} 个相关结果</span>
              </div>
            </div>
            
            <div style={{ display: 'grid', gap: '16px' }}>
              {results.map((result, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="glass"
                  style={{
                    borderRadius: '12px',
                    padding: '24px',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    transition: 'all 0.3s'
                  }}
                  whileHover={{ scale: 1.02, y: -2 }}
                >
                  <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '16px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <div style={{ padding: '8px', borderRadius: '8px', background: 'linear-gradient(135deg, #3b82f6 0%, #22d3ee 100%)', boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)' }}>
                        <FileText size={20} color="white" />
                      </div>
                      <div>
                        <h4 style={{ fontWeight: '600', color: 'white', marginBottom: '4px' }}>{getFileName(result.file_path)}</h4>
                        <p style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)' }}>文档路径</p>
                      </div>
                    </div>
                    
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <div style={{
                        padding: '4px 12px',
                        borderRadius: '20px',
                        background: `linear-gradient(135deg, ${getSimilarityColor(result.max_similarity)} 0%, ${getSimilarityColor(result.max_similarity)}80 100%)`,
                        color: 'white',
                        fontSize: '14px',
                        fontWeight: '500',
                        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.3)'
                      }}>
                        {result.max_similarity.toFixed(3)}
                      </div>
                    </div>
                  </div>
                  
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    <p style={{ color: 'rgba(255, 255, 255, 0.6)', lineHeight: '1.6', maxHeight: '60px', overflow: 'hidden' }}>
                      {result.preview}
                    </p>
                    
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: 'rgba(255, 255, 255, 0.6)' }}>
                        <div style={{ width: '6px', height: '6px', background: '#22d3ee', borderRadius: '50%', animation: 'pulse 2s infinite' }} />
                        <span>语义匹配</span>
                      </div>
                      <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.6)' }}>
                        相似度: {(result.max_similarity * 100).toFixed(1)}%
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* No Results */}
      <AnimatePresence>
        {results.length === 0 && !loading && query && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            style={{ textAlign: 'center', padding: '64px 0' }}
          >
            <div className="glass" style={{ borderRadius: '16px', padding: '48px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
              <FileText size={64} color="rgba(255, 255, 255, 0.4)" style={{ margin: '0 auto 24px' }} />
              <h3 style={{ fontSize: '20px', fontWeight: '600', color: 'white', marginBottom: '8px' }}>未找到相关文档</h3>
              <p style={{ color: 'rgba(255, 255, 255, 0.6)' }}>尝试使用不同的关键词或检查文档是否已添加到知识库</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default SearchTab