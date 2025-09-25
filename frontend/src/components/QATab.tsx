import React, { useState } from 'react'
import { MessageCircle, Send, FileText, TrendingUp } from 'lucide-react'
// import { motion, div } from 'framer-motion'
import { askQuestion } from '../services/api'

interface QAResult {
  question: string
  answer: string
  sources: Array<{
    file_path: string
    similarity_score: number
    chunk_preview: string
  }>
}

const QATab: React.FC = () => {
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState<QAResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim()) return

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

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      {/* Question Form */}
      <div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass"
        style={{ borderRadius: '16px', padding: '32px', border: '1px solid rgba(255, 255, 255, 0.1)' }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
          <div style={{ position: 'relative' }}>
            <MessageCircle size={32} color="#8b5cf6" style={{ filter: 'drop-shadow(0 0 10px #8b5cf6)' }} />
          </div>
          <div>
            <h2 style={{ fontSize: '24px', fontWeight: 'bold', background: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              AI问答
            </h2>
            <p style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)' }}>基于知识库内容的智能问答</p>
          </div>
        </div>

        <form onSubmit={handleAsk} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ position: 'relative' }}>
            <MessageCircle style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)', color: 'rgba(255, 255, 255, 0.6)' }} size={20} />
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="输入问题，基于知识库内容回答..."
              className="input"
              style={{ paddingLeft: '48px' }}
            />
          </div>
          
          <motion.button
            type="submit"
            disabled={loading || !question.trim()}
            className="btn"
            style={{
              width: '100%',
              padding: '16px',
              background: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)',
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
              opacity: (loading || !question.trim()) ? 0.5 : 1,
              pointerEvents: (loading || !question.trim()) ? 'none' : 'auto'
            }}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {loading ? (
              <div style={{ width: '20px', height: '20px', border: '2px solid white', borderTop: '2px solid transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
            ) : (
              <>
                <Send size={20} />
                提问
              </>
            )}
          </motion.button>
        </form>
      </div>

      {/* Error Message */}
      <div>
        {error && (
          <div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="glass"
            style={{ borderRadius: '12px', padding: '16px', border: '1px solid rgba(239, 68, 68, 0.3)', background: 'rgba(239, 68, 68, 0.1)' }}
          >
            <p style={{ color: '#f87171' }}>{error}</p>
          </div>
        )}
      </div>

      {/* Answer */}
      <div>
        {result && (
          <div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}
          >
            <div className="glass" style={{ borderRadius: '16px', padding: '24px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
              <h3 style={{ fontSize: '18px', fontWeight: '600', color: 'white', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <MessageCircle size={20} color="#8b5cf6" />
                问题: {result.question}
              </h3>
              <div style={{ color: 'rgba(255, 255, 255, 0.8)', lineHeight: '1.6', whiteSpace: 'pre-wrap' }}>
                {result.answer}
              </div>
            </div>

            {/* Sources */}
            {result.sources && result.sources.length > 0 && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <h4 style={{ fontSize: '18px', fontWeight: '600', color: 'white', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <TrendingUp size={20} color="#10b981" />
                  参考文档
                </h4>
                <div style={{ display: 'grid', gap: '12px' }}>
                  {result.sources.map((source, index) => (
                    <div key={index} className="glass" style={{ borderRadius: '12px', padding: '16px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
                      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '8px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <FileText size={16} color="#3b82f6" />
                          <span style={{ fontWeight: '500', color: 'white' }}>{getFileName(source.file_path)}</span>
                        </div>
                        <span style={{ fontSize: '14px', color: '#3b82f6', fontWeight: '500' }}>
                          相似度: {source.similarity_score.toFixed(3)}
                        </span>
                      </div>
                      <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px', lineHeight: '1.5' }}>
                        {source.chunk_preview}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* No Result */}
      <div>
        {!result && !loading && question && (
          <div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            style={{ textAlign: 'center', padding: '64px 0' }}
          >
            <div className="glass" style={{ borderRadius: '16px', padding: '48px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
              <MessageCircle size={64} color="rgba(255, 255, 255, 0.4)" style={{ margin: '0 auto 24px' }} />
              <h3 style={{ fontSize: '20px', fontWeight: '600', color: 'white', marginBottom: '8px' }}>等待回答...</h3>
              <p style={{ color: 'rgba(255, 255, 255, 0.6)' }}>AI正在分析您的问题</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default QATab