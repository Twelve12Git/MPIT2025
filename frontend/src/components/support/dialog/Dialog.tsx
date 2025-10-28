import './styles.css';
import type { DialogType } from "./dialogProps";



export default function Dialog({children}: DialogType) {


    return (
        <div className='modalOverlay'>
            <div className='modalContent'>
                {children}
            </div>
        </div>
    )
}