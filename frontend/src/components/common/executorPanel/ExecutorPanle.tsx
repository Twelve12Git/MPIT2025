import { useEffect, useState } from 'react';
import { Parametr } from '../../../models/classes/Parametr';
import PageHeader from '../../support/pageHeader/PageHeader';
import './styles.css';
import ParametrSetting from '../../support/parametrSetting/ParametrSetting';


export function ExecutorPanel() {
    const [parametrs, setParametrs] = useState(Array<Parametr>);
    useEffect(() => {
        const fetchedParametr: Parametr[] = [
            new Parametr(1, 'Сумма', 'number'),
            new Parametr(2, 'Горячая', 'boolean'),
            new Parametr(3, 'Отдел', 'string'),
        ];
        setParametrs(fetchedParametr);
    }, []);


    return (
        <div className="executorPanel">
            <PageHeader primaryText='Параметры' secondaryText='исполнтеля' />
            <div>
                {parametrs.map(parametr => (
                    <ParametrSetting name={parametr.name} valueType={parametr.valueType}/>
                ))}
            </div>
        </div>
    )
}