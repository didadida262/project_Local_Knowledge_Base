import React, { useState, useEffect } from 'react'
import { Upload, FileText, Plus, Trash2, CheckCircle } from 'lucide-react'
// import { motion, div } from 'framer-motion'
import { getDocuments, uploadDocument, addDocument } from '../services/api'

interface Document {
  file_path: string
  chunk_count: number
  last_modified: string | null
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

  const getFileName = (filePath: string) => {
    return filePath.split('/').pop() || filePath
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      {/* Add Document Form */}
      <div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass"
        style={{ borderRadius: '16px', padding: '24px', border: '1px solid rgba(255, 255, 255, 0.1)' }}
      >
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: 'white', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Plus size={20} color="#10b981" />
          添加本地文档
        </h3>
        <form onSubmit={handleAddDocument} style={{ display: 'flex', gap: '16px' }}>
          <input
            type="text"
            value={filePath}
            onChange={(e) => setFilePath(e.target.value)}
            placeholder="输入文件路径..."
            className="input"
            style={{ flex: 1 }}
          />
          <motion.button
            type="submit"
            disabled={uploading || !filePath.trim()}
            className="btn"
            style={{
              padding: '12px 24px',
              background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
              color: 'white',
              borderRadius: '8px',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              opacity: (uploading || !filePath.trim()) ? 0.5 : 1,
              pointerEvents: (uploading || !filePath.trim()) ? 'none' : 'auto'
            }}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {uploading ? (
              <div style={{ width: '16px', height: '16px', border: '2px solid white', borderTop: '2px solid transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
            ) : (
              <>
                <Plus size={16} />
                添加
              </>
            )}
          </motion.button>
        </form>
      </div>

      {/* Upload Documents */}
      <div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass"
        style={{ borderRadius: '16px', padding: '32px', border: '2px dashed rgba(255, 255, 255, 0.3)', textAlign: 'center' }}
      >
        <Upload size={48} color="rgba(255, 255, 255, 0.4)" style={{ margin: '0 auto 16px' }} />
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: 'white', marginBottom: '8px' }}>上传文档</h3>
        <p style={{ color: 'rgba(255, 255, 255, 0.6)', marginBottom: '16px' }}>
          支持格式: TXT, MD, PDF, DOCX, HTML
        </p>
        <input
          type="file"
          multiple
          accept=".txt,.md,.pdf,.docx,.html,.htm"
          onChange={handleFileUpload}
          disabled={uploading}
          style={{ display: 'none' }}
          id="file-upload"
        />
        <label
          htmlFor="file-upload"
          className="btn"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px',
            padding: '12px 24px',
            background: uploading ? 'rgba(255, 255, 255, 0.1)' : 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
            color: uploading ? 'rgba(255, 255, 255, 0.4)' : 'white',
            borderRadius: '8px',
            cursor: uploading ? 'not-allowed' : 'pointer',
            transition: 'all 0.3s'
          }}
        >
          {uploading ? (
            <div style={{ width: '16px', height: '16px', border: '2px solid rgba(255, 255, 255, 0.4)', borderTop: '2px solid transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
          ) : (
            <Upload size={16} />
          )}
          {uploading ? '上传中...' : '选择文件'}
        </label>
      </div>

      {/* Message */}
      <div>
        {message && (
          <div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="glass"
            style={{
              borderRadius: '12px',
              padding: '16px',
              border: `1px solid ${message.type === 'success' ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
              background: message.type === 'success' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)'
            }}
          >
            <p style={{ color: message.type === 'success' ? '#10b981' : '#f87171', display: 'flex', alignItems: 'center', gap: '8px' }}>
              {message.type === 'success' ? <CheckCircle size={16} /> : <Trash2 size={16} />}
              {message.text}
            </p>
          </div>
        )}
      </div>

      {/* Documents List */}
      <div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass"
        style={{ borderRadius: '16px', padding: '24px', border: '1px solid rgba(255, 255, 255, 0.1)' }}
      >
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: 'white', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <FileText size={20} color="#3b82f6" />
          文档列表
        </h3>
        
        {loading ? (
          <div style={{ textAlign: 'center', padding: '32px' }}>
            <div style={{ width: '32px', height: '32px', border: '3px solid #3b82f6', borderTop: '3px solid transparent', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto 16px' }} />
            <p style={{ color: 'rgba(255, 255, 255, 0.6)' }}>加载中...</p>
          </div>
        ) : documents.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '32px' }}>
            <FileText size={48} color="rgba(255, 255, 255, 0.4)" style={{ margin: '0 auto 16px' }} />
            <p style={{ color: 'rgba(255, 255, 255, 0.6)' }}>暂无文档</p>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: '12px' }}>
            {documents.map((doc, index) => (
              <div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="glass"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '16px',
                  borderRadius: '8px',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  transition: 'all 0.3s'
                }}
                whileHover={{ scale: 1.02, y: -2 }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <FileText size={20} color="#3b82f6" />
                  <div>
                    <p style={{ fontWeight: '500', color: 'white', marginBottom: '4px' }}>{getFileName(doc.file_path)}</p>
                    <p style={{ fontSize: '14px', color: 'rgba(255, 255, 255, 0.6)' }}>
                      块数: {doc.chunk_count} | 
                      最后修改: {doc.last_modified || '未知'}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default DocumentsTab