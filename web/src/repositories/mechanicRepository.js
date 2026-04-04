import { collection, getDocs } from 'firebase/firestore';
import { db } from '../lib/firebase.js';

function mechanicsCollection() {
  return collection(db, 'mechanics');
}

export async function fetchAllMechanics() {
  const snapshot = await getDocs(mechanicsCollection());

  return snapshot.docs.map((mechanicDoc) => ({
    id: mechanicDoc.id,
    ...mechanicDoc.data(),
  }));
}
