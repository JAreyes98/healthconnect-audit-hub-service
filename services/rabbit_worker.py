import pika, json
from config import settings
from database import SessionLocal
from services.audit_service import save_audit_event

def start_audit_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=settings.rabbitmq_queue, durable=True)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        db = SessionLocal()
        try:
            save_audit_event(db, data)
        finally:
            db.close()

    channel.basic_consume(queue=settings.rabbitmq_queue, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()