import logging
import utils
from time import perf_counter

import transcribe
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

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
            mimetype = await websocket.receive_text()  # Receive File mimetype

            LOG.info(f"Received {len(file_bytes)} bytes of data from WebSocket client")

            if mimetype == 'dev/file':  # Check for development/testing mode
                LOG.warning('Development mode enabled')
                transcript, summary = utils.dev()
            else:  # Else upload file to deepgram and continue as normal
                LOG.info('Production mode enabled')
                transcript, summary = await transcribe.using_deepgram(file_bytes, mimetype)
            end = perf_counter()

            # Return processed file to client
            await websocket.send_json({'transcript': transcript, 'summary': summary})

            LOG.info(f'File was processed in {end-start:.4f} seconds')
            await websocket.close()
    except WebSocketDisconnect:
        LOG.info('File Processed, closing websocket')
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
