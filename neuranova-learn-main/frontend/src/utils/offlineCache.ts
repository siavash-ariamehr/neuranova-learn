const DB_NAME = 'neuranova-offline';
const DB_VERSION = 1;
const LESSONS_STORE = 'lessons';

export class OfflineCache {
  private db: IDBDatabase | null = null;

  async init(): Promise<void> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };

      request.onupgradeneeded = (event: any) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains(LESSONS_STORE)) {
          db.createObjectStore(LESSONS_STORE, { keyPath: 'id' });
        }
      };
    });
  }

  async cacheLesson(lesson: any): Promise<void> {
    if (!this.db) await this.init();
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([LESSONS_STORE], 'readwrite');
      const store = transaction.objectStore(LESSONS_STORE);
      const request = store.put(lesson);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async getCachedLesson(id: number): Promise<any> {
    if (!this.db) await this.init();
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([LESSONS_STORE], 'readonly');
      const store = transaction.objectStore(LESSONS_STORE);
      const request = store.get(id);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }
}

export const offlineCache = new OfflineCache();
