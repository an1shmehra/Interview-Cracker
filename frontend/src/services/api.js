import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const questionsAPI = {
    // Get all questions with filters
    getQuestions: (params = {}) => api.get('/questions', { params }),

    // Get single question
    getQuestion: (id) => api.get(`/questions/${id}`),

    // Get categories
    getCategories: () => api.get('/categories'),

    // Get companies
    getCompanies: () => api.get('/companies'),

    // Get topics
    getTopics: () => api.get('/topics'),

    // Get stats
    getStats: () => api.get('/stats'),
};

export default api;