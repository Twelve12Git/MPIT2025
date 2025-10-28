
export type ValueType = "NUMBER" | "BOOLEAN";


export class Parametr {
    valueType: ValueType;
    value: string;
    name: string;

    constructor(name: string, value: string, valueType: ValueType) {
        this.valueType = valueType;
        this.value = value;
        this.name = name;
    }
}