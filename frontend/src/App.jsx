import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import LandingPage from './pages/LandingPage';
import QuestionsPage from './pages/QuestionsPage';
import QuestionDetail from './pages/QuestionDetail';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/questions" element={<QuestionsPage />} />
          <Route path="/questions/:id" element={<QuestionDetail />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;