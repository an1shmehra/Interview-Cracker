import { useEffect, useState } from 'react';
import { questionsAPI } from '../services/api';
import { BookOpen, Code, Brain, TrendingUp, Sparkles, ArrowRight, Zap } from 'lucide-react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

function HomePage() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await questionsAPI.getStats();
                setStats(response.data);
            } catch (error) {
                console.error('Error fetching stats:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, []);

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 flex items-center justify-center">
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-16 h-16 border-4 border-indigo-600 border-t-transparent rounded-full"
                />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
            {/* Hero Section */}
            <div className="container mx-auto px-4 pt-20 pb-16">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-16"
                >
                    {/* Badge */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.2 }}
                        className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-100 text-indigo-700 rounded-full mb-6"
                    >
                        <Sparkles size={16} />
                        <span className="text-sm font-medium">AI-Powered Interview Prep</span>
                    </motion.div>

                    {/* Main Heading */}
                    <h1 className="text-6xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">
                        Master Your
                        <span className="bg-gradient-to-r from-indigo-600 to-purple-600 text-transparent bg-clip-text"> Interview</span>
                        <br />
                        Journey
                    </h1>

                    <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
                        Curated collection of <span className="font-bold text-indigo-600">{stats?.total_questions}+</span> interview questions
                        from top tech companies. Practice smarter, not harder.
                    </p>

                    {/* CTA Buttons */}
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link to="/questions">
                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                className="group px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all flex items-center gap-2"
                            >
                                Start Practicing
                                <ArrowRight className="group-hover:translate-x-1 transition-transform" size={20} />
                            </motion.button>
                        </Link>
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="px-8 py-4 bg-white text-gray-900 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all border-2 border-gray-200"
                        >
                            View All Categories
                        </motion.button>
                    </div>
                </motion.div>

                {/* Stats Cards */}
                <motion.div
                    initial={{ opacity: 0, y: 40 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4, duration: 0.6 }}
                    className="grid md:grid-cols-3 gap-6 mb-20"
                >
                    <StatCard
                        icon={<Code className="w-10 h-10" />}
                        title="DSA Questions"
                        count={stats?.by_category?.DSA || 0}
                        gradient="from-blue-500 to-cyan-500"
                        delay={0.5}
                    />
                    <StatCard
                        icon={<Brain className="w-10 h-10" />}
                        title="System Design"
                        count={stats?.by_category['System Design'] || 0}
                        gradient="from-purple-500 to-pink-500"
                        delay={0.6}
                    />
                    <StatCard
                        icon={<BookOpen className="w-10 h-10" />}
                        title="Behavioral"
                        count={stats?.by_category?.Behavioral || 0}
                        gradient="from-green-500 to-emerald-500"
                        delay={0.7}
                    />
                </motion.div>

                {/* Features Grid */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.8 }}
                    className="grid md:grid-cols-2 gap-8 mb-20"
                >
                    <FeatureCard
                        icon={<Zap className="w-8 h-8" />}
                        title="Smart Filtering"
                        description="Filter by company, difficulty, and topic to focus on what matters most for your interview prep."
                        gradient="from-orange-500 to-red-500"
                    />
                    <FeatureCard
                        icon={<TrendingUp className="w-8 h-8" />}
                        title="Track Progress"
                        description="Monitor your preparation journey and identify areas that need more practice."
                        gradient="from-indigo-500 to-purple-500"
                    />
                </motion.div>

                {/* Top Companies Section */}
                <motion.div
                    initial={{ opacity: 0, y: 40 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1 }}
                    className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl p-8 md:p-12 border border-gray-100"
                >
                    <div className="flex items-center gap-3 mb-8">
                        <div className="p-3 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-xl">
                            <TrendingUp className="text-white" size={28} />
                        </div>
                        <h2 className="text-3xl font-bold text-gray-900">
                            Top Companies
                        </h2>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                        {stats?.top_companies?.map((company, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: 1.1 + index * 0.1 }}
                                whileHover={{ scale: 1.05, y: -5 }}
                                className="group relative bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-6 text-center hover:shadow-xl transition-all cursor-pointer border border-gray-200"
                            >
                                <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-purple-500/10 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity" />
                                <div className="relative">
                                    <p className="font-bold text-gray-900 text-lg mb-1">{company.name}</p>
                                    <p className="text-sm text-gray-600">
                                        <span className="font-semibold text-indigo-600">{company.count}</span> questions
                                    </p>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </motion.div>
            </div>
        </div>
    );
}

function StatCard({ icon, title, count, gradient, delay }) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay }}
            whileHover={{ y: -8, scale: 1.02 }}
            className="group relative bg-white/80 backdrop-blur-xl rounded-3xl p-8 hover:shadow-2xl transition-all border border-gray-100 overflow-hidden"
        >
            {/* Gradient Background on Hover */}
            <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-0 group-hover:opacity-10 transition-opacity`} />

            <div className="relative">
                <div className={`inline-flex p-4 rounded-2xl bg-gradient-to-br ${gradient} mb-4 shadow-lg`}>
                    <div className="text-white">
                        {icon}
                    </div>
                </div>

                <h3 className="text-5xl font-bold text-gray-900 mb-2">
                    {count.toLocaleString()}
                </h3>
                <p className="text-gray-600 text-lg font-medium">{title}</p>
            </div>
        </motion.div>
    );
}

function FeatureCard({ icon, title, description, gradient }) {
    return (
        <motion.div
            whileHover={{ y: -5 }}
            className="bg-white/80 backdrop-blur-xl rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all border border-gray-100"
        >
            <div className={`inline-flex p-4 rounded-2xl bg-gradient-to-br ${gradient} mb-4`}>
                <div className="text-white">
                    {icon}
                </div>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-3">{title}</h3>
            <p className="text-gray-600 text-lg leading-relaxed">{description}</p>
        </motion.div>
    );
}

export default HomePage;