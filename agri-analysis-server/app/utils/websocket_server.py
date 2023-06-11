from flask import Flask
import asyncio
import websockets

app = Flask(__name__)

@app.route('/ws')
async def websocket_route():
    websocket = await websockets.serve(update_data, 'localhost', 8000)
    await websocket.wait_closed()

async def update_data(websocket, path):
    # 根据需要实时更新数据
    while True:
        data = await fetch_data()  # 获取最新数据
        await websocket.send(data)  # 发送数据给前端
        await asyncio.sleep(1)  # 控制更新频率

if __name__ == '__main__':
    app.run()
