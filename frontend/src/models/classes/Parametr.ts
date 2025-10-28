
type ValueType = "string" | "number" | "boolean";


export class Parametr {
    id: number;
    name: string;
    valueType: ValueType;

    constructor(id: number, name: string, valueType: ValueType) {
        this.id = id,
        this.name = name,
        this.valueType = valueType
    }
}