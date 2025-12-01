import { ArrowRight, Zap, Shield, TrendingUp, Target, Sparkles, Award } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function LandingPage() {
    return (
        <div className="min-h-screen bg-white">
            {/* Hero Section */}
            <section className="px-8 py-20 lg:py-28">
                <div className="max-w-6xl mx-auto">
                    <div className="max-w-3xl mx-auto text-center">
                        {/* Badge */}
                        <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-50 border border-blue-200 rounded-full mb-8">
                            <Sparkles size={14} className="text-blue-600" />
                            <span className="text-sm font-medium text-blue-700">AI-Powered Interview Preparation</span>
                        </div>

                        {/* Heading */}
                        <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight tracking-tight">
                            Ace Your Next
                            <br />
                            <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                                Tech Interview
                            </span>
                        </h1>

                        <p className="text-xl text-gray-600 mb-10 leading-relaxed max-w-2xl mx-auto">
                            Master coding interviews with curated questions from FAANG and top tech companies.
                            Practice smarter with AI-powered insights and personalized recommendations.
                        </p>

                        {/* CTA */}
                        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                            <Link to="/questions">
                                <button className="px-8 py-3.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-all hover:shadow-lg hover:shadow-blue-500/50 flex items-center gap-2">
                                    Start Practicing
                                    <ArrowRight size={18} />
                                </button>
                            </Link>
                            <a href="#features">
                                <button className="px-8 py-3.5 bg-white border border-gray-300 hover:border-gray-400 text-gray-700 rounded-lg font-semibold transition-all hover:shadow-md">
                                    View Features
                                </button>
                            </a>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features */}
            <section id="features" className="px-8 py-20 bg-gray-50">
                <div className="max-w-6xl mx-auto">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
                            Everything you need to succeed
                        </h2>
                        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                            Comprehensive tools and features designed to help you prepare effectively for your dream job.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8">
                        <FeatureCard
                            icon={<Target className="text-blue-600" size={24} />}
                            title="Company-Specific Prep"
                            description="Focus your preparation with questions from specific companies like Google, Amazon, and Meta."
                        />
                        <FeatureCard
                            icon={<Shield className="text-blue-600" size={24} />}
                            title="Curated Quality"
                            description="Hand-picked questions from real interviews at FAANG and top tech companies."
                        />
                        <FeatureCard
                            icon={<Sparkles className="text-blue-600" size={24} />}
                            title="AI-Powered Insights"
                            description="Get intelligent recommendations and personalized study plans powered by AI."
                        />
                        <FeatureCard
                            icon={<Zap className="text-blue-600" size={24} />}
                            title="Smart Filtering"
                            description="Filter by difficulty, topic, and category to target your weak areas."
                        />
                        <FeatureCard
                            icon={<TrendingUp className="text-blue-600" size={24} />}
                            title="Track Progress"
                            description="Monitor your improvement and identify patterns in your preparation journey."
                        />
                        <FeatureCard
                            icon={<Award className="text-blue-600" size={24} />}
                            title="Interview Ready"
                            description="Build confidence with comprehensive coverage of DSA, System Design, and Behavioral questions."
                        />
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="px-8 py-20 bg-white">
                <div className="max-w-6xl mx-auto">
                    <div className="relative overflow-hidden bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 rounded-3xl p-12 lg:p-16 text-center text-white">
                        {/* Decorative elements */}
                        <div className="absolute top-0 left-0 w-full h-full opacity-10">
                            <div className="absolute top-10 left-10 w-32 h-32 bg-white rounded-full blur-3xl"></div>
                            <div className="absolute bottom-10 right-10 w-40 h-40 bg-white rounded-full blur-3xl"></div>
                        </div>

                        <div className="relative z-10">
                            <h2 className="text-3xl lg:text-5xl font-bold mb-6">
                                Ready to ace your interviews?
                            </h2>
                            <p className="text-lg lg:text-xl text-blue-100 mb-10 max-w-2xl mx-auto leading-relaxed">
                                Start practicing with curated questions from top companies and get AI-powered guidance.
                            </p>
                            <Link to="/questions">
                                <button className="px-10 py-4 bg-white text-blue-600 hover:bg-gray-50 rounded-xl font-bold text-lg transition-all hover:shadow-2xl hover:scale-105 inline-flex items-center gap-2">
                                    Get Started Free
                                    <ArrowRight size={20} />
                                </button>
                            </Link>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}

function FeatureCard({ icon, title, description }) {
    return (
        <div className="group p-8 bg-white border border-gray-200 rounded-2xl hover:border-blue-300 hover:shadow-xl transition-all duration-300 cursor-default">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl flex items-center justify-center mb-5 group-hover:scale-110 transition-transform duration-300">
                {icon}
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">{title}</h3>
            <p className="text-gray-600 leading-relaxed">{description}</p>
        </div>
    );
}