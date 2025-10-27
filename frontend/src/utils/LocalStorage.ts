


export default class LocalStorage {

    public static setLocalStorage(key: string, value: string): void {
        try {
            localStorage.setItem(key, value);
        } catch (error) {
            console.error('Ошибка при сохранении в localStorage:', error);
        }
    }

    public static getLocalStorage(key: string): string | null {
        try {
            const value: string | null = localStorage.getItem(key);
            return value;
        } catch (error) {
            console.error('Ошибка при чтении из localStorage:', error);
            return null;
        }
    }

    public static removeLocalStorage(key: string): void {
        localStorage.removeItem(key);
    }
}