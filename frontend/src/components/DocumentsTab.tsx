import React, { useState, useEffect } from 'react'
import { Upload, FileText, Plus, Trash2, CheckCircle, RefreshCw } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { getDocuments, uploadDocument, addDocument, rebuildKnowledgeBase } from '../services/api'

interface Document {
  file_path: string
  file_name: string
  chunk_count: number
  word_count: number
  file_size: number
}

interface DocumentsTabProps {
  onUpload: () => void
}

const DocumentsTab: React.FC<DocumentsTabProps> = ({ onUpload }) => {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [filePath, setFilePath] = useState('')
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)

  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    try {
      const data = await getDocuments()
      setDocuments(data.documents || [])
    } catch (error) {
      console.error('Failed to load documents:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (!files || files.length === 0) return

    setUploading(true)
    setMessage(null)

    try {
      for (const file of files) {
        const formData = new FormData()
        formData.append('file', file)
        
        const result = await uploadDocument(formData)
        if (result.success) {
          setMessage({ type: 'success', text: result.message })
        } else {
          setMessage({ type: 'error', text: result.error || '上传失败' })
        }
      }
      
      await loadDocuments()
      onUpload()
    } catch (error) {
      setMessage({ type: 'error', text: '上传失败，请稍后重试' })
    } finally {
      setUploading(false)
      e.target.value = ''
    }
  }

  const handleAddDocument = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!filePath.trim()) return

    setUploading(true)
    setMessage(null)

    try {
      const result = await addDocument(filePath)
      if (result.success) {
        setMessage({ type: 'success', text: result.message })
        setFilePath('')
        await loadDocuments()
        onUpload()
      } else {
        setMessage({ type: 'error', text: result.error || '添加失败' })
      }
    } catch (error) {
      setMessage({ type: 'error', text: '添加失败，请稍后重试' })
    } finally {
      setUploading(false)
    }
  }

  const handleRebuild = async () => {
    setUploading(true)
    setMessage(null)

    try {
      const result = await rebuildKnowledgeBase()
      if (result.success) {
        setMessage({ type: 'success', text: result.message })
        await loadDocuments()
        onUpload()
      } else {
        setMessage({ type: 'error', text: result.error || '重建失败' })
      }
    } catch (error) {
      setMessage({ type: 'error', text: '重建失败，请稍后重试' })
    } finally {
      setUploading(false)
    }
  }

  const getFileName = (filePath: string) => {
    return filePath.split('/').pop() || filePath
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className="space-y-8">
      {/* Add Document Form */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-2xl p-6 border border-white/10"
      >
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Plus size={20} className="text-green-400" />
          添加本地文档
        </h3>
        <form onSubmit={handleAddDocument} className="flex gap-4">
          <input
            type="text"
            value={filePath}
            onChange={(e) => setFilePath(e.target.value)}
            placeholder="输入文件路径..."
            className="flex-1 px-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-green-400/50 focus:border-green-400/50"
          />
          <motion.button
            type="submit"
            disabled={uploading || !filePath.trim()}
            className="px-6 py-3 rounded-xl bg-gradient-to-r from-green-500 to-emerald-500 text-white font-medium flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {uploading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <Plus size={16} />
                添加
              </>
            )}
          </motion.button>
        </form>
      </motion.div>

      {/* Upload Documents */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-3xl p-8 border-2 border-dashed border-white/30 text-center"
      >
        <Upload size={48} className="text-white/40 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-white mb-2">上传文档</h3>
        <p className="text-white/60 mb-6">
          支持格式: TXT, MD, PDF, DOCX, HTML
        </p>
        <input
          type="file"
          multiple
          accept=".txt,.md,.pdf,.docx,.html,.htm"
          onChange={handleFileUpload}
          disabled={uploading}
          className="hidden"
          id="file-upload"
        />
        <label
          htmlFor="file-upload"
          className={`inline-flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all ${
            uploading 
              ? 'bg-white/10 text-white/40 cursor-not-allowed' 
              : 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white cursor-pointer hover:scale-105'
          }`}
        >
          {uploading ? (
            <div className="w-4 h-4 border-2 border-white/40 border-t-transparent rounded-full animate-spin" />
          ) : (
            <Upload size={16} />
          )}
          {uploading ? '上传中...' : '选择文件'}
        </label>
      </motion.div>

      {/* Rebuild Button */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-2xl p-6 border border-white/10"
      >
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-white mb-2">重建知识库</h3>
            <p className="text-white/60 text-sm">重新扫描docs目录并重建向量索引</p>
          </div>
          <motion.button
            onClick={handleRebuild}
            disabled={uploading}
            className="px-6 py-3 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 text-white font-medium flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {uploading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <RefreshCw size={16} />
            )}
            {uploading ? '重建中...' : '重建知识库'}
          </motion.button>
        </div>
      </motion.div>

      {/* Message */}
      <AnimatePresence>
        {message && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className={`glass rounded-xl p-4 border ${
              message.type === 'success' 
                ? 'border-green-500/30 bg-green-500/10' 
                : 'border-red-500/30 bg-red-500/10'
            }`}
          >
            <p className={`flex items-center gap-2 ${
              message.type === 'success' ? 'text-green-400' : 'text-red-400'
            }`}>
              {message.type === 'success' ? <CheckCircle size={16} /> : <Trash2 size={16} />}
              {message.text}
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Documents List */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass rounded-2xl p-6 border border-white/10"
      >
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <FileText size={20} className="text-blue-400" />
          文档列表
        </h3>
        
        {loading ? (
          <div className="text-center py-8">
            <div className="w-8 h-8 border-3 border-blue-400 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
            <p className="text-white/60">加载中...</p>
          </div>
        ) : documents.length === 0 ? (
          <div className="text-center py-8">
            <FileText size={48} className="text-white/40 mx-auto mb-4" />
            <p className="text-white/60">暂无文档</p>
          </div>
        ) : (
          <div className="grid gap-3">
            {documents.map((doc, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/10 hover:border-white/20 transition-all duration-300"
                whileHover={{ scale: 1.02, y: -2 }}
              >
                <div className="flex items-center gap-3">
                  <FileText size={20} className="text-blue-400" />
                  <div>
                    <p className="font-medium text-white">{getFileName(doc.file_path)}</p>
                    <p className="text-sm text-white/60">
                      块数: {doc.chunk_count} | 大小: {formatFileSize(doc.file_size)}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </motion.div>
    </div>
  )
}

export default DocumentsTab
