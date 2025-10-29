import { useEffect, useState } from 'react';
import './styles.css';
import PageHeader from '../../support/pageHeader/PageHeader';
import Executor from '../../../models/classes/Executor';
import Dialog from '../../support/dialog/Dialog';
import { ExecutorEditParametr } from '../../common/executorEditParametr/ExecuterEditParametr';
import Environment from '../../../utils/Environment';
import axios, { type AxiosResponse } from 'axios';

export default function ExecutorsPage() {
    const [selectExecutor, setSelectExecutor] = useState<Executor | null>(null);
    const [executors, setExecutors] = useState(Array<Executor>);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // const fetchedExecutor: Executor[] = [
        //     new Executor(1, 'Иван Иванов', 52),
        //     new Executor(2, 'Петр Петров', 51),
        //     new Executor(3, 'Анна Сидорова', 48),
        //     new Executor(4, 'Мария Кузнецова', 50),
        // ];

        const fetchData = async () => {
            try {
                const response: AxiosResponse<any, any, {}> = await axios.get(Environment.VITE_WORKERS_LIST);
                setExecutors(response.data);
            } catch (error) {
                console.error("Ошибка при загрузке исполнителей:", error);
            } finally {
                setLoading(false);
            }
        };


        fetchData();
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
                        <th>Кол-во задач</th>
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
                                <td>{executor.id}</td>
                                <td>{executor.countTask}</td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    );
}