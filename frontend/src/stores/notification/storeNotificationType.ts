import type { NotificationType } from "../notificationType";




export type StoreNotificationType = {
    isVisible: boolean;
    message: string;
    type: NotificationType;
    timeVisible: number;
    timeExit: number;
    showNotification: (message: string, type: NotificationType, time?: number) => void;
    hideNotification: () => void;
}