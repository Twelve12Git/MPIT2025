import './styles.css';
import { Worker, type Declaration } from "../../../models/classes/Worker";
import PageHeader from "../../support/pageHeader/PageHeader";
import { faker } from '@faker-js/faker';
import env from '../../../utils/Environment';
import { Order, type AddProp } from "../../../models/classes/Order";
import { Parametr } from "../../../models/classes/Parametr";
import { useState, type ChangeEvent, type FormEvent } from 'react';




export default function TestsPage() {
    

    const [workers, setWorkers] = useState<number>(1);

    const [orders, setOrders] = useState<number>(1000);
    const [delays, setDelays] = useState<number>(500);

    const handleWorkers = (e: ChangeEvent<HTMLInputElement>) => {
        setWorkers(Number(e.target.value));
    }

    const handleOrders = (e: ChangeEvent<HTMLInputElement>) => {
        setOrders(Number(e.target.value));
        console.log(orders);
    }

    const handleDelays = (e: ChangeEvent<HTMLInputElement>) => {
        setDelays(Number(e.target.value));
    }

    const createWorkers = async (e: FormEvent) => {
        e.preventDefault();

        for (let i = 0; i < workers; i++) {
            let deaclaration: Declaration[] = [{
                type: faker.helpers.arrayElement(['BOOLEAN', "NUMBER"]),
                name: faker.lorem.word(5)
            }]
            let data: Worker = new Worker(deaclaration, "= 1");

            await fetch(env.VITE_WORKERS_CREATE, {
                method: 'POST',
                body: JSON.stringify(data),
            })
        };
    }

    const createorders = async (e: FormEvent) => {
        e.preventDefault();

        for (let i = 0; i < orders; i++) {
            let addProp: AddProp = { additionalProp1: {} };
            let parametr: Parametr = new Parametr(faker.lorem.word(5), 1, faker.helpers.arrayElement(['BOOLEAN', "NUMBER"]));
            let data: Order = new Order(addProp, parametr);

            try {
                const response = await fetch(env.VITE_ORDERS_CREATE, {
                    method: 'POST',
                    body: JSON.stringify(data),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    console.error(`Ошибка при отправке заказа ${i}: ${response.statusText}`);
                }

                await new Promise(resolve => setTimeout(resolve, delays));

            } catch (error) {
                console.error(`Произошла ошибка при отправке заказа ${i}:`, error);
            }
        }
    }

    return (
        <div>
            <PageHeader primaryText='Страница с' secondaryText='тестами' />
            <div className='test-wrapper'>
                <form className="test-form" onSubmit={createWorkers} >
                    <label htmlFor="count">Кол-во исполнителей</label>
                    <input type="number" name='count' min={1} value={workers} onChange={handleWorkers}/>
                    <button type="submit">Создать исполнителей</button>
                </form>
                <form className="test-form" onSubmit={createorders}>
                    <label htmlFor="count">Кол-во заявок</label>
                    <input type="number" name='count' min={1} value={orders} onChange={handleOrders} />

                    <label htmlFor="delay">Задержка создания заявки</label>
                    <input type="number" name='delay' min={1} value={delays} onChange={handleDelays}/>

                    <button type="submit">Создать заявки</button>
                </form>
            </div>
        </div>
    )
}