import './styles.css';
import type { PageHeaderProps } from "./pageHeaderType";




export default function PageHeader({primaryText, secondaryText}: PageHeaderProps) {
    return (
        <div className="wrapper-header">
                <p className="primary-text">{primaryText}</p>
                <p className="secondary-text">{secondaryText}</p>
            </div>
    )
}