/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_WORKERS_LIST: string;
    readonly VITE_WORKERS_CREATE: string;
    readonly VITE_WORKERS_GET: string;
    readonly VITE_WORKERS_UPDATE: string;
    readonly VITE_WORKERS_DELETE: string;

    readonly VITE_ORDERS_CREATE: string;
    readonly VITE_ORDERS_STATS_LIST: string;
    readonly VITE_ORDERS_STATS_GET: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
