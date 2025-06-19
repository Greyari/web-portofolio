import cv2
import asyncio
import aiohttp
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole
from ultralytics import YOLO
import av
import numpy as np

pcs = set()
model = YOLO("yolov8n.pt")  # Pastikan model sudah diunduh

class YOLOCameraStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)

    async def recv(self):
        pts, time_base = await self.next_timestamp()
        ret, frame = self.cap.read()
        if not ret:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
        else:
            frame = cv2.resize(frame, (640, 480))
            results = model(frame, verbose=False)

            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls)
                    cls_name = model.names[cls_id].lower()
                    if cls_name in ['car', 'truck', 'bus', 'motorcycle']:
                        bx1, by1, bx2, by2 = map(int, box.xyxy[0])
                        cv2.rectangle(frame, (bx1, by1), (bx2, by2), (0, 0, 255), 2)
                        cv2.putText(frame, cls_name, (bx1, by1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        new_frame = av.VideoFrame.from_ndarray(frame, format="bgr24")
        new_frame.pts = pts
        new_frame.time_base = time_base
        return new_frame

async def offer(request):
    params = await request.json()
    offer_dict = params["offer"]
    offer = RTCSessionDescription(sdp=offer_dict["sdp"], type=offer_dict["type"])
    await pc.setRemoteDescription(offer)

    offer_dict = params["offer"]

    # Konversi dict jadi RTCSessionDescription
    offer = RTCSessionDescription(sdp=offer_dict["sdp"], type=offer_dict["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state:", pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    pc.addTrack(YOLOCameraStreamTrack())
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response({
        "answer": {
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        }
    })

async def on_shutdown(app):
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)

app = web.Application()
app.router.add_post("/offer", offer)
app.router.add_static("/", ".")  # Pastikan client.html ada di folder yang sama
app.on_shutdown.append(on_shutdown)

web.run_app(app, port=8080)
