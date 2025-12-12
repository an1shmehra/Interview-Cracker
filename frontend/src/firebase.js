import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
    apiKey: "AIzaSyBZa0wjFoBpsKniArWtK8CG3i6FWFEWzvQ",
    authDomain: "interview-cracker-c077a.firebaseapp.com",
    projectId: "interview-cracker-c077a",
    storageBucket: "interview-cracker-c077a.firebasestorage.app",
    messagingSenderId: "82026880158",
    appId: "1:82026880158:web:8462390a0191920847af8f",
    measurementId: "G-Z5S66H40J4"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication
export const auth = getAuth(app);

// Initialize Firestore
export const db = getFirestore(app);

// Google Auth Provider
export const googleProvider = new GoogleAuthProvider();

// Configure Google provider to always show account selection
googleProvider.setCustomParameters({
    prompt: 'select_account'
});

export default app;
