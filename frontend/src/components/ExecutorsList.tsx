import '../styles/style.css';

const fetchExecutorsCache = () =>
    Promise.resolve([
        { id: 1, name: 'Иванов', active: true, currentLoad: 3, dailyLimit: 10, weight: 2 },
        { id: 2, name: 'Петров', active: true, currentLoad: 1, dailyLimit: 8, weight: 1 },
        { id: 3, name: 'Сидоров', active: false, currentLoad: 0, dailyLimit: 5, weight: 3 },
    ]);


interface Executor {
    id: number;
    name: string;
    active: boolean;
    currentLoad: number;
    dailyLimit: number;
    weight: number;
}

interface ExecutorsListProps {
    executors: Executor[];
}

// Список активных исполнителей с текущей загрузкой и лимитами
const ExecutorsList: React.FC<ExecutorsListProps> = ({ executors }) => {
    return (
        <section style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '20px' }}>
            <h3>Активные исполнители</h3>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                    <tr>
                        <th>Имя</th>
                        <th>Активен</th>
                        <th>Текущая нагрузка</th>
                        <th>Дневной лимит</th>
                        <th>Вес</th>
                    </tr>
                </thead>
                <tbody>
                    {executors.map((exec: Executor) => (
                        <tr key={exec.id} style={{ backgroundColor: exec.active ? 'white' : '#eee' }}>
                            <td>{exec.name}</td>
                            <td>{exec.active ? 'Да' : 'Нет'}</td>
                            <td>{exec.currentLoad}</td>
                            <td>{exec.dailyLimit}</td>
                            <td>{exec.weight}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </section>
    );
};