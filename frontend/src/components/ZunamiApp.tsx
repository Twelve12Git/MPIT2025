import Logo from "./Logo";
import '../styles/zunamiApp.css';
import ExecutorList from "./ExecutorList";




export default function ZumaniApp() {


    return (
        <div className="container">
            <Logo />
            <ExecutorList />
        </div>
    )
}