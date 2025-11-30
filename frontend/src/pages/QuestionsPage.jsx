import { useEffect, useState } from 'react';
import { questionsAPI } from '../services/api';
import { Link } from 'react-router-dom';
import { Search, Filter } from 'lucide-react';

function QuestionsPage() {
    const [questions, setQuestions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [category, setCategory] = useState('');
    const [difficulty, setDifficulty] = useState('');
    const [search, setSearch] = useState('');

    useEffect(() => {
        fetchQuestions();
    }, [category, difficulty, search]);

    const fetchQuestions = async () => {
        setLoading(true);
        try {
            const params = {};
            if (category) params.category = category;
            if (difficulty) params.difficulty = difficulty;
            if (search) params.search = search;

            const response = await questionsAPI.getQuestions(params);
            setQuestions(response.data.questions);
        } catch (error) {
            console.error('Error fetching questions:', error);
        } finally {
            setLoading(false);
        }
    };

    const difficultyColors = {
        Easy: 'text-green-600 bg-green-100',
        Medium: 'text-yellow-600 bg-yellow-100',
        Hard: 'text-red-600 bg-red-100',
        Unknown: 'text-gray-600 bg-gray-100',
    };

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="container mx-auto px-4">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">
                        Practice Questions
                    </h1>

                    {/* Filters */}
                    <div className="flex flex-wrap gap-4">
                        {/* Search */}
                        <div className="flex-1 min-w-[300px]">
                            <div className="relative">
                                <Search className="absolute left-3 top-3 text-gray-400" size={20} />
                                <input
                                    type="text"
                                    placeholder="Search questions..."
                                    value={search}
                                    onChange={(e) => setSearch(e.target.value)}
                                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                />
                            </div>
                        </div>

                        {/* Category Filter */}
                        <select
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="">All Categories</option>
                            <option value="DSA">DSA</option>
                            <option value="System Design">System Design</option>
                            <option value="Behavioral">Behavioral</option>
                        </select>

                        {/* Difficulty Filter */}
                        <select
                            value={difficulty}
                            onChange={(e) => setDifficulty(e.target.value)}
                            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="">All Difficulties</option>
                            <option value="Easy">Easy</option>
                            <option value="Medium">Medium</option>
                            <option value="Hard">Hard</option>
                        </select>
                    </div>
                </div>

                {/* Questions List */}
                {loading ? (
                    <div className="flex justify-center py-12">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                    </div>
                ) : (
                    <div className="space-y-4">
                        {questions.map((question) => (
                            <Link
                                key={question.id}
                                to={`/questions/${question.id}`}
                                className="block bg-white rounded-lg shadow hover:shadow-lg transition p-6"
                            >
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <h3 className="text-xl font-semibold text-gray-900 mb-2">
                                            {question.title}
                                        </h3>
                                        <div className="flex items-center gap-3 text-sm">
                                            <span className="px-3 py-1 bg-blue-100 text-blue-600 rounded-full">
                                                {question.category}
                                            </span>
                                            <span className={`px-3 py-1 rounded-full ${difficultyColors[question.difficulty]}`}>
                                                {question.difficulty}
                                            </span>
                                            {question.companies?.length > 0 && (
                                                <span className="text-gray-600">
                                                    {question.companies.slice(0, 3).map(c => c.name).join(', ')}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

export default QuestionsPage;