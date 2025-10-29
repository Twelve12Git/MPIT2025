import type { ValueType } from "./Parametr"

export type Declaration = {
    type: ValueType,
    name: string,
}

export class Worker {
    id?: string;
    parameters_declaration: Declaration[];
    parameters_expression: string;

    constructor(declaration: Declaration[], expression: string) {
        this.parameters_declaration = declaration,
        this.parameters_expression = expression
    }
}