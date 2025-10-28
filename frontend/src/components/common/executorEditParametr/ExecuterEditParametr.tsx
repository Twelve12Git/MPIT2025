import { useState, type ChangeEvent, type FormEvent } from 'react';
import { Parametr, type ValueType } from '../../../models/classes/Parametr';
import PageHeader from '../../support/pageHeader/PageHeader';
import './styles.css';
import type Executor from '../../../models/classes/Executor';
import Select from 'react-select';
import { PararametrsData } from '../../../models/classes/ParametrsData';
import axios, { Axios } from 'axios';


type ExecutorPanelProps = {
    executor: Executor;
    handleClose: () => void;
}

const options: { value: ValueType, label: string }[] = [
    { value: 'NUMBER', label: 'Цифры' },
    { value: 'BOOLEAN', label: 'Истина или ложь' }
];


export function ExecutorEditParametr({ executor, handleClose }: ExecutorPanelProps) {
    const [parametrs, setParametrs] = useState<Parametr[]>(new Array<Parametr>());
    const [selectedOption, setSelectedOption] = useState(options[0]);
    const [name, setName] = useState("");
    const [condition, setCondition] = useState("");


    const handleName = (e: ChangeEvent<HTMLInputElement>) => {
        setName(e.target.value);
    }
    const handleCondition = (e: ChangeEvent<HTMLInputElement>) => {
        setCondition(e.target.value);
    }


    const handleAddParametr = (e: FormEvent) => {
        e.preventDefault();
        if (!name.trim()) return;
        const newParametr = new Parametr(name, selectedOption.value);
        setParametrs([...parametrs, newParametr]);
        setName("");
    }

    const handleSaveData = (e: FormEvent) => {
        e.preventDefault();
        if (parametrs.length == 0) {
            alert("Добавьте хотя бы один параметр");
        }
        const data: PararametrsData = new PararametrsData(parametrs, condition);
        alert(JSON.stringify(data))
        fetch("http://localhost:8080/workers", {
            body: JSON.stringify(data),
            method: 'POST'
        })
    }

    return (
        <div className="executorPanel" >
            <div className='executorPanel-header'>
                <PageHeader primaryText='Параметры' secondaryText='исполнтеля:' otherText={executor.name} />
                <button style={{ height: '50px', alignSelf: 'center' }} onClick={handleClose}>Закрыть</button>
            </div>
            <form className='executor-form' onSubmit={handleAddParametr}>
                <div className='executor-wrapper'>
                    <div className='executor-container'>
                        <label htmlFor="name">Название параметра</label>
                        <input value={name} onChange={handleName} type="text" name='name' placeholder='Введте название параметра' required />
                    </div>
                    <div className='executor-container'>
                        <label htmlFor="name">Тип параметра</label>
                        <Select className='select'
                            defaultValue={selectedOption}
                            onChange={setSelectedOption}
                            options={options}
                            placeholder="Выберите тип"
                            isSearchable
                        />
                    </div>
                    <button className='executor-button' type='submit'>Добавить</button>
                </div>
            </form>
            <div className='executor-wrapper-param'>
                {parametrs.map(parametr => (
                    <div className='executor-parametr'>
                        {parametr.name} : {parametr.valueType}
                    </div>
                ))}
            </div>
            <form onSubmit={handleSaveData}>
                <input value={condition} onChange={handleCondition} type="text" required />
                <button type='submit'>Внести изменения</button>
            </form>
        </div>
    )
}