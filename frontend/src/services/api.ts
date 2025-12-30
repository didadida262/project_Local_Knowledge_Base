import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// 添加请求拦截器，显示loading状态
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加loading状态管理
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 添加响应拦截器，处理连接错误
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // 如果是 HTTP 错误响应，尝试解析错误信息
    if (error.response) {
      const status = error.response.status
      const data = error.response.data
      
      // 如果后端返回了错误信息，保留它
      if (data && typeof data === 'object') {
        return Promise.reject({
          ...error,
          message: data.error || data.message || error.message,
          response: error.response
        })
      }
      
      // 对于 4xx 和 5xx 错误，返回更友好的错误信息
      if (status >= 400 && status < 500) {
        return Promise.reject({
          ...error,
          message: data?.error || data?.message || `请求错误 (${status})`
        })
      }
      
      if (status >= 500) {
        return Promise.reject({
          ...error,
          message: data?.error || data?.message || `服务器错误 (${status})`
        })
      }
    }
    
    if (error.code === 'ECONNREFUSED' || error.message.includes('ECONNREFUSED')) {
      // 连接被拒绝，可能是服务器还在启动
      console.warn('🔄 服务器连接被拒绝，可能是服务器正在启动...')
      throw new Error('服务器正在启动中，请稍候...')
    }
    if (error.code === 'ECONNRESET') {
      // 连接被重置，服务器可能崩溃了
      console.warn('🔄 连接被重置，服务器可能重启中...')
      throw new Error('服务器重启中，请稍候...')
    }
    return Promise.reject(error)
  }
)

// 获取知识库统计信息
export const getStats = async () => {
  const response = await api.get('/stats')
  return response.data
}

// 搜索文档
export const searchDocuments = async (query: string, topK: number = 10) => {
  const response = await api.post('/search', {
    query,
    top_k: topK
  })
  return response.data
}

// 问答
export const askQuestion = async (question: string, topK: number = 5) => {
  const response = await api.post('/ask', {
    question,
    top_k: topK
  })
  return response.data
}

// 获取文档列表
export const getDocuments = async () => {
  const response = await api.get('/documents')
  return response.data
}

// 上传文档（单个文件）
export const uploadDocument = async (formData: FormData) => {
  const response = await api.post('/upload_document', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    timeout: 300000, // 5分钟超时，处理大文件
  })
  return response.data
}

// 添加文档
export const addDocument = async (filePath: string) => {
  const response = await api.post('/add_document', {
    file_path: filePath
  })
  return response.data
}

// 重建知识库
export const rebuildKnowledgeBase = async () => {
  const response = await api.post('/rebuild')
  return response.data
}

// 健康检查
export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}
