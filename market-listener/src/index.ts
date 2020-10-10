import * as ccxws from 'ccxws';
import { Kafka } from 'kafkajs';

// See https://github.com/tulios/kafkajs
const kafka = new Kafka({
  clientId: 'crypto-app',
  brokers: [process.env.BROKER_URL],
});


// See https://github.com/altangent/ccxws
const market = {
    id: "XXBTZUSD", // remote_id used by the exchange
    base: "BTC", // standardized base symbol for Bitcoin
    quote: "USD",
    type: "spot",
};

const kraken = new ccxws.Kraken({ apiKey: process.env.API_KEY, apiSecret: process.env.API_SECRET });
const producer = kafka.producer();

function publishMessage(candle) {
    const message = {
        value: JSON.stringify(
            {
                timestampMs: candle.timestampMs,
                open: candle.open,
                high: candle.high,
                low: candle.low,
                close: candle.close,
                volume: candle.volume,
            }
        ),
    };

    producer
        .send({ topic: 'crypto.candles', messages: [message] })
        .then(console.log)
        .catch(e => console.error(`[example/producer] ${e.message}`, e));
}

const run = async () => {
    await producer.connect();

    kraken.on("error", err => console.error(err));
    kraken.on("candle", publishMessage);
    // kraken.on("ticker", (ticker) => console.log("recvt>", ticker));

    kraken.subscribeCandles(market);
    // kraken.subscribeTicker(market);
};

run().catch(e => console.error(`[example/producer] ${e.message}`, e));
