import React, { useState, useRef, useEffect } from 'react'
import { Upload, FileText, CheckCircle, AlertCircle, Loader, Trash2 } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { uploadDocument, rebuildKnowledgeBase, getDocuments } from '../services/api'

interface FileUploadPanelProps {
  onUploadSuccess: () => void
  onResetSuccess?: () => void // 重置知识库成功后的回调
}

interface Document {
  file_path: string
  file_name: string
  chunk_count: number
  word_count: number
  file_size: number
}

const FileUploadPanel: React.FC<FileUploadPanelProps> = ({ onUploadSuccess, onResetSuccess }) => {
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [resetting, setResetting] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)
  const [documents, setDocuments] = useState<Document[]>([])
  const [loadingDocuments, setLoadingDocuments] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // 加载文档列表
  const loadDocuments = async () => {
    try {
      setLoadingDocuments(true)
      const data = await getDocuments()
      setDocuments(data.documents || [])
    } catch (error) {
      console.error('加载文档列表失败:', error)
      setDocuments([])
    } finally {
      setLoadingDocuments(false)
    }
  }

  // 组件挂载时加载文档列表
  useEffect(() => {
    loadDocuments()
  }, [])

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (!files || files.length === 0) return

    setUploading(true)
    setMessage(null)
    setUploadProgress(0)

    try {
      const totalFiles = files.length
      let processedCount = 0
      let failedCount = 0
      const failedFiles: string[] = []
      
      // 逐个文件上传，实时更新进度
      for (let i = 0; i < totalFiles; i++) {
        const file = files[i]
        
        // 检查文件扩展名
        const fileExt = '.' + file.name.split('.').pop()?.toLowerCase()
        const supportedExtensions = ['.txt', '.md', '.pdf', '.docx', '.html', '.htm']
        if (!supportedExtensions.includes(fileExt)) {
          failedCount++
          failedFiles.push(file.name)
          // 更新进度（跳过不支持的文件也算进度）
          setUploadProgress(((i + 1) / totalFiles) * 100)
          continue
        }
        
        try {
          // 创建FormData，每次只添加一个文件
          const formData = new FormData()
          formData.append('files', file)
          
          const result = await uploadDocument(formData)
          console.log(`文件 ${i + 1}/${totalFiles} 上传响应:`, result) // 调试日志
          
          if (result && result.success) {
            processedCount += result.processed_count || 1
            if (result.error_count && result.error_count > 0) {
              failedCount += result.error_count
            }
          } else {
            failedCount++
            failedFiles.push(file.name)
          }
        } catch (error: any) {
          console.error(`文件 ${i + 1}/${totalFiles} 上传异常:`, error) // 调试日志
          failedCount++
          failedFiles.push(file.name)
        }
        
        // 更新进度：已处理的文件数（包括成功和失败）/ 总文件数
        setUploadProgress(((i + 1) / totalFiles) * 100)
      }
      
      // 所有文件处理完成
      if (processedCount > 0) {
        if (failedCount > 0) {
          setMessage({ 
            type: 'error', 
            text: `成功处理 ${processedCount} 个文件，失败 ${failedCount} 个` 
          })
        } else {
          setMessage({ 
            type: 'success', 
            text: `成功处理 ${processedCount} 个文件` 
          })
        }
        
          onUploadSuccess()
          // 刷新文档列表
          await loadDocuments()
          // 3秒后清除成功消息
          setTimeout(() => {
            setMessage(null)
          }, 3000)
      } else if (failedCount > 0) {
        setMessage({ 
          type: 'error', 
          text: `所有文件上传失败（${failedCount} 个）` 
        })
      } else {
        setMessage({ 
          type: 'error', 
          text: '未选择任何有效文件' 
        })
      }
    } catch (error: any) {
      console.error('上传异常:', error) // 调试日志
      setMessage({ 
        type: 'error', 
        text: error?.message || '上传失败，请稍后重试' 
      })
    } finally {
      setUploading(false)
      // 上传完成后，进度条应该已经显示100%，不需要重置
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const files = e.dataTransfer.files
    if (files.length > 0 && fileInputRef.current) {
      fileInputRef.current.files = files
      handleFileSelect({ target: { files } } as any)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const handleReset = async () => {
    if (!confirm('确定要清空知识库吗？此操作不可恢复！')) {
      return
    }

    setResetting(true)
    setMessage(null)

    try {
      const result = await rebuildKnowledgeBase()
      if (result.success) {
        setMessage({ 
          type: 'success', 
          text: '知识库已清空' 
        })
        onUploadSuccess()
        // 刷新文档列表（应该为空）
        await loadDocuments()
        // 触发问答内容重置
        if (onResetSuccess) {
          onResetSuccess()
        }
        setTimeout(() => {
          setMessage(null)
        }, 3000)
      } else {
        setMessage({ 
          type: 'error', 
          text: result.error || '清空失败' 
        })
      }
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: '清空失败，请稍后重试' 
      })
    } finally {
      setResetting(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass rounded-xl p-3 border border-white/10"
    >
      <div className="flex items-center gap-2 mb-2">
        <div className="w-7 h-7 rounded-lg bg-gradient-to-r from-blue-500 to-cyan-500 flex items-center justify-center">
          <Upload size={14} className="text-white" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-white">选择本地文件</h3>
          <p className="text-white/60 text-xs">上传文件构建知识库</p>
        </div>
      </div>

      {/* 上传控件 - 只在没有文件或正在上传时显示 */}
      {(documents.length === 0 || uploading) && (
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          className={`relative border-2 border-dashed rounded-lg p-4 text-center transition-all duration-300 ${
            uploading
              ? 'border-blue-400/50 bg-blue-500/10'
              : 'border-white/30 bg-white/5 hover:border-white/50 hover:bg-white/10'
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            webkitdirectory=""
            directory=""
            multiple
            onChange={handleFileSelect}
            disabled={uploading}
            className="hidden"
            id="file-upload-input"
          />
          
          {uploading ? (
            <div className="space-y-2">
              <Loader size={28} className="text-blue-400 mx-auto animate-spin" />
              <div>
                <p className="text-white font-medium mb-1.5 text-sm">上传中...</p>
                <div className="w-full bg-white/10 rounded-full h-1.5 overflow-hidden">
                  <motion.div
                    className="h-full bg-gradient-to-r from-blue-500 to-cyan-500"
                    initial={{ width: 0 }}
                    animate={{ width: `${uploadProgress}%` }}
                    transition={{ duration: 0.3 }}
                  />
                </div>
                <p className="text-white/60 text-xs mt-1.5">{uploadProgress.toFixed(0)}%</p>
              </div>
            </div>
          ) : (
            <>
              <Upload size={28} className="text-white/40 mx-auto mb-2" />
            <p className="text-white/80 mb-1 font-medium text-sm">拖拽文件夹到此处或点击选择</p>
            <p className="text-white/60 text-xs mb-2">
              支持格式: TXT, MD, PDF, DOCX, HTML
            </p>
              <label
                htmlFor="file-upload-input"
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-gradient-to-r from-blue-500 to-cyan-500 text-white text-sm font-medium cursor-pointer hover:scale-105 transition-transform"
              >
                <FileText size={12} />
                选择文件
              </label>
            </>
          )}
        </div>
      )}

      {/* 已上传文件列表 */}
      {documents.length > 0 && (
        <div className="mt-3 space-y-2">
          <div className="flex items-center gap-1.5">
            <CheckCircle size={12} className="text-green-400" />
            <p className="text-sm font-medium text-white/80">已上传文件 ({documents.length})</p>
          </div>
          <div className="max-h-32 overflow-y-auto space-y-1.5 pr-1">
            {documents.map((doc, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: -5 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center gap-2 p-2 rounded-lg bg-white/5 border border-white/10"
              >
                <FileText size={12} className="text-blue-400 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-xs text-white/90 truncate" title={doc.file_name}>
                    {doc.file_name}
                  </p>
                  <p className="text-xs text-white/60">
                    {doc.chunk_count} 块 · {(doc.file_size / 1024).toFixed(1)} KB
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Reset Button - 只在有文件时显示 */}
      {documents.length > 0 && (
        <motion.button
          onClick={handleReset}
          disabled={resetting || uploading}
          className="mt-3 w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-gradient-to-r from-red-500/20 to-orange-500/20 border border-red-500/30 text-red-400 text-sm font-medium hover:from-red-500/30 hover:to-orange-500/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          whileHover={{ scale: resetting || uploading ? 1 : 1.02 }}
          whileTap={{ scale: resetting || uploading ? 1 : 0.98 }}
        >
          {resetting ? (
            <>
              <Loader size={12} className="animate-spin" />
              清空中...
            </>
          ) : (
            <>
              <Trash2 size={12} />
              重置知识库
            </>
          )}
        </motion.button>
      )}

      {/* Message */}
      <AnimatePresence>
        {message && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className={`mt-2 flex items-center gap-1.5 p-2 rounded-lg ${
              message.type === 'success'
                ? 'bg-green-500/10 border border-green-500/30'
                : 'bg-red-500/10 border border-red-500/30'
            }`}
          >
            {message.type === 'success' ? (
              <CheckCircle size={12} className="text-green-400" />
            ) : (
              <AlertCircle size={12} className="text-red-400" />
            )}
            <p className={`text-sm ${
              message.type === 'success' ? 'text-green-400' : 'text-red-400'
            }`}>
              {message.text}
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

export default FileUploadPanel

