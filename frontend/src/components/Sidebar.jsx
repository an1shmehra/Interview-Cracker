import { Link, useLocation } from 'react-router-dom';
import { Home, Code, Brain, MessageSquare, Sparkles, X } from 'lucide-react';

const navigation = [
    { name: 'Home', href: '/', icon: Home },
    { name: 'DSA', href: '/questions?category=DSA', icon: Code },
    { name: 'System Design', href: '/questions?category=System Design', icon: Brain },
    { name: 'Behavioral', href: '/questions?category=Behavioral', icon: MessageSquare },
    { name: 'AI Assistant', href: '/ai', icon: Sparkles },
];

export default function Sidebar({ isOpen, onClose }) {
    const location = useLocation();

    const isActive = (href) => {
        if (href === '/') return location.pathname === '/';
        return location.pathname.includes(href.split('?')[0]);
    };

    return (
        <aside
            className={`fixed left-0 top-0 h-screen w-64 bg-white border-r border-gray-200 flex flex-col z-50 transition-transform duration-300 ease-in-out
                ${isOpen ? 'translate-x-0' : '-translate-x-full'}
            `}
        >
            {/* Logo */}
            <div className="h-16 flex items-center justify-between px-6 border-b border-gray-200">
                <Link to="/" className="flex items-center gap-2" onClick={onClose}>
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center">
                        <Code className="text-white" size={18} />
                    </div>
                    <span className="text-lg font-bold text-gray-900">InterviewPrep</span>
                </Link>

                {/* Close button */}
                <button
                    onClick={onClose}
                    className="p-1 hover:bg-gray-100 rounded-md transition-colors"
                    aria-label="Close menu"
                >
                    <X size={20} className="text-gray-600" />
                </button>
            </div>

            {/* Navigation */}
            <nav className="flex-1 px-3 py-4 overflow-y-auto">
                <div className="space-y-1">
                    {navigation.map((item) => {
                        const Icon = item.icon;
                        const active = isActive(item.href);

                        return (
                            <Link
                                key={item.name}
                                to={item.href}
                                onClick={onClose}
                                className={`
                                    flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all
                                    ${active
                                        ? 'bg-blue-50 text-blue-700 font-medium'
                                        : 'text-gray-700 hover:bg-gray-100'
                                    }
                                `}
                            >
                                <Icon size={20} />
                                <span className="flex-1">{item.name}</span>
                                {item.badge && (
                                    <span className="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded-full font-medium">
                                        {item.badge}
                                    </span>
                                )}
                            </Link>
                        );
                    })}
                </div>
            </nav>

            {/* Footer */}
            <div className="p-4 border-t border-gray-200">
                <div className="px-3 py-3 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border border-blue-100">
                    <p className="text-xs text-blue-600 font-medium">Top Companies</p>
                    <p className="text-sm font-semibold text-gray-900 mt-1">Curated From Premium Sources</p>
                </div>
            </div>
        </aside>
    );
}
