import time
import signal
from confluent_kafka import Consumer, KafkaException

# ==================================================
# CONFIGURAZIONE CONSUMER
# ==================================================

BOOTSTRAP_SERVERS = "localhost:9092"   # <--- cambia in "kafka:9093" se giri da container
TOPIC = "hfgw_lnf"
GROUP_ID = "throughput-consumer"

BYTES_PER_MB = 1024 * 1024


def create_consumer():
    return Consumer({
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "group.id": GROUP_ID,
        "auto.offset.reset": "latest",      # parte dai messaggi nuovi
        "enable.auto.commit": False,
        "fetch.min.bytes": 1_000_000,       # prova a leggere chunk grossi
        "fetch.max.bytes": 50_000_000,
        "max.partition.fetch.bytes": 50_000_000,
    })


def main():
    c = create_consumer()
    c.subscribe([TOPIC])

    stop = False

    def handle_stop(sig, frame):
        nonlocal stop
        stop = True
        print("\nInterruzione richiesta, chiudo consumer...")

    signal.signal(signal.SIGINT, handle_stop)

    bytes_interval = 0
    bytes_total = 0
    interval_start = time.perf_counter()

    print(f"Receiver avviato sul topic '{TOPIC}'")

    while not stop:
        try:
            msg = c.poll(0.1)
        except KafkaException as e:
            print(f"Errore consumer: {e}")
            continue

        if msg is None:
            # nessun messaggio in questo giro
            pass
        elif msg.error():
            print(f"Errore nel messaggio: {msg.error()}")
            continue
        else:
            v = msg.value()
            if v is not None:
                size = len(v)
                bytes_interval += size
                bytes_total += size

        now = time.perf_counter()
        elapsed = now - interval_start

        if elapsed >= 1.0:
            mb_sec = (bytes_interval / BYTES_PER_MB) / elapsed
            total_mb = bytes_total / BYTES_PER_MB

            print(f"[STAT] {mb_sec:8.2f} MB/s | totale ricevuto: {total_mb:.2f} MB")

            interval_start = now
            bytes_interval = 0

    c.close()
    print("Terminato.")


if __name__ == "__main__":
    main()
