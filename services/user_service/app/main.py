from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pika
import json

from .core.config import get_settings
from .core.database import engine, Base
from .routers import users

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="User Service API for managing user authentication and profiles"
    )
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(users.router, prefix="/api/v1")
    
    @app.get("/health")
    def health_check():
        return {"status": "healthy", "service": "user-service"}
    
    return app


def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)
    return connection


def publish_event(routing_key: str, message: dict):
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        channel.exchange_declare(
            exchange=settings.RABBITMQ_EXCHANGE,
            exchange_type='topic',
            durable=True
        )
        
        channel.basic_publish(
            exchange=settings.RABBITMQ_EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
                content_type='application/json'
            )
        )
        
        connection.close()
    except Exception as e:
        print(f"Error publishing event: {e}")


app = create_app()
