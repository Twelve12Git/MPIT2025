import type { ComponentType, JSX } from 'react';
import './zunamiApp.css';
import TestsPage from '../../pages/testPage/TestsPage';
import ParametrsPage from '../../pages/parametrsPage/ParametrsPage';
import ExecutorsPage from '../../pages/executorsPage/ExecutorsPage';
import { DashboardPage } from '../../pages/dashboardPage/DashboardPage';
import useStoreActivePages from '../../../stores/activePage/useSoreActivePage';
import Menu from '../menu/Menu';


const pageMap: Record<string, ComponentType> = {
    tests: TestsPage,
    parametrs: ParametrsPage,
    executors: ExecutorsPage,
    dashboard: DashboardPage,
};

function renderPage(activePageName: string): JSX.Element {
    const Page = pageMap[activePageName];
    if (!Page) throw new Error(`Страница ${activePageName} не найдена`);
    return <Page />;
}


export default function ZumaniApp() {
    const { activePageName } = useStoreActivePages();


    return (
        <div className="container">
            <Menu />
            {renderPage(activePageName)}
        </div>
    )
}