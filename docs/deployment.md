# 环境变量配置和自动部署指南

## 环境变量配置

### 本地开发环境

1. 在项目根目录创建 `.env` 文件
2. 添加以下环境变量：
   ```
   VOLC_ACCESSKEY=你的火山引擎访问密钥
   VOLC_SECRETKEY=你的火山引擎访问密钥
   ```
3. 确保 `.env` 文件已被添加到 `.gitignore` 中，避免敏感信息泄露

### Netlify 环境变量配置

1. 登录 Netlify 控制台
2. 进入你的项目设置页面
3. 点击 "Site settings" -> "Environment variables"
4. 添加以下环境变量：
   - `VOLC_ACCESSKEY`：设置为你的火山引擎访问密钥
   - `VOLC_SECRETKEY`：设置为你的火山引擎访问密钥

## 自动部署配置

### 项目配置

当前项目已经包含了必要的 Netlify 配置文件 `netlify.toml`，其中定义了：

- 构建命令：`pip install -r requirements.txt`
- 发布目录：`public`
- Python 版本：3.9
- API 路由重定向规则
- 函数目录：`services`

### 自动部署步骤

1. 连接代码仓库
   - 在 Netlify 控制台中选择 "Site settings" -> "Build & deploy"
   - 点击 "Link to Git provider"
   - 选择你的 GitHub 仓库并授权

2. 配置部署设置
   - 构建命令和发布目录会自动从 `netlify.toml` 读取
   - 确认构建设置正确无误

3. 启用自动部署
   - 在 "Build & deploy" 设置中，确保 "Auto publish" 为开启状态
   - 每次推送到主分支时会自动触发部署

4. 部署状态监控
   - 在 Netlify 控制台的 "Deploys" 标签页查看部署状态
   - 可以查看构建日志和部署历史

## 注意事项

1. 确保本地测试通过后再推送代码
2. 定期检查环境变量是否正确配置
3. 如遇部署失败，及时查看构建日志排查问题
4. 建议在推送重要更新前先在本地环境完整测试