import { Link } from 'react-router-dom';
import { Zap, Github, Linkedin, Mail } from 'lucide-react';

export default function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="bg-gray-900 text-gray-300 mt-auto">
            <div className="max-w-7xl mx-auto px-8 py-12">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
                    {/* About Section */}
                    <div className="md:col-span-2">
                        <div className="flex items-center gap-2 mb-4">
                            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center">
                                <Zap className="text-white" size={18} />
                            </div>
                            <span className="text-xl font-bold text-white">Interview Cracker</span>
                        </div>
                        <p className="text-gray-400 mb-4 max-w-md">
                            Your comprehensive platform for mastering technical interviews. We curate high-quality interview questions from hard-to-find sources across top companies, all in one place. Get AI-powered guidance and ace your next interview with confidence.
                        </p>
                        <div className="flex gap-4">
                            <a
                                href="https://github.com/an1shmehra"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="w-9 h-9 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-gray-700 transition-colors"
                                aria-label="GitHub"
                            >
                                <Github size={18} />
                            </a>
                            <a
                                href="https://www.linkedin.com/in/anishh-mehraa"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="w-9 h-9 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-gray-700 transition-colors"
                                aria-label="LinkedIn"
                            >
                                <Linkedin size={18} />
                            </a>
                            <a
                                href="mailto:mehraanishh@gmail.com"
                                className="w-9 h-9 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-gray-700 transition-colors"
                                aria-label="Email"
                            >
                                <Mail size={18} />
                            </a>
                        </div>
                    </div>

                    {/* Quick Links */}
                    <div>
                        <h3 className="text-white font-semibold mb-4">Quick Links</h3>
                        <ul className="space-y-2">
                            <li>
                                <Link to="/" className="text-gray-400 hover:text-white transition-colors">
                                    Home
                                </Link>
                            </li>
                            <li>
                                <Link to="/questions?category=DSA" className="text-gray-400 hover:text-white transition-colors">
                                    DSA Questions
                                </Link>
                            </li>
                            <li>
                                <Link to="/questions?category=System Design" className="text-gray-400 hover:text-white transition-colors">
                                    System Design
                                </Link>
                            </li>
                            <li>
                                <Link to="/questions?category=Behavioral" className="text-gray-400 hover:text-white transition-colors">
                                    Behavioral
                                </Link>
                            </li>
                            <li>
                                <Link to="/ai" className="text-gray-400 hover:text-white transition-colors">
                                    AI Assistant
                                </Link>
                            </li>
                        </ul>
                    </div>
                </div>

                {/* Bottom Bar */}
                <div className="pt-8 border-t border-gray-800 text-center">
                    <p className="text-gray-400 text-sm mb-2">
                        © {currentYear} Interview Cracker. All rights reserved.
                    </p>
                    <p className="text-gray-500 text-xs">
                        Built with React, FastAPI, PostgreSQL, and AI-powered by Groq
                    </p>
                </div>
            </div>
        </footer>
    );
}
