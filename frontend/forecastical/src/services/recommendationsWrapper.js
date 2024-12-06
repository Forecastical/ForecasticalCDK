// src/services/recommendationsWrapper.js

const API_URL = 'http://localhost:8000';

async function makeRequest(endpoint, username, password) {
    console.log(`Making request to ${endpoint} for user ${username}`);
    
    try {
        const requestBody = JSON.stringify({ username, password });
        console.log('Request body:', requestBody);

        const response = await fetch(`${API_URL}/${endpoint}`, {
            method: 'POST',  // Changed to POST
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: requestBody
        });

        console.log(`Response status:`, response.status);
        const responseText = await response.text();
        console.log(`Raw response:`, responseText);

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}: ${responseText}`);
        }

        return JSON.parse(responseText);
    } catch (error) {
        console.error(`Error in ${endpoint}:`, error);
        throw error;
    }
}

export async function getClothingRecommendations(username, password) {
    try {
        const data = await makeRequest('clothes_reccomended', username, password);
        console.log('Clothing data:', data);
        return [data.prediction, data.prediction2, data.prediction3].filter(Boolean);
    } catch (error) {
        console.error('Error in getClothingRecommendations:', error);
        throw error;
    }
}

export async function getToolRecommendations(username, password) {
    try {
        const data = await makeRequest('tools_reccomended', username, password);
        console.log('Tools data:', data);
        return [data.prediction, data.prediction2].filter(Boolean);
    } catch (error) {
        console.error('Error in getToolRecommendations:', error);
        throw error;
    }
}

export async function getActivityRecommendations(username, password) {
    try {
        const data = await makeRequest('activities_reccomended', username, password);
        console.log('Activities data:', data);
        return [data.prediction, data.prediction2, data.prediction3].filter(Boolean);
    } catch (error) {
        console.error('Error in getActivityRecommendations:', error);
        throw error;
    }
}