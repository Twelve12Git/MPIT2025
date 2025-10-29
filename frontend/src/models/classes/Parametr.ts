
export type ValueType = "NUMBER" | "BOOLEAN";


export class Parametr {
    id?: string;
    valueType: ValueType;
    value: number;
    name: string;

    constructor(name: string, value: number, valueType: ValueType) {
        this.name = name;
        this.valueType = valueType;
        this.value = value;
    }
}