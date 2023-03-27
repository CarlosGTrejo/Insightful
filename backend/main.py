from fastapi import FastAPI, WebSocket
import uvicorn
import audio_utils
import logging
from time import perf_counter

app = FastAPI()

# Setup custom logger
logging_config = uvicorn.config.LOGGING_CONFIG  # type: ignore
logging_config['loggers']['uvicorn']['level'] = 'INFO'
logging_config['loggers']['main'] = {
    'handlers': ['default'],
    'level': 'INFO',
    'propagate': False
}
LOG = logging.getLogger('main')


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    '''Handles client websocket connections, file transmissions, and file processing'''
    await websocket.accept()
    try:
        while True:
            start = perf_counter()  # begin processing timer
            file_bytes = await websocket.receive_bytes()  # Receive File
            LOG.info(f"Received {len(file_bytes)} bytes of data from WebSocket client")

            # Process file (example: convert file to flac)
            # converted_file = audio_utils.mp3_to_flac(file_bytes)  # 1.0262s / 2,727ms
            converted_file = audio_utils.audio_to_flac(file_bytes)  # 1.0252s / 2,762ms
            end = perf_counter()

            # Return processed file to client
            await websocket.send_bytes(converted_file)

            LOG.info(f'File was processed in {end-start:.4f} seconds')

    except Exception as e:
        LOG.exception(f'Exception occurred: {e}')


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        log_config=logging_config,
        reload=True)
