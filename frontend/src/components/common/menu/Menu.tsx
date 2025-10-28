import './styles.css';
import Logo from "../../support/logo/Logo";
import useStoreActivePages from '../../../stores/activePage/useSoreActivePage';



export default function Menu() {
    const { setActivePage, removeActivePage } = useStoreActivePages();

     const handleParametrsPage = async () => {
        setActivePage('parametrs');
    }
    const handleExecutorsPage = async () => {
        setActivePage('executors');
    }
    const handleDashboardPage = async () => {
        setActivePage('dashboard');
    }


    return (
        <div className='menu'>
            <Logo/>
            <div className='wrapper'>
                {/* <button onClick={handleParametrsPage}>Конструктор параметров</button> */}
                <button onClick={handleExecutorsPage}>Список исполнителей</button>
                <button onClick={handleDashboardPage}>Дашбоард</button>
            </div>
        </div>
    )
}