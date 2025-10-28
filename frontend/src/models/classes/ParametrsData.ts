import type { Parametr } from "./Parametr";



export class PararametrsData {
    parameters_declaration: Parametr[];
    parameters_expressiom: string;

    constructor(param: Parametr[], condition: string) {
        this.parameters_declaration = param;
        this.parameters_expressiom = condition;
    }
}