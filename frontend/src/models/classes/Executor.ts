


export default class Executor {
    id: number;
    name: string;
    active: boolean;
    countTask: number;
    weight: number;

    constructor(id: number, name: string, active: boolean, countTask: number, weight: number) {
        this.id = id,
        this.name = name,
        this.active = active,
        this.countTask = countTask,
        this.weight = weight
    }

}