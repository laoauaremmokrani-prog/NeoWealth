
import { motion } from 'framer-motion';

const TICKER_ITEMS = [
    { symbol: "SPX", price: "4,785.24", change: "+1.2%", up: true },
    { symbol: "NDX", price: "16,832.91", change: "+0.8%", up: true },
    { symbol: "DJI", price: "37,645.18", change: "-0.3%", up: false },
    { symbol: "VIX", price: "13.45", change: "-2.1%", up: false },
    { symbol: "AAPL", price: "192.45", change: "+0.5%", up: true },
    { symbol: "MSFT", price: "375.12", change: "+1.1%", up: true },
    { symbol: "NVDA", price: "485.09", change: "+2.4%", up: true },
    { symbol: "TSLA", price: "245.67", change: "-1.2%", up: false },
];

export function MarketTicker() {
    return (
        <div className="ticker">
            <motion.div
                className="ticker-track"
                animate={{ x: ["0%", "-50%"] }}
                transition={{ repeat: Infinity, duration: 20, ease: "linear" }}
            >
                {[...TICKER_ITEMS, ...TICKER_ITEMS].map((item, i) => (
                    <div key={i} className="ticker-item">
                        <span className="ticker-symbol">{item.symbol}</span>
                        <span className="ticker-price">{item.price}</span>
                        <span className={item.up ? "ticker-change up" : "ticker-change down"}>
                            {item.change}
                        </span>
                    </div>
                ))}
            </motion.div>
        </div>
    );
}
