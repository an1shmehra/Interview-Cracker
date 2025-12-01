import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const questionsAPI = {
    getQuestions: (params = {}) => api.get('/questions', { params }),
    getQuestion: (id) => api.get(`/questions/${id}`),
    getCategories: () => api.get('/categories'),
    getCompanies: () => api.get('/companies'),
    getTopics: () => api.get('/topics'),
    getStats: () => api.get('/stats'),
};

export default api;