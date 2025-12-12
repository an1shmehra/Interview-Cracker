import { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { questionsAPI } from '../services/api';
import { Search, Check, Bookmark } from 'lucide-react';
import { useProgress } from '../context/ProgressContext';
import DemoModeBanner from '../components/DemoModeBanner';

export default function QuestionsPage() {
    const [searchParams] = useSearchParams();
    const [questions, setQuestions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const { getQuestionProgress, isGuestMode } = useProgress();

    const category = searchParams.get('category') || '';

    // Utility function to clean question titles
    const cleanTitle = (title) => {
        // Remove "Question X:" or "Question X." prefix
        return title.replace(/^Question\s+\d+[:.]\s*/i, '');
    };

    useEffect(() => {
        fetchQuestions();
    }, [category, search]);

    const fetchQuestions = async () => {
        setLoading(true);
        try {
            const params = { limit: 200 }; // Get all questions in category
            if (category) params.category = category;
            if (search) params.search = search;

            const response = await questionsAPI.getQuestions(params);
            setQuestions(response.data.questions);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    const difficultyColors = {
        Easy: 'bg-green-50 text-green-700 border-green-200',
        Medium: 'bg-yellow-50 text-yellow-700 border-yellow-200',
        Hard: 'bg-red-50 text-red-700 border-red-200',
        Unknown: 'bg-gray-50 text-gray-700 border-gray-200',
    };

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="px-8 py-10">
                <div className="max-w-6xl mx-auto">
                    {/* Header */}
                    <div className="mb-10">
                        <h1 className="text-4xl font-bold text-gray-900 mb-3">
                            {category || 'All Questions'}
                        </h1>
                        <p className="text-lg text-gray-600">Browse and practice curated interview questions from top tech companies</p>
                    </div>

                    {/* Search */}
                    <div className="mb-8">
                        <div className="relative max-w-xl">
                            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
                            <input
                                type="text"
                                placeholder="Search questions by title, company, or topic..."
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                                className="w-full pl-12 pr-4 py-3.5 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm transition-all"
                            />
                        </div>
                    </div>

                    {/* Demo Mode Banner */}
                    {isGuestMode && <DemoModeBanner />}

                    {/* Questions */}
                    {loading ? (
                        <div className="flex flex-col items-center justify-center py-32">
                            <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
                            <p className="text-gray-600 font-medium">Loading questions...</p>
                        </div>
                    ) : questions.length === 0 ? (
                        <div className="text-center py-32">
                            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                <Search className="text-gray-400" size={24} />
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">No questions found</h3>
                            <p className="text-gray-600">Try adjusting your search or filters</p>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {questions.map((question) => {
                                const progress = getQuestionProgress(question.id);
                                return (
                                <Link key={question.id} to={`/questions/${question.id}`}>
                                    <div className="group p-6 bg-white border border-gray-200 rounded-xl hover:border-blue-300 hover:shadow-lg transition-all duration-200 relative">
                                        {/* Progress Indicators */}
                                        <div className="absolute top-4 right-4 flex gap-2">
                                            {progress.status === 'completed' && (
                                                <div className="w-7 h-7 bg-green-600 rounded-full flex items-center justify-center" title="Completed">
                                                    <Check size={16} className="text-white" />
                                                </div>
                                            )}
                                            {progress.bookmarked && (
                                                <div className="w-7 h-7 bg-blue-600 rounded-full flex items-center justify-center" title="Bookmarked">
                                                    <Bookmark size={14} className="text-white" fill="white" />
                                                </div>
                                            )}
                                        </div>

                                        <h3 className="text-lg font-semibold text-gray-900 mb-4 group-hover:text-blue-600 transition-colors pr-16">
                                            {cleanTitle(question.title)}
                                        </h3>

                                        <div className="flex flex-wrap gap-2">
                                            <span className="px-3 py-1.5 bg-blue-50 text-blue-700 text-sm font-medium rounded-lg border border-blue-200">
                                                {question.category}
                                            </span>

                                            {question.difficulty && question.difficulty !== 'Unknown' && (
                                                <span className={`px-3 py-1.5 text-sm font-medium rounded-lg border ${difficultyColors[question.difficulty]}`}>
                                                    {question.difficulty}
                                                </span>
                                            )}

                                            {question.companies?.slice(0, 3).map((company, i) => (
                                                <span key={i} className="px-3 py-1.5 bg-gray-50 text-gray-700 text-sm font-medium rounded-lg border border-gray-200">
                                                    {company.name}
                                                </span>
                                            ))}

                                            {question.companies?.length > 3 && (
                                                <span className="px-3 py-1.5 bg-gray-50 text-gray-500 text-sm font-medium rounded-lg border border-gray-200">
                                                    +{question.companies.length - 3} more
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                </Link>
                                );
                            })}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
