import { useState, type ChangeEvent, type FormEvent } from 'react';
import { type ValueType } from '../../../models/classes/Parametr';
import PageHeader from '../../support/pageHeader/PageHeader';
import './styles.css';
import type Executor from '../../../models/classes/Executor';
import Select, { type SingleValue } from 'react-select';
import { Worker, type Declaration } from '../../../models/classes/Worker';
import Environment from '../../../utils/Environment';


type ExecutorPanelProps = {
    executor: Executor;
    handleClose: () => void;
}

type SelectOptionType = { value: ValueType, label: string };

const options: { value: ValueType, label: string }[] = [
    { value: 'NUMBER', label: 'Цифры' },
    { value: 'BOOLEAN', label: 'Истина или ложь' }
];


export function ExecutorEditParametr({ executor, handleClose }: ExecutorPanelProps) {
    const [parametrs, setParametrs] = useState<Declaration[]>([]);
     const [selectedOption, setSelectedOption] = useState<SelectOptionType | null>(options[0]);
    const [name, setName] = useState("");
    const [condition, setCondition] = useState("");


    const handleName = (e: ChangeEvent<HTMLInputElement>) => {
        setName(e.target.value);
    }
    const handleCondition = (e: ChangeEvent<HTMLInputElement>) => {
        setCondition(e.target.value);
    }
    
    const handleSelectChange = (newValue: SingleValue<SelectOptionType>) => {
        setSelectedOption(newValue);
    }

    const handleAddParametr = (e: FormEvent) => {
        e.preventDefault();
        if (!name.trim() || !selectedOption) {
            alert("Заполните название и выберите тип параметра");
            return;
        }
        const newParametr: Declaration = {
            type: selectedOption.value,
            name: name
        }
        setParametrs([...parametrs, newParametr]);
        setName("");
    }

    const handleSaveData = (e: FormEvent) => {
        e.preventDefault();
        if (parametrs.length === 0) {
            alert("Добавьте хотя бы один параметр");
            return;
        }
        const data: Worker = new Worker(parametrs, condition);
        alert(JSON.stringify(data))
        fetch(Environment.VITE_WORKERS_UPDATE, {
            body: JSON.stringify(data),
            method: 'PUT'
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
                        {parametr.name} : {parametr.type}
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