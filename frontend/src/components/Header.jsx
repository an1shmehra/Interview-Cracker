import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Zap, Menu, LogIn, LogOut, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Header({ onMenuClick }) {
    const { user, signInWithGoogle, logout } = useAuth();
    const [showDropdown, setShowDropdown] = useState(false);
    const [imageError, setImageError] = useState(false);

    const handleSignIn = async () => {
        try {
            await signInWithGoogle();
            setImageError(false); // Reset image error on new sign in
        } catch (error) {
            console.error('Failed to sign in:', error);
        }
    };

    const handleSignOut = async () => {
        try {
            await logout();
            setShowDropdown(false);
            setImageError(false); // Reset image error on sign out
        } catch (error) {
            console.error('Failed to sign out:', error);
        }
    };

    const handleImageError = () => {
        setImageError(true);
    };

    return (
        <header className="fixed top-0 left-0 right-0 h-16 bg-white border-b border-gray-200 z-40">
            <div className="h-full px-8 flex items-center justify-between">
                {/* Hamburger Menu Button */}
                <button
                    onClick={onMenuClick}
                    className="p-2 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 transition-all"
                    aria-label="Open menu"
                >
                    <Menu size={24} className="text-gray-700" />
                </button>

                {/* Centered Logo and Name */}
                <Link
                    to="/"
                    className="flex items-center gap-3 hover:opacity-80 transition-opacity"
                >
                    {/* Logo */}
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center shadow-md">
                        <Zap className="text-white" size={24} strokeWidth={2.5} />
                    </div>

                    {/* Website Name */}
                    <h1 className="text-2xl font-bold text-gray-900 tracking-tight">
                        Interview Cracker
                    </h1>
                </Link>

                {/* Auth Section */}
                <div className="relative">
                    {!user ? (
                        // Sign In Button
                        <button
                            onClick={handleSignIn}
                            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-all shadow-sm hover:shadow-md"
                        >
                            <LogIn size={18} />
                            <span>Sign In</span>
                        </button>
                    ) : (
                        // User Profile
                        <div>
                            <button
                                onClick={() => setShowDropdown(!showDropdown)}
                                className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded-lg transition-all"
                            >
                                {user.photoURL && !imageError ? (
                                    <img
                                        src={user.photoURL}
                                        alt={user.displayName || 'User'}
                                        onError={handleImageError}
                                        className="w-8 h-8 rounded-full border-2 border-blue-500"
                                    />
                                ) : (
                                    <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
                                        <User size={18} className="text-white" />
                                    </div>
                                )}
                                <span className="text-sm font-medium text-gray-700 hidden sm:block">
                                    {user.displayName || 'User'}
                                </span>
                            </button>

                            {/* Dropdown Menu */}
                            {showDropdown && (
                                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2">
                                    <div className="px-4 py-2 border-b border-gray-100">
                                        <p className="text-sm font-medium text-gray-900 truncate">
                                            {user.displayName}
                                        </p>
                                        <p className="text-xs text-gray-500 truncate">
                                            {user.email}
                                        </p>
                                    </div>
                                    <button
                                        onClick={handleSignOut}
                                        className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-2 transition-colors"
                                    >
                                        <LogOut size={16} />
                                        Sign Out
                                    </button>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
}
