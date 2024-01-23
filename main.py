
from camera import VideoCamera
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import StreamingResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.route('/') #맨 처음 접속할 화면
def index(request: Request): # 객체 탐지 결과 화면이 송출되는 페이지

    return templates.TemplateResponse("index.html", {'request': request})

def gen(camera): # camera = camera.py에 있는 VidwoCamera 객체다.
    while True: # 계속 반복시킨다.
        frame = camera.get_frame() # 실시간 영상을 통해 디텍션한 결과 이미지 프레임을 받아오는 것.
        # 함수에서 차례대로 값을 return 해주는 yield 함수
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# index.html에 있는 img 태그는 url 기반으로 아래 함수에서 이미지를 가져옴.
@app.get('/video_feed')
def video_feed():            # 리스폰 반응 함수 yeild가 반복적(while문 때문에)으로 리턴을 하는걸 받는다
    
    # StreamingRespinse -> 미디어 매체를 응답으로 반환하는 함수, 오직 FastApi에만 있는
                            #gen(VideoCamera()) -> 바루 위에 있는 gen함수에 이 스크립트 코드 초반에 있는 import한 VideoCamera() 객체를 던짐
    return StreamingResponse(gen(VideoCamera()),
                    media_type='multipart/x-mixed-replace; boundary=frame') 
                    #미디어 타입 양식

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)


# 가상환경 만들고 설치할 것들(python==3.8.3)
# pip install uvicorn
# pip install fastapi
# pip install ultralytics