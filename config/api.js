// API配置文件

export const API_CONFIG = {
    // DeepSeek R1 API配置
    DEEPSEEK_API_KEY: process.env.VOLC_ACCESSKEY || '',  // 从环境变量读取API密钥
    DEEPSEEK_API_SECRET: process.env.VOLC_SECRETKEY || '',  // 从环境变量读取API密钥
    DEEPSEEK_API_ENDPOINT: 'https://api.deepseek.com/v1',  // 请替换为实际的API端点
    
    // API请求配置
    REQUEST_TIMEOUT: 30000,  // 请求超时时间（毫秒）
    MAX_TOKENS: 2000,       // 每次请求的最大token数
    TEMPERATURE: 0.7,       // 响应的随机性（0-1）
    
    // 错误消息
    ERROR_MESSAGES: {
        NETWORK_ERROR: '网络连接错误，请检查网络后重试',
        API_ERROR: 'API调用失败，请稍后重试',
        TIMEOUT_ERROR: '请求超时，请重试'
    }
};

// API工具函数
export const apiUtils = {
    // 检查API配置是否有效
    validateConfig() {
        if (!API_CONFIG.DEEPSEEK_API_KEY || API_CONFIG.DEEPSEEK_API_KEY === 'your_api_key_here') {
            throw new Error('请配置有效的API密钥');
        }
    },
    
    // 构建API请求头
    getHeaders() {
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${API_CONFIG.DEEPSEEK_API_KEY}`
        };
    }
};