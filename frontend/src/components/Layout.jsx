import { useState } from 'react';
import { Menu } from 'lucide-react';
import Sidebar from './Sidebar';

export default function Layout({ children }) {
    const [sidebarOpen, setSidebarOpen] = useState(false);

    return (
        <div className="min-h-screen bg-gray-50">
            <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

            {/* Content wrapper that shifts when sidebar opens */}
            <div className={`min-h-screen transition-all duration-300 ${
                sidebarOpen ? 'ml-64' : 'ml-0'
            }`}>
                {/* Hamburger Menu Button */}
                <button
                    onClick={() => setSidebarOpen(true)}
                    className="fixed top-4 left-4 z-30 p-2 bg-white border border-gray-300 rounded-lg shadow-md hover:bg-gray-50 transition-all"
                    aria-label="Open menu"
                >
                    <Menu size={24} className="text-gray-700" />
                </button>

                {/* Main Content */}
                <main>
                    {children}
                </main>
            </div>
        </div>
    );
}
