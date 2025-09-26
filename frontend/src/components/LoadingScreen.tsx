import React from 'react'
import { motion } from 'framer-motion'
import { Loader2, Brain, Zap, Database } from 'lucide-react'

interface LoadingScreenProps {
  message?: string
  progress?: number
}

const LoadingScreen: React.FC<LoadingScreenProps> = ({ 
  message = "正在初始化系统...", 
  progress = 0 
}) => {
  const loadingSteps = [
    { icon: Database, text: "加载向量数据库", progress: 20 },
    { icon: Brain, text: "初始化AI模型", progress: 60 },
    { icon: Zap, text: "优化搜索性能", progress: 90 },
  ]

  return (
    <div className="min-h-screen bg-black flex items-center justify-center relative overflow-hidden">
      {/* 背景装饰 */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900" />
        
        {/* 动态光效 */}
        <motion.div
          className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-full blur-3xl"
          animate={{
            x: [0, 100, 0],
            y: [0, -50, 0],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        <motion.div
          className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gradient-to-r from-pink-500/20 to-cyan-500/20 rounded-full blur-3xl"
          animate={{
            x: [0, -100, 0],
            y: [0, 50, 0],
            scale: [1, 1.1, 1],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 2
          }}
        />
      </div>

      {/* 主内容 */}
      <div className="relative z-10 text-center">
        {/* Logo和标题 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="mb-12"
        >
          <div className="relative mb-8">
            <motion.div
              className="w-20 h-20 rounded-2xl bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center mx-auto"
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            >
              <Brain size={40} className="text-white" />
            </motion.div>
            <motion.div
              className="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-gradient-to-r from-yellow-400 to-orange-400 flex items-center justify-center"
              animate={{ 
                scale: [1, 1.2, 1],
                rotate: [0, 180, 360]
              }}
              transition={{ 
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            >
              <Zap size={16} className="text-white" />
            </motion.div>
          </div>
          
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-4">
            本地向量知识库
          </h1>
          <p className="text-white/60 text-lg">AI驱动的智能文档检索系统</p>
        </motion.div>

        {/* 加载动画 */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="glass rounded-3xl p-8 max-w-md mx-auto border border-white/10"
        >
          <div className="flex items-center justify-center mb-6">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            >
              <Loader2 size={32} className="text-blue-400" />
            </motion.div>
          </div>
          
          <h3 className="text-xl font-semibold text-white mb-4">{message}</h3>
          
          {/* 进度条 */}
          <div className="w-full bg-white/10 rounded-full h-2 mb-6">
            <motion.div
              className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
          
          {/* 加载步骤 */}
          <div className="space-y-3">
            {loadingSteps.map((step, index) => {
              const Icon = step.icon
              const isActive = progress >= step.progress
              const isCompleted = progress > step.progress
              
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.2 }}
                  className={`flex items-center gap-3 p-3 rounded-xl transition-all duration-300 ${
                    isCompleted 
                      ? 'bg-green-500/20 border border-green-500/30' 
                      : isActive 
                        ? 'bg-blue-500/20 border border-blue-500/30' 
                        : 'bg-white/5 border border-white/10'
                  }`}
                >
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    isCompleted 
                      ? 'bg-green-500' 
                      : isActive 
                        ? 'bg-blue-500' 
                        : 'bg-white/20'
                  }`}>
                    {isCompleted ? (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: "spring", bounce: 0.4 }}
                      >
                        ✓
                      </motion.div>
                    ) : (
                      <Icon size={16} className="text-white" />
                    )}
                  </div>
                  <span className={`font-medium ${
                    isCompleted 
                      ? 'text-green-400' 
                      : isActive 
                        ? 'text-blue-400' 
                        : 'text-white/60'
                  }`}>
                    {step.text}
                  </span>
                </motion.div>
              )
            })}
          </div>
        </motion.div>

        {/* 提示信息 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1 }}
          className="mt-8 text-center"
        >
          <p className="text-white/60 text-sm">
            正在初始化AI模型，这可能需要几分钟时间
          </p>
          <p className="text-white/40 text-xs mt-2">
            模型完全加载后才会进入系统，请耐心等待
          </p>
        </motion.div>
      </div>
    </div>
  )
}

export default LoadingScreen
