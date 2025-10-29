


export const validPagesAsTuple = ["tests", "parametrs", "executors", "dashboard"] as const;

export type PageType = typeof validPagesAsTuple[number];