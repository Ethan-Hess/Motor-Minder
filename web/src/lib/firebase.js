import { initializeApp } from 'firebase/app';
import { connectAuthEmulator, getAuth } from 'firebase/auth';
import { connectFirestoreEmulator, getFirestore } from 'firebase/firestore';
// import { getAnalytics } from "firebase/analytics";
// Import the functions you need from the SDKs you need
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional

// These values are safe to be public since they are only used to 
// identify the Firebase project and do not contain any sensitive information.
const firebaseConfig = {
  apiKey: "AIzaSyBuvN9jFqJ_clpPU4JXeEijzCX7oEzoOeI",
  authDomain: "motor-minder-1d53c.firebaseapp.com",
  projectId: "motor-minder-1d53c",
  storageBucket: "motor-minder-1d53c.firebasestorage.app",
  messagingSenderId: "983840324878",
  appId: "1:983840324878:web:bd1f3dbe52a92729fb2b5f",
  measurementId: "G-GQV2LLRXM0"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);

export const auth = getAuth(app);
export const db = getFirestore(app);

const emulatorConfig = {
  authHost: '127.0.0.1',
  authPort: 9099,
  firestoreHost: '127.0.0.1',
  firestorePort: 8080,
};

const useFirebaseEmulators = import.meta.env.MODE === 'emulators';

if (useFirebaseEmulators) {
  connectAuthEmulator(auth, `http://${emulatorConfig.authHost}:${emulatorConfig.authPort}`, {
    disableWarnings: true,
  });
  connectFirestoreEmulator(db, emulatorConfig.firestoreHost, emulatorConfig.firestorePort);
}
