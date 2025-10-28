import { useEffect, useState } from 'react';
import './styles.css';
import PageHeader from '../../support/pageHeader/PageHeader';
import Executor from '../../../models/classes/Executor';
import Dialog from '../../support/dialog/Dialog';
import { ExecutorPanel } from '../../common/executorPanel/ExecutorPanle';

export default function ExecutorsPage() {
    const [executors, setExecutors] = useState(Array<Executor>);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            const fetchedExecutor: Executor[] = [
                new Executor(1, 'Иван Иванов', true, 'Средняя', 75 ),
                new Executor(2, 'Петр Петров', false, 'Низкая', 82 ),
                new Executor(3, 'Анна Сидорова', true, 'Высокая', 60 ),
                new Executor(4, 'Мария Кузнецова', true, 'Средняя', 68 ),
            ];
            setExecutors(fetchedExecutor);
            setLoading(false);
        }, 1500);

        return () => clearTimeout(timer);
    }, []);





    return (
        <div className='executorlist'>
            <Dialog>
                <ExecutorPanel/>
            </Dialog>
            <PageHeader primaryText='Активные' secondaryText='исполнители' />
            <table className='executors-table'>
                <thead>
                    <tr>
                        <th>Имя</th>
                        <th>Активен</th>
                        <th>Текущая нагрузка</th>
                        <th>Вес</th>
                    </tr>
                </thead>
                <tbody>
                    {loading ? (
                        <tr>
                            <td colSpan={5}>Загрузка исполнителей...</td>
                        </tr>
                    ) : (
                        executors.map(executor => (
                            <tr key={executor.id}>
                                <td>{executor.name}</td>
                                <td>{executor.active ? 'Да' : 'Нет'}</td>
                                <td>{executor.load}</td>
                                <td>{executor.weight}</td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    );
}