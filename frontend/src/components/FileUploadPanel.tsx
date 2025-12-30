import React, { useState, useRef } from 'react'
import { Upload, FileText, CheckCircle, AlertCircle, Loader } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { uploadDocument } from '../services/api'

interface FileUploadPanelProps {
  onUploadSuccess: () => void
}

const FileUploadPanel: React.FC<FileUploadPanelProps> = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (!files || files.length === 0) return

    setUploading(true)
    setMessage(null)
    setUploadProgress(0)

    try {
      // 创建FormData，添加所有文件
      const formData = new FormData()
      const totalFiles = files.length
      
      // 添加所有文件到FormData
      Array.from(files).forEach((file) => {
        formData.append('files', file)
      })
      
      try {
        const result = await uploadDocument(formData)
        if (result.success) {
          setUploadProgress(100)
          const processedCount = result.processed_count || 0
          const errorCount = result.error_count || 0
          
          if (errorCount > 0) {
            setMessage({ 
              type: 'error', 
              text: `成功处理 ${processedCount} 个文件，失败 ${errorCount} 个` 
            })
          } else {
            setMessage({ 
              type: 'success', 
              text: `成功处理 ${processedCount} 个文件` 
            })
          }
          
          onUploadSuccess()
          // 3秒后清除成功消息
          setTimeout(() => {
            setMessage(null)
          }, 3000)
        } else {
          setMessage({ 
            type: 'error', 
            text: result.error || '上传失败' 
          })
        }
      } catch (error) {
        setMessage({ 
          type: 'error', 
          text: '上传失败，请稍后重试' 
        })
      }
    } catch (error) {
      setMessage({ type: 'error', text: '上传失败，请稍后重试' })
    } finally {
      setUploading(false)
      setUploadProgress(0)
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
          <p className="text-white/60 text-[10px]">上传文件构建知识库</p>
        </div>
      </div>

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
              <p className="text-white font-medium mb-1.5 text-xs">上传中...</p>
              <div className="w-full bg-white/10 rounded-full h-1.5 overflow-hidden">
                <motion.div
                  className="h-full bg-gradient-to-r from-blue-500 to-cyan-500"
                  initial={{ width: 0 }}
                  animate={{ width: `${uploadProgress}%` }}
                  transition={{ duration: 0.3 }}
                />
              </div>
              <p className="text-white/60 text-[10px] mt-1.5">{uploadProgress.toFixed(0)}%</p>
            </div>
          </div>
        ) : (
          <>
            <Upload size={28} className="text-white/40 mx-auto mb-2" />
            <p className="text-white/80 mb-1 font-medium text-xs">拖拽文件夹到此处或点击选择</p>
            <p className="text-white/60 text-[10px] mb-2">
              支持格式: TXT, MD, PDF, DOCX, HTML
            </p>
            <label
              htmlFor="file-upload-input"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-gradient-to-r from-blue-500 to-cyan-500 text-white text-xs font-medium cursor-pointer hover:scale-105 transition-transform"
            >
              <FileText size={12} />
              选择文件
            </label>
          </>
        )}
      </div>

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
            <p className={`text-xs ${
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

