import { create } from "zustand"
import { validPagesAsTuple, type PageType, } from "./pageType";
import LocalStorage from "../../utils/LocalStorage";
import type { StoreActivePageType } from "./storeActivePageType";


const keyLocalStore: string = "activePageName";
const defaultPage: PageType = "executors";

const loadFromSessionStorage = (): PageType => {
    try {
        const storePage: string = LocalStorage.getLocalStorage(keyLocalStore) ?? "";
        if (validPagesAsTuple.includes(storePage as PageType)) {
            return storePage as PageType;
        }
    } catch (err) {
        console.error(err);
    }
    return  defaultPage;
};

const saveToSessionStorage = (pageName: PageType) => {
    LocalStorage.setLocalStorage(keyLocalStore, pageName);
};

const removeToSessionStorage = () => {
    LocalStorage.removeLocalStorage(keyLocalStore);
}


const useStoreActivePages = create<StoreActivePageType>((set) => ({
    activePageName: loadFromSessionStorage(),

    setActivePage: (pageName: PageType) => {
        set({ activePageName: pageName });
        saveToSessionStorage(pageName);
    },

    removeActivePage: () => {
        set({ activePageName: defaultPage })
        removeToSessionStorage();
    }
}));

export default useStoreActivePages;