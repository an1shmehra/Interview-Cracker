import { createContext, useContext, useState, useEffect } from 'react';
import { doc, getDoc, setDoc, updateDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useAuth } from './AuthContext';

const ProgressContext = createContext({});

export const useProgress = () => {
    const context = useContext(ProgressContext);
    if (!context) {
        throw new Error('useProgress must be used within ProgressProvider');
    }
    return context;
};

// LocalStorage key for guest progress
const GUEST_PROGRESS_KEY = 'interview_cracker_guest_progress';

// Helper functions for localStorage
const loadFromLocalStorage = () => {
    try {
        const stored = localStorage.getItem(GUEST_PROGRESS_KEY);
        return stored ? JSON.parse(stored) : {};
    } catch (error) {
        console.error('Error loading from localStorage:', error);
        return {};
    }
};

const saveToLocalStorage = (progress) => {
    try {
        localStorage.setItem(GUEST_PROGRESS_KEY, JSON.stringify(progress));
    } catch (error) {
        console.error('Error saving to localStorage:', error);
    }
};

export function ProgressProvider({ children }) {
    const { user } = useAuth();
    const [progress, setProgress] = useState({});
    const [loading, setLoading] = useState(true);

    // Load user progress from Firestore or localStorage
    useEffect(() => {
        if (!user) {
            // Guest mode: Load from localStorage
            const guestProgress = loadFromLocalStorage();
            setProgress(guestProgress);
            setLoading(false);
            return;
        }

        const loadProgress = async () => {
            try {
                const docRef = doc(db, 'userProgress', user.uid);
                const docSnap = await getDoc(docRef);

                if (docSnap.exists()) {
                    setProgress(docSnap.data().questions || {});
                } else {
                    // Create new progress document
                    await setDoc(docRef, { questions: {} });
                    setProgress({});
                }
            } catch (error) {
                console.error('Error loading progress:', error);
            } finally {
                setLoading(false);
            }
        };

        loadProgress();
    }, [user]);

    // Update question status
    const updateQuestionStatus = async (questionId, status) => {
        const newProgress = {
            ...progress,
            [questionId]: {
                ...progress[questionId],
                status,
                updatedAt: new Date().toISOString()
            }
        };

        setProgress(newProgress);

        if (!user) {
            // Guest mode: Save to localStorage
            saveToLocalStorage(newProgress);
            return;
        }

        // Logged in: Save to Firestore
        try {
            const docRef = doc(db, 'userProgress', user.uid);
            await updateDoc(docRef, { questions: newProgress });
        } catch (error) {
            console.error('Error updating progress:', error);
        }
    };

    // Toggle bookmark
    const toggleBookmark = async (questionId) => {
        const currentBookmark = progress[questionId]?.bookmarked || false;

        const newProgress = {
            ...progress,
            [questionId]: {
                ...progress[questionId],
                bookmarked: !currentBookmark,
                updatedAt: new Date().toISOString()
            }
        };

        setProgress(newProgress);

        if (!user) {
            // Guest mode: Save to localStorage
            saveToLocalStorage(newProgress);
            return;
        }

        // Logged in: Save to Firestore
        try {
            const docRef = doc(db, 'userProgress', user.uid);
            await updateDoc(docRef, { questions: newProgress });
        } catch (error) {
            console.error('Error toggling bookmark:', error);
        }
    };

    // Get question progress
    const getQuestionProgress = (questionId) => {
        return progress[questionId] || { status: null, bookmarked: false };
    };

    // Get stats
    const getStats = () => {
        const questions = Object.values(progress);
        return {
            total: questions.length,
            completed: questions.filter(q => q.status === 'completed').length,
            inProgress: questions.filter(q => q.status === 'in_progress').length,
            bookmarked: questions.filter(q => q.bookmarked).length
        };
    };

    const value = {
        progress,
        loading,
        updateQuestionStatus,
        toggleBookmark,
        getQuestionProgress,
        getStats,
        isGuestMode: !user
    };

    return (
        <ProgressContext.Provider value={value}>
            {children}
        </ProgressContext.Provider>
    );
}
