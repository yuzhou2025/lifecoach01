// API服务
import { API_CONFIG, apiUtils } from '../config/api.js';

export class ApiService {
    // 发送消息到DeepSeek R1
    static async sendMessage(message) {
        try {
            // 验证API配置
            apiUtils.validateConfig();

            // 构建请求数据
            const requestData = {
                prompt: message,
                max_tokens: API_CONFIG.MAX_TOKENS,
                temperature: API_CONFIG.TEMPERATURE
            };

            // 发送请求
            const response = await fetch(API_CONFIG.DEEPSEEK_API_ENDPOINT, {
                method: 'POST',
                headers: apiUtils.getHeaders(),
                body: JSON.stringify(requestData),
                timeout: API_CONFIG.REQUEST_TIMEOUT
            });

            if (!response.ok) {
                throw new Error(API_CONFIG.ERROR_MESSAGES.API_ERROR);
            }

            const data = await response.json();
            return {
                success: true,
                message: data.choices[0].text,
                suggestions: this.extractSuggestions(data.choices[0].text)
            };

        } catch (error) {
            if (error.name === 'AbortError') {
                return { success: false, error: API_CONFIG.ERROR_MESSAGES.TIMEOUT_ERROR };
            }
            return { success: false, error: error.message };
        }
    }

    // 从AI响应中提取建议
    static extractSuggestions(text) {
        // 这里可以根据实际需求实现建议提取逻辑
        // 例如：通过关键词、标点符号等方式识别建议内容
        const suggestions = [];
        const sentences = text.split(/[.。!！?？]/).filter(s => s.trim());
        
        for (const sentence of sentences) {
            if (sentence.includes('建议') || sentence.includes('推荐') || 
                sentence.includes('可以') || sentence.includes('不妨')) {
                suggestions.push(sentence.trim());
            }
        }

        return suggestions;
    }
}