# React前端设置指南

## 🚀 快速开始

### 1. 安装Node.js

下载并安装 [Node.js](https://nodejs.org/) (推荐版本 16+)

### 2. 安装前端依赖

```bash
cd frontend
npm install
```

### 3. 启动开发服务器

```bash
npm run dev
```

### 4. 构建生产版本

```bash
npm run build
```

## 🛠️ 开发工具

### 推荐VS Code插件

- **ES7+ React/Redux/React-Native snippets**: React代码片段
- **TypeScript Importer**: 自动导入TypeScript类型
- **Tailwind CSS IntelliSense**: Tailwind CSS智能提示
- **Auto Rename Tag**: 自动重命名标签
- **Bracket Pair Colorizer**: 括号配对高亮

### 代码格式化

```bash
# 安装Prettier
npm install -D prettier

# 格式化代码
npx prettier --write src/
```

## 📁 项目结构

```
frontend/
├── src/
│   ├── components/          # React组件
│   │   ├── StatsCard.tsx   # 统计卡片
│   │   ├── SearchTab.tsx   # 搜索标签页
│   │   ├── QATab.tsx       # 问答标签页
│   │   └── DocumentsTab.tsx # 文档管理标签页
│   ├── services/           # API服务
│   │   └── api.ts          # API接口
│   ├── App.tsx             # 主应用组件
│   ├── main.tsx            # 应用入口
│   └── index.css           # 全局样式
├── public/                 # 静态资源
├── package.json           # 依赖配置
├── vite.config.ts         # Vite配置
├── tsconfig.json          # TypeScript配置
└── build.py               # 构建脚本
```

## 🎨 样式指南

### Tailwind CSS类名

```tsx
// 按钮样式
<button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
  按钮
</button>

// 卡片样式
<div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
  卡片内容
</div>

// 响应式布局
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  响应式网格
</div>
```

### 组件样式

```tsx
// 使用clsx合并类名
import clsx from 'clsx'

const buttonClass = clsx(
  'px-4 py-2 rounded-lg',
  {
    'bg-blue-600 text-white': variant === 'primary',
    'bg-gray-200 text-gray-800': variant === 'secondary'
  }
)
```

## 🔧 开发技巧

### 1. 组件开发

```tsx
// 定义Props接口
interface ButtonProps {
  variant: 'primary' | 'secondary'
  size: 'sm' | 'md' | 'lg'
  onClick: () => void
  children: React.ReactNode
}

// 使用默认值
const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  onClick,
  children
}) => {
  return (
    <button
      className={clsx(
        'px-4 py-2 rounded-lg',
        {
          'bg-blue-600 text-white': variant === 'primary',
          'bg-gray-200 text-gray-800': variant === 'secondary'
        }
      )}
      onClick={onClick}
    >
      {children}
    </button>
  )
}
```

### 2. API调用

```tsx
// 使用async/await
const [data, setData] = useState(null)
const [loading, setLoading] = useState(false)

const fetchData = async () => {
  setLoading(true)
  try {
    const result = await api.getData()
    setData(result)
  } catch (error) {
    console.error('API调用失败:', error)
  } finally {
    setLoading(false)
  }
}
```

### 3. 错误处理

```tsx
// 错误边界组件
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true }
  }

  render() {
    if (this.state.hasError) {
      return <div>出现错误，请刷新页面</div>
    }
    return this.props.children
  }
}
```

## 🚀 部署

### 1. 构建生产版本

```bash
npm run build
```

### 2. 集成到Flask

```bash
# 运行构建脚本
python frontend/build.py
```

### 3. 启动后端

```bash
python web_interface.py
```

## 📝 注意事项

- 确保后端API运行在端口5000
- 前端开发服务器运行在端口3000
- 使用代理配置连接前后端
- 支持热重载开发体验
- 保持组件样式的一致性
- 使用TypeScript类型检查
