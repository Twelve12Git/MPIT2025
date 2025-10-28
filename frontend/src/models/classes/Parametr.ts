
export type ValueType = "NUMBER" | "BOOLEAN";


export class Parametr {
    name: string;
    valueType: ValueType;

    constructor(name: string, valueType: ValueType) {
        this.valueType = valueType,
        this.name = name
    }
}