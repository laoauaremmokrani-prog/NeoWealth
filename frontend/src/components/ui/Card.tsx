
import { clsx } from 'clsx';
import './Card.css';

export function Card({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
    return (
        <div
            className={clsx('card', className)}
            {...props}
        >
            {children}
        </div>
    );
}

export function CardHeader({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
    return (
        <div className={clsx('card-header', className)} {...props}>
            {children}
        </div>
    );
}

export function CardTitle({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
    return (
        <h3 className={clsx('card-title', className)} {...props}>
            {children}
        </h3>
    );
}

export function CardContent({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
    return (
        <div className={clsx('card-content', className)} {...props}>
            {children}
        </div>
    );
}
