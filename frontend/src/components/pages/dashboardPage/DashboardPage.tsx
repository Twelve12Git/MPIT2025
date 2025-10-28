import PageHeader from "../../support/pageHeader/PageHeader";
import { Bar, BarChart, CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { useState } from 'react';


type User = {
    name: string;
    age: number;
}

type SprintData = {
    age: number;
    sprintTime: number;
}

const data: Array<User> = [
    { name: 'Ivan', age: 34 },
    { name: 'Valeryy', age: 42 },
    { name: 'Petr', age: 15 },
    { name: 'Anatolyy', age: 25 },
    { name: 'Evgenyy', age: 62 },
];


const dataSprint: Array<SprintData> = [
    { age: 20, sprintTime: 10.30 },
    { age: 21, sprintTime: 9.63 },
    { age: 22, sprintTime: 11.11 },
    { age: 23, sprintTime: 11.11 },
    { age: 24, sprintTime: 11.07 },
    { age: 25, sprintTime: 9.74 },
    { age: 26, sprintTime: 9.67 },
    { age: 27, sprintTime: 10.10 },
    { age: 28, sprintTime: 10.80 }
];

const dataSome = [
    { name: '2020', expenses: 400, incomes: 2400 },
    { name: '2021', expenses: 300, incomes: 1398 },
    { name: '2022', expenses: 200, incomes: 9800 },
    { name: '2023', expenses: 278, incomes: 3908 },
    { name: '2024', expenses: 189, incomes: 4800 },
];

const dataSprinters = [
    { name: "Ivan", sprintTime: 12.4 },
    { name: "Valeryy", sprintTime: 11.8 },
    { name: "Petr", sprintTime: 10.6 },
    { name: "Anatolyy", sprintTime: 13.0 },
    { name: "Evgenyy", sprintTime: 12.1 },
];


export function DashboardPage() {
    const [state, rerenderByState] = useState<boolean>(true);

    const tickFormatter = (tick: any) => `${tick} сек`;

    return (
        <div>
            <PageHeader primaryText="Панель" secondaryText="мониторнинга" />

            <div>
                <div>
                    <LineChart title='Простой график' width={600} height={400} data={data}>
                        <Line type='monotone' stroke='#8884d8' dataKey='age' />
                    </LineChart>
                </div>
                <div style={{ borderBottom: '1px solid gray' }} />
                <div>
                    <LineChart title='Возраст скорость' width={600} height={400} data={dataSprint}>
                        <Line type='monotone' stroke='#8884d8' dataKey='sprintTime' />
                        <Line type='monotone' stroke='brown' dataKey='age' />
                    </LineChart>
                </div>
                <div style={{ borderBottom: '1px solid gray' }} />
                <div>
                    <ResponsiveContainer width='100%' height={400} >
                        <LineChart data={dataSome}>
                            <CartesianGrid strokeDasharray='10 5' />
                            <XAxis dataKey='name' />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Line type='monotone' dataKey='incomes' stroke='#8884d8' />
                            <Line type='monotone' dataKey='expenses' stroke='#82ca9d' />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
                <div style={{ borderBottom: '1px solid gray' }} />
                <div>
                    <ResponsiveContainer width='100%' height={400} >
                        <BarChart data={dataSome}>
                            <CartesianGrid />
                            <XAxis dataKey='name' />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar type='monotone' dataKey='incomes' fill='#8884d8' />
                            <Bar type='monotone' dataKey='expenses' fill='#82ca9d' />
                        </BarChart>
                    </ResponsiveContainer>
                    <div style={{ borderBottom: '1px solid gray' }} />
                    <div>
                        <LineChart
                            data={dataSprinters}
                            width={1280}
                            height={400}
                            margin={{ top: 50, right: 30, left: 20, bottom: 5 }}
                        >
                            <CartesianGrid strokeDasharray='10 5' />
                            <XAxis dataKey='name' />
                            <YAxis tickFormatter={tickFormatter} />
                            <Tooltip />
                            <Legend />
                            <Line type='monotone' dataKey='sprintTime' stroke='#8884d8' strokeWidth={2} isAnimationActive={state} animationDuration={30000} />
                        </LineChart>
                        <button onClick={() => { rerenderByState(!state) }}>Изменить состояние спровоцировав ререндеринг для просмотра анимации</button>
                    </div>
                </div>
            </div>

        </div>
    );
}
