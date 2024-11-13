import pygame  # pygame 모듈 불러오기
import os  # 운영 체제 관련 모듈
import random  # 무작위 값 생성 모듈
import time  # 시간 관련 모듈

# 초기 설정
pygame.init()  # pygame 초기화
display_info = pygame.display.Info()  # 디스플레이 정보 가져오기
WIDTH = display_info.current_w  # 화면 너비 설정
HEIGHT = int(WIDTH * 9 / 16)  # 16:9 비율로 화면 높이 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # 전체 화면 모드로 설정
pygame.display.set_caption("물류 수송 게임")  # 게임 창 제목 설정

WHITE = (255, 255, 255)  # 흰색 RGB 값
FPS = 60  # 초당 프레임 수 설정

# 글꼴 설정
font = pygame.font.Font("font/Maplestory Bold.ttf", 36)  # 글꼴과 크기 설정

# 자동차 이미지 불러오기
car_images = {
    "left": pygame.image.load(os.path.join("image", "left.png")),  # 왼쪽 방향 이미지
    "right": pygame.image.load(os.path.join("image", "right.png")),  # 오른쪽 방향 이미지
    "front": pygame.image.load(os.path.join("image", "front.png")),  # 앞쪽 방향 이미지
    "back": pygame.image.load(os.path.join("image", "back.png"))  # 뒤쪽 방향 이미지
}

# 장애물 이미지 불러오기 및 크기 조정
obstacle_images = [pygame.image.load(os.path.join("image", f"티니핑_{i}.png")) for i in range(1, 11)]
obstacle_images = [pygame.transform.scale(img, (40, 40)) for img in obstacle_images]  # 이미지 크기 조정

# 픽업 및 드롭존 이미지 불러오기 및 크기 조정
pickup_zone_img = pygame.transform.scale(pygame.image.load(os.path.join("image", "basket.png")), (100, 100))
drop_zone_img = pygame.transform.scale(pygame.image.load(os.path.join("image", "robot.png")), (100, 100))

# 장애물 클래스 정의
class Obstacle:
    def __init__(self, img, pos_x, pos_y, direction, speed, range_distance):
        self.image = img  # 이미지 설정
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))  # 위치 설정
        self.direction = direction  # 이동 방향
        self.speed = speed  # 이동 속도
        self.range_distance = range_distance  # 이동 범위
        self.start_pos = pos_x if direction == "horizontal" else pos_y  # 시작 위치
        self.end_pos = self.start_pos + range_distance  # 끝 위치

    def update(self):  # 장애물 업데이트
        if self.direction == "horizontal":  # 수평 이동
            self.rect.x += self.speed
            if self.rect.left < self.start_pos or self.rect.right > self.end_pos:
                self.speed *= -1  # 방향 반전
        elif self.direction == "vertical":  # 수직 이동
            self.rect.y += self.speed
            if self.rect.top < self.start_pos or self.rect.bottom > self.end_pos:
                self.speed *= -1  # 방향 반전

    def draw(self, screen):  # 장애물 그리기
        if self.direction == "horizontal":
            pygame.draw.line(screen, (255, 229, 204), (self.start_pos, self.rect.centery), (self.end_pos, self.rect.centery), 3)
        elif self.direction == "vertical":
            pygame.draw.line(screen, (255, 229, 204), (self.rect.centerx, self.start_pos), (self.rect.centerx, self.end_pos), 3)
        
        screen.blit(self.image, self.rect)  # 화면에 이미지 그리기

# 장애물 생성 함수
def create_obstacles(num_obstacles):
    obstacles = []  # 장애물 리스트
    for _ in range(num_obstacles):
        img = random.choice(obstacle_images)  # 랜덤 이미지 선택
        pos_x = random.randint(150, WIDTH - 200)  # 랜덤 X 좌표
        pos_y = random.randint(100, HEIGHT - 200)  # 랜덤 Y 좌표
        direction = random.choice(["horizontal", "vertical"])  # 랜덤 방향 선택
        speed = 2  # 이동 속도
        range_distance = random.randint(150, 300)  # 이동 범위
        obstacles.append(Obstacle(img, pos_x, pos_y, direction, speed, range_distance))  # 장애물 추가
    return obstacles

# 메시지 관련 설정
message = ""  # 표시할 메시지
message_timer = 0  # 메시지 타이머
message_duration = 2  # 메시지 표시 시간 (초)

