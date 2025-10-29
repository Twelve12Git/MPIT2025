import PageHeader from "../../support/pageHeader/PageHeader";
import { Bar, BarChart, CartesianGrid, LabelList, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { useState } from 'react';
import { faker, fakerRU } from "@faker-js/faker";




const workers: { name: string, tasks: number }[] = [];

for (let i = 0; i < 10; i++) {
    let worker = { name: fakerRU.person.firstName(), tasks: faker.helpers.arrayElement([98, 99, 100, 101, 102]) };
    workers.push(worker);
}

const ordersTime = [
    { name: "500", time: 0.34 },
    { name: "1000", time: 0.71 },
    { name: "5000", time: 2.69 },
    { name: "10000", time: 6.53 },
];


export function DashboardPage() {
    const [state, rerenderByState] = useState<boolean>(true);

    const tickFormatter = (tick: any) => `${tick} сек`;

    return (
        <div>
            <PageHeader primaryText="Панель" secondaryText="мониторнинга" />

            <div>
                {/* <div style={{ borderBottom: '1px solid gray' }} />
                <div>
                    <ResponsiveContainer width='100%' height={400} >
                        <LineChart data={workers}>
                            <CartesianGrid strokeDasharray='10 5' />
                            <XAxis dataKey='name' />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Line type='monotone' dataKey='tasks' stroke='#8884d8' />
                        </LineChart>
                    </ResponsiveContainer>
                </div> */}
                <div style={{ borderBottom: '1px solid gray' }} />
                <div>
                    <ResponsiveContainer width="100%" height={400}>
                        <BarChart data={workers}>
                            <CartesianGrid />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar type="monotone" dataKey="tasks" fill="#ffb892ff" animationDuration={10000}> 
                                <LabelList dataKey="tasks" position="top" />
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
                <div style={{ borderBottom: '1px solid gray' }} />
                <div>
                    <LineChart
                        data={ordersTime}
                        width={1280}
                        height={400}
                        margin={{ top: 50, right: 30, left: 20, bottom: 5 }}
                    >
                        <CartesianGrid />
                        <XAxis dataKey='name' />
                        <YAxis tickFormatter={tickFormatter} />
                        <Tooltip />
                        <Legend />
                        <Line type='monotone' dataKey='time' stroke='#ff5900' strokeWidth={2} animationDuration={10000} />
                    </LineChart>
                </div>
            </div>

        </div>
    );
}
