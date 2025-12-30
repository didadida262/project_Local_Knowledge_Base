import React, { useState, useEffect } from 'react'
import { MessageCircle, Send, FileText, TrendingUp } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { askQuestion } from '../services/api'

interface QAResult {
  question: string
  answer: string
  sources: Array<{
    file_path: string
    file_name: string
    text: string
    similarity: number
    chunk_index: number
  }>
  confidence: number
}

interface QATabProps {
  resetKey?: number // 当这个key变化时，清空内容
}

const QATab: React.FC<QATabProps> = ({ resetKey = 0 }) => {
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState<QAResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [hasSubmitted, setHasSubmitted] = useState(false) // 是否已提交问题

  // 当 resetKey 变化时，清空所有内容
  useEffect(() => {
    if (resetKey > 0) {
      setQuestion('')
      setResult(null)
      setError(null)
      setLoading(false)
      setHasSubmitted(false)
    }
  }, [resetKey])

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim()) return

    setHasSubmitted(true) // 标记已提交
    setLoading(true)
    setError(null)

    try {
      const data = await askQuestion(question, 5)
      setResult(data)
    } catch (err) {
      setError('问答失败，请稍后重试')
      console.error('QA error:', err)
    } finally {
      setLoading(false)
    }
  }

  const getFileName = (filePath: string) => {
    return filePath.split('/').pop() || filePath
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.8) return 'text-green-400'
    if (confidence > 0.6) return 'text-yellow-400'
    return 'text-red-400'
  }

  return (
    <div className="space-y-4 pb-4">
      {/* Question Form */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-3xl p-8 border border-white/10"
      >
        <div className="flex items-center gap-4 mb-6">
          <div className="relative">
            <MessageCircle size={32} className="text-purple-400 drop-shadow-lg" />
          </div>
          <div>
            <h2 className="text-sm font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              AI问答
            </h2>
            <p className="text-white/60 text-xs">基于知识库内容的智能问答</p>
          </div>
        </div>

        <form onSubmit={handleAsk} className="space-y-4">
          <div className="relative">
            <MessageCircle className="absolute left-4 top-1/2 transform -translate-y-1/2 text-white/60" size={20} />
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="输入问题，基于知识库内容回答..."
              className="w-full pl-12 pr-4 py-4 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-purple-400/50 focus:border-purple-400/50"
            />
          </div>
          
          <motion.button
            type="submit"
            disabled={loading || !question.trim()}
            className="w-full py-4 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 text-white font-medium flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <Send size={20} />
                提问
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
            <p className="text-sm text-red-400">{error}</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Answer */}
      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="space-y-3"
          >
            <div className="glass p-6 border border-white/10">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <MessageCircle size={20} className="text-purple-400" />
                问题: {result.question}
              </h3>
              <div className="text-base text-white/80 leading-relaxed whitespace-pre-wrap">
                {result.answer}
              </div>
              {result.confidence > 0 && (
                <div className="mt-4 flex items-center gap-2">
                  <span className="text-sm text-white/60">置信度:</span>
                  <span className={`text-sm font-medium ${getConfidenceColor(result.confidence)}`}>
                    {(result.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              )}
            </div>

            {/* Sources */}
            {result.sources && result.sources.length > 0 && (
              <div className="space-y-4">
                <h4 className="text-lg font-semibold text-white flex items-center gap-2">
                  <TrendingUp size={20} className="text-green-400" />
                  参考文档
                </h4>
                <div className="grid gap-3">
                  {result.sources.map((source, index) => (
                    <div key={index} className="glass rounded-lg p-4 border border-white/10">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <FileText size={16} className="text-blue-400" />
                          <span className="font-medium text-white">{getFileName(source.file_path)}</span>
                        </div>
                        <span className="text-sm text-blue-400 font-medium">
                          相似度: {source.similarity.toFixed(3)}
                        </span>
                      </div>
                      <p className="text-white/70 text-base leading-relaxed line-clamp-2">
                        {source.text}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Loading State - 加载中时显示 */}
      <AnimatePresence>
        {loading && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="text-center py-16"
          >
            <div className="glass rounded-3xl p-12 border border-white/10">
              <div className="w-16 h-16 border-4 border-purple-400 border-t-transparent rounded-full animate-spin mx-auto mb-6" />
              <h3 className="text-lg font-semibold text-white mb-2">等待回答...</h3>
              <p className="text-white/60 text-sm">AI正在分析您的问题</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* No Result - 只在已提交且不在加载中且没有结果时显示 */}
      <AnimatePresence>
        {!result && !loading && hasSubmitted && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="text-center py-16"
          >
            <div className="glass rounded-3xl p-12 border border-white/10">
              <MessageCircle size={64} className="text-white/40 mx-auto mb-6" />
              <h3 className="text-lg font-semibold text-white mb-2">等待回答...</h3>
              <p className="text-white/60 text-sm">AI正在分析您的问题</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default QATab
