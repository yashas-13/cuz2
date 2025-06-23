import { openDB } from 'idb';
const dbPromise = openDB('scm-queue', 1, {
  upgrade(db) { db.createObjectStore('queue', { autoIncrement: true }); }
});

export async function queueRequest(req) {
  const db = await dbPromise;
  await db.add('queue', req);
}

export async function flushQueue() {
  const db = await dbPromise;
  const tx = db.transaction('queue', 'readwrite');
  const store = tx.objectStore('queue');
  let cursor = await store.openCursor();
  while (cursor) {
    await fetch(cursor.value.url, cursor.value.options);
    await cursor.delete();
    cursor = await cursor.continue();
  }
  await tx.done;
}

window.addEventListener('online', flushQueue);
