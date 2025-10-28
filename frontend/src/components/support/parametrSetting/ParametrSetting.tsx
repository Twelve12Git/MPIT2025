import './styles.css';



type ParametrSettingProps = {
    name: string;
    valueType: 'string' | 'number' | 'boolean';
}




export default function ParametrSetting({ name, valueType }: ParametrSettingProps) {
    const operator = '=';
    var operations: string[] = new Array<string>;
    let inputType = "text";
    if (valueType == 'number') {
        inputType = 'number';
        operations = [
            "Больше чем",
            "Меньше чем",
            "Равно"
        ]
    }

    if (valueType == 'boolean') inputType = 'checkbox';

    return (
        <div className='wrapper'>
            <div className='parametrSettings-name'>{name}</div>
            <input className='parametrSettings-value' type={inputType} />
            <div className='parametrSettings-operator'>{operator}</div>
        </div>
    )
}