import { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { aiAPI } from '../services/api';
import { Send, Sparkles, BookOpen } from 'lucide-react';

export default function AIAssistant() {
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content: 'Hi! I\'m your AI interview preparation assistant. Ask me anything about technical interviews, data structures, system design, or behavioral questions. I\'ll provide guidance and recommend relevant practice questions from our database.',
            recommended_questions: []
        }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMessage = input.trim();
        setInput('');

        // Add user message
        setMessages(prev => [...prev, { role: 'user', content: userMessage, recommended_questions: [] }]);
        setLoading(true);

        try {
            const response = await aiAPI.ask(userMessage);
            const { response: aiResponse, recommended_questions } = response.data;

            // Add AI response
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: aiResponse,
                recommended_questions: recommended_questions || []
            }]);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'Sorry, I encountered an error. Please try again.',
                recommended_questions: []
            }]);
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
                <div className="max-w-4xl mx-auto">
                    {/* Header */}
                    <div className="mb-8">
                        <div className="flex items-center gap-3 mb-3">
                            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                                <Sparkles className="text-white" size={20} />
                            </div>
                            <h1 className="text-4xl font-bold text-gray-900">AI Study Assistant</h1>
                        </div>
                        <p className="text-lg text-gray-600">Get personalized interview prep guidance powered by AI</p>
                    </div>

                    {/* Chat Container */}
                    <div className="bg-white border border-gray-200 rounded-2xl shadow-sm flex flex-col" style={{ height: 'calc(100vh - 280px)' }}>
                        {/* Messages */}
                        <div className="flex-1 overflow-y-auto p-6 space-y-6">
                            {messages.map((message, index) => (
                                <div key={index}>
                                    {/* Message */}
                                    <div className={`flex gap-4 ${message.role === 'user' ? 'flex-row-reverse' : ''}`}>
                                        {/* Avatar */}
                                        <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                                            message.role === 'assistant'
                                                ? 'bg-gradient-to-br from-blue-500 to-purple-600'
                                                : 'bg-gray-700'
                                        }`}>
                                            {message.role === 'assistant' ? (
                                                <Sparkles className="text-white" size={16} />
                                            ) : (
                                                <span className="text-white text-sm font-semibold">U</span>
                                            )}
                                        </div>

                                        {/* Message Content */}
                                        <div className={`flex-1 ${message.role === 'user' ? 'flex justify-end' : ''}`}>
                                            <div className={`inline-block px-4 py-3 rounded-2xl ${
                                                message.role === 'user'
                                                    ? 'bg-blue-600 text-white'
                                                    : 'bg-gray-100 text-gray-900'
                                            }`}>
                                                <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Recommended Questions */}
                                    {message.recommended_questions && message.recommended_questions.length > 0 && (
                                        <div className="mt-4 ml-12">
                                            <div className="flex items-center gap-2 mb-3">
                                                <BookOpen size={16} className="text-gray-600" />
                                                <p className="text-sm font-semibold text-gray-700">Recommended Questions</p>
                                            </div>
                                            <div className="space-y-2">
                                                {message.recommended_questions.map((question) => (
                                                    <Link
                                                        key={question.id}
                                                        to={`/questions/${question.id}`}
                                                        className="block"
                                                    >
                                                        <div className="p-4 bg-white border border-gray-200 rounded-xl hover:border-blue-300 hover:shadow-md transition-all">
                                                            <h4 className="font-medium text-gray-900 mb-2 hover:text-blue-600 transition-colors">
                                                                {question.title}
                                                            </h4>
                                                            <div className="flex gap-2">
                                                                <span className="px-2 py-1 bg-blue-50 text-blue-700 text-xs font-medium rounded-lg border border-blue-200">
                                                                    {question.category}
                                                                </span>
                                                                <span className={`px-2 py-1 text-xs font-medium rounded-lg border ${difficultyColors[question.difficulty]}`}>
                                                                    {question.difficulty}
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </Link>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            ))}

                            {/* Loading indicator */}
                            {loading && (
                                <div className="flex gap-4">
                                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                                        <Sparkles className="text-white" size={16} />
                                    </div>
                                    <div className="flex-1">
                                        <div className="inline-block px-4 py-3 rounded-2xl bg-gray-100">
                                            <div className="flex gap-1">
                                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}

                            <div ref={messagesEndRef} />
                        </div>

                        {/* Input Form */}
                        <div className="border-t border-gray-200 p-4">
                            <form onSubmit={handleSubmit} className="flex gap-3">
                                <input
                                    type="text"
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    placeholder="Ask me anything about interview preparation..."
                                    className="flex-1 px-4 py-3 bg-gray-50 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                    disabled={loading}
                                />
                                <button
                                    type="submit"
                                    disabled={!input.trim() || loading}
                                    className="px-6 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2"
                                >
                                    <Send size={18} />
                                    Send
                                </button>
                            </form>
                        </div>
                    </div>

                    {/* Example Questions */}
                    <div className="mt-6">
                        <p className="text-sm text-gray-600 mb-3">Try asking:</p>
                        <div className="flex flex-wrap gap-2">
                            {[
                                'How do I prepare for system design interviews?',
                                'What are common behavioral interview questions?',
                                'Explain binary search trees',
                                'Tips for coding interviews at FAANG companies'
                            ].map((example, i) => (
                                <button
                                    key={i}
                                    onClick={() => setInput(example)}
                                    className="px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm text-gray-700 hover:border-blue-300 hover:bg-blue-50 transition-all"
                                >
                                    {example}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
