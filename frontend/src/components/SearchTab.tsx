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
    if (similarity > 0.8) return 'from-green-500 to-emerald-500'
    if (similarity > 0.6) return 'from-yellow-500 to-orange-500'
    return 'from-red-500 to-pink-500'
  }

  return (
    <div className="space-y-8">
      {/* Search Form */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-2xl p-8 border border-white/10"
      >
        <div className="flex items-center space-x-3 mb-6">
          <div className="relative">
            <Search className="h-8 w-8 text-cyan-400 glow" />
            <Sparkles className="h-4 w-4 text-yellow-400 absolute -top-1 -right-1 animate-pulse" />
          </div>
          <div>
            <h2 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
              智能搜索
            </h2>
            <p className="text-sm text-muted-foreground">基于语义相似度的文档检索</p>
          </div>
        </div>

        <form onSubmit={handleSearch} className="space-y-4">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-muted-foreground" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="输入关键词搜索相关文档..."
              className="w-full pl-12 pr-4 py-4 glass border border-white/20 rounded-xl focus:ring-2 focus:ring-cyan-500 focus:border-transparent bg-transparent text-white placeholder:text-muted-foreground transition-all duration-300"
            />
          </div>
          
          <motion.button
            type="submit"
            disabled={loading || !query.trim()}
            className="w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-xl hover:from-cyan-600 hover:to-blue-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3 font-medium transition-all duration-300 shadow-lg hover:shadow-xl"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {loading ? (
              <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full" />
            ) : (
              <>
                <Search className="h-5 w-5" />
                开始搜索
                <Zap className="h-4 w-4" />
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
            className="glass border border-red-500/30 rounded-xl p-4 bg-red-500/10"
          >
            <p className="text-red-400 flex items-center gap-2">
              <Filter className="h-4 w-4" />
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
            <div className="flex items-center space-x-3">
              <TrendingUp className="h-6 w-6 text-green-400" />
              <h3 className="text-xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">
                搜索结果
              </h3>
              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
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
                  className="glass rounded-xl p-6 border border-white/10 hover:border-white/20 transition-all duration-300 group"
                  whileHover={{ scale: 1.02, y: -2 }}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-gradient-to-r from-blue-500 to-cyan-500 shadow-lg">
                        <FileText className="h-5 w-5 text-white" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-white group-hover:text-cyan-400 transition-colors">
                          {getFileName(result.file_path)}
                        </h4>
                        <p className="text-sm text-muted-foreground">文档路径</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <div className={`px-3 py-1 rounded-full bg-gradient-to-r ${getSimilarityColor(result.max_similarity)} text-white text-sm font-medium shadow-lg`}>
                        {result.max_similarity.toFixed(3)}
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-3">
                    <p className="text-muted-foreground leading-relaxed line-clamp-3">
                      {result.preview}
                    </p>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                        <div className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse" />
                        <span>语义匹配</span>
                      </div>
                      <div className="text-xs text-muted-foreground">
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
            className="text-center py-16"
          >
            <div className="glass rounded-2xl p-12 border border-white/10">
              <FileText className="h-16 w-16 text-muted-foreground mx-auto mb-6 opacity-50" />
              <h3 className="text-xl font-semibold text-white mb-2">未找到相关文档</h3>
              <p className="text-muted-foreground">尝试使用不同的关键词或检查文档是否已添加到知识库</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default SearchTab
