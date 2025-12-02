import { useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import Footer from './Footer';

export default function Layout({ children }) {
    const [sidebarOpen, setSidebarOpen] = useState(false);

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            {/* Header with menu button */}
            <Header onMenuClick={() => setSidebarOpen(true)} />

            {/* Sidebar */}
            <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

            {/* Content wrapper */}
            <div className={`flex-1 flex flex-col transition-all duration-300 ${
                sidebarOpen ? 'ml-64' : 'ml-0'
            }`}>
                {/* Main Content with top padding for fixed header */}
                <main className="pt-16 flex-1">
                    {children}
                </main>

                {/* Footer */}
                <Footer />
            </div>
        </div>
    );
}
