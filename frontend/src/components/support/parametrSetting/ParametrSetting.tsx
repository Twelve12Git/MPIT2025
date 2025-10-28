import './styles.css';



type ParametrSettingProps = {
    name: string;
    valueType: 'string' | 'number' | 'boolean';

}


export default function ParametrSetting({name, valueType}: ParametrSettingProps) {
    const operator = '=';
    let inputType = "text";
    if (valueType == 'number') inputType = 'number';
    if (valueType == 'boolean') inputType = 'checkbox';

    return (
        <div className='wrapper'>
            <div className='parametrSettings-name'>{name}</div>
            <div className='parametrSettings-operator'>{operator}</div>
            <input className='parametrSettings-value' type={inputType} />
        </div>
    )
}