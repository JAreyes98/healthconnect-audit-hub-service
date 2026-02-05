import time
import pika, json
from config import settings
from database import SessionLocal
from services.audit_service import save_audit_event

def start_audit_consumer():
    print(f"[*] AuditHub trying to connect RabbitMQ: {settings.rabbitmq_host}")
    
    connection = None
    while True:
        try:
            params = pika.URLParameters(settings.rabbitmq_host)
            connection = pika.BlockingConnection(params)
            break
        except Exception as e:
            print(f"[!] Connexion Error RabbitMQ ({settings.rabbitmq_host}): {e}. Retrying 5 seconds...")
            time.sleep(5)

    channel = connection.channel()
    
    channel.queue_declare(queue=settings.rabbitmq_queue, durable=True)
    print(f"[*] Successfully connected. Listening to queue: {settings.rabbitmq_queue}")

    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            print(f"[*] Message received: {data}")
            db = SessionLocal()
            try:
                save_audit_event(db, data)
            finally:
                db.close()
        except Exception as e:
            print(f"[!] Processing error: {e}")

    channel.basic_consume(queue=settings.rabbitmq_queue, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()