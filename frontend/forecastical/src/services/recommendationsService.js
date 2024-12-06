// src/services/recommendationsService.js
import axios from 'axios';

const API_URL = 'http://localhost:8000';

class RecommendationsService {
    constructor() {
        this.client = axios.create({
            baseURL: API_URL,
            timeout: 5000,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
    }

    async getClothingRecommendations(username, password) {
        const response = await this.client.get('/clothes_reccomended', {
            data: { username, password }
        });
        return [response.data.prediction, response.data.prediction2, response.data.prediction3];
    }

    async getToolRecommendations(username, password) {
        const response = await this.client.get('/tools_reccomended', {
            data: { username, password }
        });
        return [response.data.prediction, response.data.prediction2];
    }

    async getActivityRecommendations(username, password) {
        const response = await this.client.get('/activities_reccomended', {
            data: { username, password }
        });
        return [response.data.prediction, response.data.prediction2, response.data.prediction3];
    }
}

const recommendationsService = new RecommendationsService();
export { recommendationsService };