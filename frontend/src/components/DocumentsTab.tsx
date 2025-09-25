import React, { useState, useEffect } from 'react'
import { Upload, FileText, Plus, Trash2, CheckCircle } from 'lucide-react'
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
    <div className="space-y-6">
      {/* Add Document Form */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Plus className="h-5 w-5" />
          添加本地文档
        </h3>
        <form onSubmit={handleAddDocument} className="flex gap-4">
          <input
            type="text"
            value={filePath}
            onChange={(e) => setFilePath(e.target.value)}
            placeholder="输入文件路径..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            type="submit"
            disabled={uploading || !filePath.trim()}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {uploading ? (
              <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full" />
            ) : (
              <>
                <Plus className="h-5 w-5" />
                添加
              </>
            )}
          </button>
        </form>
      </div>

      {/* Upload Documents */}
      <div className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-8">
        <div className="text-center">
          <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">上传文档</h3>
          <p className="text-gray-500 mb-4">
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
            className={`inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-lg cursor-pointer ${
              uploading
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {uploading ? (
              <div className="animate-spin h-5 w-5 border-2 border-gray-400 border-t-transparent rounded-full mr-2" />
            ) : (
              <Upload className="h-5 w-5 mr-2" />
            )}
            {uploading ? '上传中...' : '选择文件'}
          </label>
        </div>
      </div>

      {/* Message */}
      {message && (
        <div className={`rounded-lg p-4 flex items-center gap-2 ${
          message.type === 'success' 
            ? 'bg-green-50 border border-green-200 text-green-800' 
            : 'bg-red-50 border border-red-200 text-red-800'
        }`}>
          {message.type === 'success' ? (
            <CheckCircle className="h-5 w-5" />
          ) : (
            <Trash2 className="h-5 w-5" />
          )}
          {message.text}
        </div>
      )}

      {/* Documents List */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <FileText className="h-5 w-5" />
          文档列表
        </h3>
        
        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full mx-auto mb-4" />
            <p className="text-gray-500">加载中...</p>
          </div>
        ) : documents.length === 0 ? (
          <div className="text-center py-8">
            <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">暂无文档</p>
          </div>
        ) : (
          <div className="space-y-3">
            {documents.map((doc, index) => (
              <div key={index} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
                <div className="flex items-center gap-3">
                  <FileText className="h-5 w-5 text-blue-600" />
                  <div>
                    <p className="font-medium text-gray-900">{getFileName(doc.file_path)}</p>
                    <p className="text-sm text-gray-500">
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
