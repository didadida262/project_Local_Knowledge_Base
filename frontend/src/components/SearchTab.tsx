import React, { useState } from 'react'
import { Search, FileText, TrendingUp, Sparkles, Zap, Filter } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { searchDocuments } from '../services/api'

interface SearchResult {
  file_path: string
  file_name: string
  text: string
  similarity: number
  chunk_index: number
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
    if (similarity > 0.8) return 'text-green-400'
    if (similarity > 0.6) return 'text-yellow-400'
    return 'text-red-400'
  }

  return (
    <div className="space-y-8">
      {/* Search Form */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-3xl p-8 border border-white/10"
      >
        <div className="flex items-center gap-4 mb-6">
          <div className="relative">
            <Search size={32} className="text-cyan-400 drop-shadow-lg" />
            <Sparkles size={16} className="text-yellow-400 absolute -top-1 -right-1 animate-pulse" />
          </div>
          <div>
            <h2 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
              智能搜索
            </h2>
            <p className="text-white/60 text-sm">基于语义相似度的文档检索</p>
          </div>
        </div>

        <form onSubmit={handleSearch} className="space-y-4">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-white/60" size={20} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="输入关键词搜索相关文档..."
              className="w-full pl-12 pr-4 py-4 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-cyan-400/50 focus:border-cyan-400/50"
            />
          </div>
          
          <motion.button
            type="submit"
            disabled={loading || !query.trim()}
            className="w-full py-4 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-medium flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
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
            className="glass rounded-xl p-4 border border-red-500/30 bg-red-500/10"
          >
            <p className="text-red-400 flex items-center gap-2">
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
            className="space-y-6"
          >
            <div className="flex items-center gap-3">
              <TrendingUp size={24} className="text-green-400" />
              <h3 className="text-xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">
                搜索结果
              </h3>
              <div className="flex items-center gap-2 text-sm text-white/60">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                <span>找到 {results.length} 个相关结果</span>
              </div>
            </div>
            
            <div className="grid gap-4">
              {results.map((result, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="glass rounded-2xl p-6 border border-white/10 hover:border-white/20 transition-all duration-300"
                  whileHover={{ scale: 1.02, y: -2 }}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500 flex items-center justify-center">
                        <FileText size={20} className="text-white" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-white">{getFileName(result.file_path)}</h4>
                        <p className="text-sm text-white/60">文档路径</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <span className={`text-sm font-medium ${getSimilarityColor(result.similarity)}`}>
                        {result.similarity.toFixed(3)}
                      </span>
                    </div>
                  </div>
                  
                  <div className="space-y-3">
                    <p className="text-white/80 leading-relaxed line-clamp-3">
                      {result.text}
                    </p>
                    
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-2 text-white/60">
                        <div className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse" />
                        <span>语义匹配</span>
                      </div>
                      <div className="text-white/60">
                        相似度: {(result.similarity * 100).toFixed(1)}%
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
            className="text-center py-16"
          >
            <div className="glass rounded-3xl p-12 border border-white/10">
              <FileText size={64} className="text-white/40 mx-auto mb-6" />
              <h3 className="text-xl font-semibold text-white mb-2">未找到相关文档</h3>
              <p className="text-white/60">尝试使用不同的关键词或检查文档是否已添加到知识库</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default SearchTab
