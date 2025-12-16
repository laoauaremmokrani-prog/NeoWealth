
import { clsx } from 'clsx';
import './Badge.css';

interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
    variant?: 'default' | 'success' | 'danger' | 'warning' | 'outline';
}

export function Badge({ className, variant = 'default', ...props }: BadgeProps) {
    const variants = {
        default: 'badge-default',
        success: 'badge-success',
        danger: 'badge-danger',
        warning: 'badge-warning',
        outline: 'badge-outline',
    };

    return (
        <div
            className={clsx('badge', variants[variant], className)}
            {...props}
        />
    );
}
