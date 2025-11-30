import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Code2, Home, BookOpen } from 'lucide-react';
import HomePage from './pages/HomePage';
import QuestionsPage from './pages/QuestionsPage';

function Navigation() {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-xl shadow-sm border-b border-gray-100">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <motion.div
              whileHover={{ rotate: 360 }}
              transition={{ duration: 0.6 }}
              className="p-2 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl shadow-lg"
            >
              <Code2 className="text-white" size={28} />
            </motion.div>
            <span className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 text-transparent bg-clip-text">
              InterviewPrep
            </span>
          </Link>

          {/* Nav Links */}
          <div className="flex items-center gap-2">
            <NavLink to="/" icon={<Home size={18} />} active={isActive('/')}>
              Home
            </NavLink>
            <NavLink to="/questions" icon={<BookOpen size={18} />} active={isActive('/questions')}>
              Questions
            </NavLink>
          </div>
        </div>
      </div>
    </nav>
  );
}

function NavLink({ to, icon, children, active }) {
  return (
    <Link to={to}>
      <motion.div
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className={`
          flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all
          ${active
            ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg'
            : 'text-gray-700 hover:bg-gray-100'
          }
        `}
      >
        {icon}
        {children}
      </motion.div>
    </Link>
  );
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/questions" element={<QuestionsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;