# 게임 초기화
car_pos = [WIDTH // 2 + 30, HEIGHT - 100]  # 자동차 시작 위치
car_speed = 3  # 자동차 속도
car_rect = pygame.Rect(car_pos[0], car_pos[1], 50, 50)  # 자동차 위치와 크기
pickup_zone_rect = pickup_zone_img.get_rect(center=(WIDTH - 150, HEIGHT // 2))  # 픽업존 위치
drop_zone_rect = drop_zone_img.get_rect(center=(150, HEIGHT // 2))  # 드롭존 위치
carrying_item = False  # 물체 운반 여부

# 초기 변수 설정
car_direction = "front"  # 자동차 초기 방향
current_image = car_images[car_direction]  # 현재 자동차 이미지
obstacles = create_obstacles(10)  # 장애물 생성
remaining_items = 5  # 남은 물체 개수
lives = 3  # 남은 목숨

# 무적 및 하트 상태 설정
start_time = time.time()  # 시작 시간
invincibility_duration = 2  # 무적 지속 시간
is_invincible = True  # 무적 상태 여부

clock = pygame.time.Clock()  # 시계 객체
running = True  # 게임 루프 상태
game_over = False  # 게임 오버 여부
game_clear = False  # 게임 클리어 여부

while running:
    screen.fill(WHITE)  # 화면을 흰색으로 채움
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # 게임 종료
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  # ESC 키로 게임 종료

    # 무적 상태 확인
    if is_invincible and (time.time() - start_time >= invincibility_duration):
        is_invincible = False  # 무적 상태 해제

    # 키보드 입력 및 자동차 방향 업데이트
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_rect.left > 0:  # 왼쪽 키
        car_rect.x -= car_speed
        car_direction = "left"
    elif keys[pygame.K_RIGHT] and car_rect.right < WIDTH:  # 오른쪽 키
        car_rect.x += car_speed
        car_direction = "right"
    elif keys[pygame.K_UP] and car_rect.top > 0:  # 위쪽 키
        car_rect.y -= car_speed
        car_direction = "back"
    elif keys[pygame.K_DOWN] and car_rect.bottom < HEIGHT:  # 아래쪽 키
        car_rect.y += car_speed
        car_direction = "front"

    # 자동차 이미지 업데이트
    current_image = car_images[car_direction]

    # 장애물 업데이트 및 충돌 체크
    for obstacle in obstacles:
        obstacle.update()  # 장애물 업데이트
        obstacle.draw(screen)  # 장애물 그리기
        if car_rect.colliderect(obstacle.rect) and not is_invincible:  # 충돌 감지
            print("장애물 충돌!")
            lives -= 1  # 목숨 감소
            car_rect.topleft = (WIDTH // 2 + 30, HEIGHT - 100)  # 자동차 위치 초기화
            start_time = time.time()  # 무적 시작 시간 갱신
            is_invincible = True  # 무적 상태로 전환
            if lives <= 0:  # 목숨이 0이면 게임 오버
                game_over = True
                message = "Game Over"
                message_timer = time.time()

    # 물체 잡기 및 수송 완료 처리
    if car_rect.colliderect(pickup_zone_rect) and not carrying_item:  # 픽업존에서 물체 잡기
        carrying_item = True
        message = "물체를 집었습니다!"
        message_timer = time.time()  # 메시지 타이머 초기화
        print("물체를 집었습니다!")
    elif car_rect.colliderect(drop_zone_rect) and carrying_item:  # 드롭존에서 물체 수송
        carrying_item = False
        message = "물체 수송 완료!"
        message_timer = time.time()
        print("물체를 수송 완료했습니다!")
        remaining_items -= 1  # 남은 물체 개수 감소
        if remaining_items <= 0:  # 모든 물체를 수송하면 게임 클리어
            game_clear = True
            message = "Game Clear!"
            message_timer = time.time()

    # 게임 오버 또는 클리어 처리
    if game_over or game_clear:
        running = False  # 게임 루프 종료

    # 물체 상태에 따라 픽업존 및 드롭존 이미지 그리기
    screen.blit(pickup_zone_img, pickup_zone_rect)
    screen.blit(drop_zone_img, drop_zone_rect)

    # 자동차 이미지 그리기
    screen.blit(current_image, car_rect)

    # 메시지 표시
    if time.time() - message_timer <= message_duration:
        message_surface = font.render(message, True, (255, 0, 0))
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 8))
        screen.blit(message_surface, message_rect)

    pygame.display.flip()  # 화면 업데이트
    clock.tick(FPS)  # FPS 설정

pygame.quit()  # pygame 종료

