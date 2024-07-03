# main.py
from contextlib import asynccontextmanager
from typing import Union, Optional, Annotated
from app import settings
from sqlmodel import Field, Session, SQLModel, create_engine, select, Sequence
from fastapi import FastAPI, Depends
from typing import AsyncGenerator
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(index=True) 


# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL 
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
) 


# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)

def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)


# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

#todos consumer        
todos_consumed_messages = []

async def consume_messages(topic, bootstrap_servers,queue):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-group-4",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()   
    try:
        # Continuously listen for messages.
        async for message in consumer:
            msg = json.loads(message.value)
            print(f"Received message: {msg} on topic {message.topic}")
            await queue.put(msg)
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
        
async def consume_messages_without_queue(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="test-group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()   
    try:
        # Continuously listen for messages.
        async for message in consumer:
            msg = json.loads(message.value)
            print(f"Received message: {msg} on topic {message.topic}")
            todos_consumed_messages.append(msg)
            
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()

# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    # Start Kafka consumer in a separate task
    loop.create_task(consume_messages('todos', 'broker:19092',queue))
    # Start a task to process messages from the queue
    loop.create_task(process_queue(queue))
    
    # without queue
    # task = asyncio.create_task(consume_messages('todos', 'broker:19092'))
    
    #database
    print("Creating tables..")
    create_db_and_tables()
    yield  

app = FastAPI(lifespan=lifespan, title="Hello World API with DB", 
    version="0.0.1",
    servers=[
            {
                "url": "http://host.docker.internal:8501", # ADD NGROK URL Here Before Creating GPT Action
                "description": "Development Docker Server"
            },
            {
                "url": "http://localhost:8501", 
                "description": "Development Local Server"
            }
        ]
    ) 

def get_session():
    with Session(engine) as session:
        yield session
    

async def process_queue(queue):
    while True:
        message = await queue.get()
        todos_consumed_messages.append(message)
        queue.task_done()

@app.get("/") 
def read_root():
    return {"Hello": "World", "todos consumer": todos_consumed_messages}

@app.get("/hello") 
def read_root():
    return {"Hello": "World"}

@app.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo, session: Annotated[Session, Depends(get_session)],producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)])->Todo:
        todo_dict = {field: getattr(todo, field) for field in todo.dict()}
        todo_json = json.dumps(todo_dict).encode("utf-8")
        print("todoJSON:", todo_json)
        # Produce message
        await producer.send_and_wait("todos", todo_json)
        # session.add(todo)
        # session.commit()
        # session.refresh(todo)
        return todo


@app.get("/todos/", response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)]):
        todos = session.exec(select(Todo)).all()
        return todos 
    