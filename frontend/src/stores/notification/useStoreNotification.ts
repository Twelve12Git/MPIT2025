import { create } from 'zustand';
import type { StoreNotificationType } from './storeNotificationType';



export const useStotreNotification = create<StoreNotificationType>((set) => ({
    isVisible: false,
    message: "",
    type: "info",
    timeVisible: 4000,
    timeExit: 1000,

    showNotification: (message: string | undefined, type, time?) => {
        set({
            isVisible: true,
            message: message ?? "Непредвиденная ошибка, обратитесь в отдел разработки",
            type,
            timeVisible: time ?? 4000
        });
    },

    hideNotification: () => {
        set({
            isVisible: false,
            message: "",
            type: 'info',
            timeVisible: 4000,
            timeExit: 1000
        });
    },
}));