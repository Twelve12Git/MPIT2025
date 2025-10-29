import type { Parametr } from "./Parametr";



export type AddProp = {
    additionalProp1: Object;
}

export class Order {
    id?: string;
    payload: AddProp;
    parameters: Parametr;
    constructor(payload: AddProp, parameters: Parametr) {
        this.payload = payload,
        this.parameters = parameters
    }
}