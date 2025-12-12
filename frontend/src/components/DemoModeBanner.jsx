import { Info, LogIn } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function DemoModeBanner() {
    return (
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-4 mb-6">
            <div className="flex items-start gap-3">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <Info className="text-blue-600" size={18} />
                </div>
                <div className="flex-1">
                    <h3 className="text-sm font-semibold text-gray-900 mb-1">
                        Demo Mode
                    </h3>
                    <p className="text-sm text-gray-700 leading-relaxed mb-3">
                        You're using the app in demo mode. Your progress is saved locally in your browser,
                        but won't sync across devices.
                    </p>
                    <Link
                        to="/"
                        className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
                    >
                        <LogIn size={16} />
                        Sign in to save permanently
                    </Link>
                </div>
            </div>
        </div>
    );
}
