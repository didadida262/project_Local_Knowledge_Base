# Fly.io 配置指南

## 默认配置说明

在 Fly.io 的配置界面中，以下设置可以保持默认：

### ✅ 保持默认的设置

1. **Network - Internal port: 5000**
   - ✅ **保持 5000**：这与后端代码中的端口配置一致
   - 不需要修改

2. **CPU & Memory - VM Sizes: shared-cpu-1x**
   - ✅ **保持 shared-cpu-1x**：这是免费额度，足够运行本项目
   - 如果后续需要更多性能，可以升级

3. **CPU & Memory - VM Memory: 1GB**
   - ✅ **保持 1GB**：对于本项目来说足够
   - AI 模型加载后大约占用 200-300MB，1GB 内存足够

4. **Postgres: none**
   - ✅ **保持 none**：本项目不需要数据库
   - 知识库数据存储在文件系统中

5. **Tigris Object Storage: Disabled**
   - ✅ **保持 Disabled**：除非你需要持久化存储上传的文件
   - 默认情况下，文件存储在服务实例中
   - 如果服务重启，上传的文件可能会丢失（但知识库数据会保留）

6. **Redis: Disabled**
   - ✅ **保持 Disabled**：本项目不需要 Redis 缓存

### ⚠️ 可能需要调整的设置

1. **Region（区域）**
   - 选择离你最近的区域，以获得更好的性能
   - 例如：如果在中国，可以选择 `nrt`（东京）或 `sin`（新加坡）
   - 如果在美国，可以选择 `sjc`（旧金山）或 `iad`（弗吉尼亚）

2. **VM Memory（如果遇到内存不足）**
   - 如果部署后出现内存不足错误，可以升级到 2GB
   - 但免费额度只有 1GB，升级需要付费

## 推荐配置

### 最小配置（免费）
```
Region: nrt (Tokyo) 或 sin (Singapore) 或 sjc (San Francisco)
Network - Internal port: 5000
VM Sizes: shared-cpu-1x
VM Memory: 1GB
Postgres: none
Tigris Object Storage: Disabled
Redis: Disabled
```

### 如果遇到问题

**内存不足错误**：
- 升级到 2GB 内存（需要付费）
- 或优化代码，减少内存使用

**响应慢**：
- 升级到 dedicated-cpu（需要付费）
- 或选择更近的区域

## 部署后检查

部署完成后，检查：
1. 服务是否正常启动
2. 内存使用是否在 1GB 以内
3. 响应速度是否正常

如果一切正常，默认配置就足够了！

