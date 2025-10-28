import { useEffect, useState } from 'react';
import { Parametr } from '../../../models/classes/Parametr';
import PageHeader from '../../support/pageHeader/PageHeader';
import './styles.css';
import ParametrSetting from '../../support/parametrSetting/ParametrSetting';
import type Executor from '../../../models/classes/Executor';


type ExecutorPanelProps = {
    executor: Executor;
    handleClose: () => void;
}

export function ExecutorPanel({ executor, handleClose }: ExecutorPanelProps) {
    const [parametrs, setParametrs] = useState(Array<Parametr>);
    useEffect(() => {
        const fetchedParametr: Parametr[] = [
            new Parametr(1, 'Сумма', 'number'),
            new Parametr(2, 'Горячая', 'boolean'),
            new Parametr(3, 'Отдел', 'string'),
        ];
        setParametrs(fetchedParametr);
    }, []);

    console.log(executor);

    const handleSaveParametr = () => {
        event?.preventDefault();

        alert('Параметры обновлены');
    }


    return (
        <div className="executorPanel">
            <div className='executorPanel-header'>
                <PageHeader primaryText='Параметры' secondaryText='исполнтеля:' otherText={executor.name} />
                <button style={{height: '50px', alignSelf: 'center'}} onClick={handleClose}>Закрыть</button>
            </div>
            <form className='executor-form' onSubmit={handleSaveParametr}>
                {parametrs.map(parametr => (
                    <ParametrSetting name={parametr.name} valueType={parametr.valueType} />
                ))}
                <button className='executor-button' type='submit'>Обновить</button>
            </form>
        </div>
    )
}