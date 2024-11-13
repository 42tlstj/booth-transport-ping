# pygame 개념 + 캐치 수송핑 게임 설명

------------

> 1. pygame 기초 개념 설명
> 2. 집현 발표회 ppt 발표 범위 예상
> 3. 캐치 수송핑 게임 설명

이 문서와 게임은 모두 나무위키, GPT 기반으로 약 3시간의 제작시간을 걸쳐 제작되었습니다. 사소한 오류 등이 있을 수도 있습니다. 집현 발표회 준비용 문서입니다.

------------

## 1. pygame 기초 개념 설명
Python으로 작성 가능한 게임 등의 멀티미디어 표현을 위한 라이브러리이다. SDL 기반이다. 오픈 소스이자 무료 도구이며, Python을 돌릴 수 있는 플랫폼이라면 어디서든 실행할 수 있다. 게임 개발 도구이지만 이미지 프로세스 또는 조이스틱 입력, 음악 재생 등의 기능만 떼어다 쓸 수도 있다.

hello world.py에서 보면 pygame의 기초 작동 방식을 알 수 있다.
더 공부해보고 싶으면 https://www.pygame.org/docs/ 이 사이트를 참고해 공부하자.

```python
import pygame # pygame 모듈의 임포트
import sys # 외장 모듈
from pygame.locals import * # QUIT 등의 pygame 상수들을 로드한다.

width = 600 # 상수 설정
height = 400
white = (255, 255, 255)
black = (  0,   0,   0)
fps = 30

pygame.init() # 초기화

pygame.display.set_caption('Hello, world!') # 창 제목 설정
displaysurf = pygame.display.set_mode((width, height), 0, 32) # 메인 디스플레이를 설정한다
clock = pygame.time.Clock() # 시간 설정

gulimfont = pygame.font.SysFont('굴림', 70) # 서체 설정
helloworld = gulimfont.render('Hello, world!', 1, black) 

hellorect = helloworld.get_rect() # 생성한 이미지의 rect 객체를 가져온다 # .render() 함수에 내용과 안티앨리어싱, 색을 전달하여 글자 이미지 생성
hellorect.center = (width / 2, height / 2) # 해당 rect의 중앙을 화면 중앙에 맞춘다

while True: # 아래의 코드를 무한 반복한다.
    for event in pygame.event.get(): # 발생한 입력 event 목록의 event마다 검사
        if event.type == QUIT: # event의 type이 QUIT에 해당할 경우
            pygame.quit() # pygame을 종료한다
            sys.exit() # 창을 닫는다
    displaysurf.fill(white) # displaysurf를 하얀색으로 채운다
    displaysurf.blit(helloworld, hellorect) # displaysurf의 hellorect의 위치에 helloworld를 입력한다
    
    pygame.display.update() # 화면을 업데이트한다
    clock.tick(fps) # 화면 표시 회수 설정만큼 루프의 간격을 둔다
```

모듈은 pygame을 사용하는데, pygame 모듈들을 사용하기 위해서는 pygame.init(), pygame.quit() 등으로 초기화, 종료를 시켜줘야 한다. 또 디스플레이에 작업한 내용을 보이려면 pygame.display.update()를 시켜줘야 한다.

## 2. 집현 발표회 ppt 발표 범위 예상
내 생각에 집현 발표회 때는 ppt를 이용해 발표를 진행할텐데, 기본적으로 우리가 pygame을 어떻게 공부했는지, 이 코드가 무엇을 설명하는지, 어떻게 작동하는지 이런 것들을 물어볼 것 같다. 집현 심사하는 선생님이 아주 깊은 지식을 알고 있는 것도 아닐 거라서, 우리는 공부했던 내용, 개발한 코드를 잘 정리해 발표하면 될 것이다. 프밍기 시험도 아니고 간단하게 어려워봐야 어떤 코드 짚고 기능 묻는다던지, 그런 것들 질문으로 나올듯. 윤희샘은 그런거 물어볼 것 같고, 서진샘은 이 코드를 만든 이유.. gpt 피셜 같은 질문 나올듯 (알아서 잘 말하면 될듯 !!)
> 1. 파이게임 공부는 어떻게 했나요?
>> 파이게임 사이트에 나와있는 공식 문서를 정리하여 기본적인 파이게임 문법을 공부하였습니다.
> 2. 파이게임 개발은 어떻게 했나요?
>> 공식 문서 정리본을 참고하여 저희가 실제로 제작했던 수송로봇의 방식을 참고하여 제작하였습니다.
> 3. 이 코드, 설명해주세요.
>> (어차피 코드 다 주석 깔고, 실제 집현 발표회 때 주석 넣을지 말지에 따라서 달라질 것 같긴 함.) 이 코드는  ... 이런 기능을 하는 코드입니다.

뭐... GPT 피셜 이런거를 집현 심사회에서 발표할거라고 한다.
1. 프로젝트 목표 및 개요
> 이 프로젝트의 주된 목표가 무엇인가요?
> 프로젝트를 시작하게 된 동기는 무엇인가요?
> 이 프로젝트의 가장 큰 특징은 무엇인가요?
2. 기술적 구성 및 선택 이유
> 이 프로젝트에서 사용한 주요 기술 스택(프레임워크, 언어 등)은 무엇인가요?
> 특정 기술을 선택한 이유는 무엇인가요?
> (특정 기능에 대해) 이 기능은 어떻게 구현되었나요?
3. 개발 과정에서의 어려움 및 해결 방법
> 개발 과정에서 겪은 가장 큰 어려움은 무엇이었나요?
> 어려움을 해결하기 위해 어떤 접근 방식을 취했나요?
> 프로젝트가 예상대로 되지 않았을 때 어떻게 대처했나요?
4. 테스트와 성능
> 이 프로젝트는 어떻게 테스트했나요?
> 성능 최적화를 위해 어떤 부분을 개선했나요?
> 사용자 피드백을 반영한 점이 있나요?
5. 프로젝트 결과와 활용 방안
> 프로젝트 결과물은 실제로 어디에 적용될 수 있나요?
> 향후 개선하고자 하는 계획이나 추가하고 싶은 기능이 있나요?
> 이 프로젝트를 통해 배운 가장 중요한 점은 무엇인가요?
