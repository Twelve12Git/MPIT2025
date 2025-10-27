


export default class Executor {
    id: number;
    name: string;
    active: boolean;
    load: string;
    weight: number;

    constructor(id: number, name: string, active: boolean, load: string, weight: number) {
        this.id = id,
        this.name = name,
        this.active = active,
        this.load = load,
        this.weight = weight
    }

}