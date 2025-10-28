import { useEffect, useState } from 'react';
import './styles.css';
import PageHeader from '../../support/pageHeader/PageHeader';
import Executor from '../../../models/classes/Executor';
import Dialog from '../../support/dialog/Dialog';
import { ExecutorPanel } from '../../common/executorPanel/ExecutorPanle';
import { ExecutorEditParametr } from '../../common/executorEditParametr/ExecuterEditParametr';

export default function ExecutorsPage() {
    const [selectExecutor, setSelectExecutor] = useState<Executor | null>(null);
    const [executors, setExecutors] = useState(Array<Executor>);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchedExecutor: Executor[] = [
            new Executor(1, 'Иван Иванов', true, 50, 75),
            new Executor(2, 'Петр Петров', false, 51, 82),
            new Executor(3, 'Анна Сидорова', true, 48, 60),
            new Executor(4, 'Мария Кузнецова', true, 50, 68),
        ];
        setExecutors(fetchedExecutor);
        setLoading(false);
    }, []);


    const handleExecutorParametrs = (executor: Executor) => {
        setSelectExecutor(executor);
    }

    const handleClose = () => {
        setSelectExecutor(null);
    }


    return (
        <div className='executorlist'>
            {
                selectExecutor &&
                <Dialog>
                    {/* <ExecutorPanel executor={selectExecutor} handleClose={handleClose}/> */}
                    <ExecutorEditParametr executor={selectExecutor} handleClose={handleClose} />
                </Dialog>
            }

            <PageHeader primaryText='Активные' secondaryText='исполнители' />
            <table className='executors-table'>
                <thead>
                    <tr>
                        <th>Имя</th>
                        <th>Активен</th>
                        <th>Кол-во задач</th>
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
                            <tr key={executor.id} onClick={() => handleExecutorParametrs(executor)}>
                                <td>{executor.name}</td>
                                <td>{executor.active ? 'Да' : 'Нет'}</td>
                                <td>{executor.countTask}</td>
                                <td>{executor.weight}</td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    );
}