import type { PageType } from "../pageType";



export type StoreActivePageType = {
    activePageName: PageType;
    setActivePage: (pageName: PageType) => void;
    removeActivePage: () => void;
}