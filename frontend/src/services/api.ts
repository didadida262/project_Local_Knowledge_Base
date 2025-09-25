import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

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

// 上传文档
export const uploadDocument = async (formData: FormData) => {
  const response = await api.post('/upload_document', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
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