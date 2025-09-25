import React, { useState } from 'react'
import { MessageCircle, Send, FileText, TrendingUp } from 'lucide-react'
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
    <div className="space-y-6">
      {/* Question Form */}
      <form onSubmit={handleAsk} className="flex gap-4">
        <div className="flex-1 relative">
          <MessageCircle className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="输入问题，基于知识库内容回答..."
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {loading ? (
            <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full" />
          ) : (
            <>
              <Send className="h-5 w-5" />
              提问
            </>
          )}
        </button>
      </form>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Answer */}
      {result && (
        <div className="space-y-4">
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <MessageCircle className="h-5 w-5" />
              问题: {result.question}
            </h3>
            <div className="prose max-w-none">
              <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                {result.answer}
              </p>
            </div>
          </div>

          {/* Sources */}
          {result.sources && result.sources.length > 0 && (
            <div className="space-y-3">
              <h4 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                参考文档
              </h4>
              <div className="space-y-3">
                {result.sources.map((source, index) => (
                  <div key={index} className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <FileText className="h-5 w-5 text-blue-600" />
                        <span className="font-medium text-gray-900">
                          {getFileName(source.file_path)}
                        </span>
                      </div>
                      <span className="text-sm text-blue-600 font-medium">
                        相似度: {source.similarity_score.toFixed(3)}
                      </span>
                    </div>
                    <p className="text-gray-600 text-sm leading-relaxed">
                      {source.chunk_preview}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* No Result */}
      {!result && !loading && question && (
        <div className="text-center py-12">
          <MessageCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">等待回答...</p>
        </div>
      )}
    </div>
  )
}

export default QATab
