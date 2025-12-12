import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProgressProvider } from './context/ProgressContext';
import Layout from './components/Layout';
import LandingPage from './pages/LandingPage';
import QuestionsPage from './pages/QuestionsPage';
import QuestionDetail from './pages/QuestionDetail';
import AIAssistant from './pages/AIAssistant';

function App() {
  return (
    <AuthProvider>
      <ProgressProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/questions" element={<QuestionsPage />} />
              <Route path="/questions/:id" element={<QuestionDetail />} />
              <Route path="/ai" element={<AIAssistant />} />
            </Routes>
          </Layout>
        </Router>
      </ProgressProvider>
    </AuthProvider>
  );
}

export default App;