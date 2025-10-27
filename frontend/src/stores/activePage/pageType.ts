


export const validPagesAsTuple = ["parametrs", "executors", "dashboard"] as const;

export type PageType = typeof validPagesAsTuple[number];