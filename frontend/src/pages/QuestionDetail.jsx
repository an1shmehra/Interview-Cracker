import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { questionsAPI } from '../services/api';
import { ArrowLeft, Building2, Tag, ExternalLink } from 'lucide-react';

export default function QuestionDetail() {
    const { id } = useParams();
    const [question, setQuestion] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchQuestion();
    }, [id]);

    const fetchQuestion = async () => {
        setLoading(true);
        try {
            const response = await questionsAPI.getQuestion(id);
            setQuestion(response.data);
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

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-gray-600 font-medium">Loading question...</p>
                </div>
            </div>
        );
    }

    if (!question) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">Question not found</h2>
                    <Link to="/questions" className="text-blue-600 hover:text-blue-700">
                        ê Back to questions
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="px-8 py-10">
                <div className="max-w-4xl mx-auto">
                    {/* Back button */}
                    <Link
                        to="/questions"
                        className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-8 transition-colors"
                    >
                        <ArrowLeft size={20} />
                        <span className="font-medium">Back to Questions</span>
                    </Link>

                    {/* Question Card */}
                    <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm">
                        {/* Title */}
                        <h1 className="text-3xl font-bold text-gray-900 mb-6">
                            {question.title}
                        </h1>

                        {/* Metadata */}
                        <div className="flex flex-wrap gap-2 mb-8 pb-6 border-b border-gray-200">
                            <span className="px-3 py-1.5 bg-blue-50 text-blue-700 text-sm font-medium rounded-lg border border-blue-200">
                                {question.category}
                            </span>

                            <span className={`px-3 py-1.5 text-sm font-medium rounded-lg border ${difficultyColors[question.difficulty]}`}>
                                {question.difficulty}
                            </span>

                            {question.url && (
                                <a
                                    href={question.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="px-3 py-1.5 bg-gray-50 text-gray-700 text-sm font-medium rounded-lg border border-gray-200 hover:bg-gray-100 transition-colors inline-flex items-center gap-1.5"
                                >
                                    <ExternalLink size={14} />
                                    {question.source || 'View Source'}
                                </a>
                            )}
                        </div>

                        {/* Companies */}
                        {question.companies && question.companies.length > 0 && (
                            <div className="mb-6">
                                <div className="flex items-center gap-2 mb-3">
                                    <Building2 size={18} className="text-gray-600" />
                                    <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wide">
                                        Asked by Companies
                                    </h3>
                                </div>
                                <div className="flex flex-wrap gap-2">
                                    {question.companies.map((company, i) => (
                                        <span
                                            key={i}
                                            className="px-3 py-1.5 bg-gray-50 text-gray-700 text-sm font-medium rounded-lg border border-gray-200"
                                        >
                                            {company.name}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Topics */}
                        {question.topics && question.topics.length > 0 && (
                            <div className="mb-8">
                                <div className="flex items-center gap-2 mb-3">
                                    <Tag size={18} className="text-gray-600" />
                                    <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wide">
                                        Topics
                                    </h3>
                                </div>
                                <div className="flex flex-wrap gap-2">
                                    {question.topics.map((topic, i) => (
                                        <span
                                            key={i}
                                            className="px-3 py-1.5 bg-indigo-50 text-indigo-700 text-sm font-medium rounded-lg border border-indigo-200"
                                        >
                                            {topic.name}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Question Content */}
                        {question.content && (
                            <div className="prose prose-lg max-w-none">
                                <h3 className="text-lg font-semibold text-gray-900 mb-4">Problem Description</h3>
                                <div
                                    className="text-gray-700 leading-relaxed"
                                    dangerouslySetInnerHTML={{ __html: question.content }}
                                />
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
