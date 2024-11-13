import pygame  # pygame 모듈 임포트
import os  # 파일 경로 처리를 위한 os 모듈 임포트
import random  # 무작위 선택을 위한 random 모듈 임포트
import math  # 수학 계산을 위한 math 모듈 임포트
import time  # 시간 계산을 위한 time 모듈 임포트

# 초기 설정
pygame.init()  # pygame 초기화
display_info = pygame.display.Info()  # 현재 디스플레이 정보 가져오기
WIDTH = display_info.current_w  # 화면 너비 설정
HEIGHT = int(WIDTH * 9 / 16)  # 16:9 비율에 맞춘 화면 높이 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # 전체 화면 설정
pygame.display.set_caption("물류 수송 게임")  # 게임 창 제목 설정

WHITE = (255, 255, 255)  # 하얀색
FPS = 60  # 초당 프레임 수 설정

# 글꼴 설정
font = pygame.font.Font("font/Maplestory Bold.ttf", 36)  # 텍스트 글꼴 설정

# 자동차 이미지 불러오기
car_images = {
    "left": pygame.image.load(os.path.join("image", "left.png")),
    "right": pygame.image.load(os.path.join("image", "right.png")),
    "front": pygame.image.load(os.path.join("image", "front.png")),
    "back": pygame.image.load(os.path.join("image", "back.png"))
}

# 장애물 이미지 불러오기 및 크기 조정
obstacle_images = [pygame.image.load(os.path.join("image", f"티니핑_{i}.png")) for i in range(1, 11)]
obstacle_images = [pygame.transform.scale(img, (30, 30)) for img in obstacle_images]  # 이미지 크기 조정

# 픽업 및 드롭존 이미지 불러오기 및 크기 조정
pickup_image = pygame.image.load(os.path.join("image", "basket.png"))
pickup_image = pygame.transform.scale(pickup_image, (100, 100))  # 픽업존 이미지 크기 조정
drop_image = pygame.image.load(os.path.join("image", "robot.png"))
drop_image = pygame.transform.scale(drop_image, (100, 100))  # 드롭존 이미지 크기 조정

# 탄환 클래스 정의 (장애물 이미지 사용)
class Bullet:
    def __init__(self, x, y, angle, speed):
        self.x = x  # x 좌표
        self.y = y  # y 좌표
        self.angle = angle  # 이동 각도
        self.speed = speed  # 이동 속도
        self.image = random.choice(obstacle_images)  # 무작위로 장애물 이미지 선택
        self.rect = self.image.get_rect(center=(x, y))  # 이미지의 중심 좌표 설정

    # 탄환 업데이트 함수
    def update(self):
        # 각도에 따라 탄환 이동
        self.x += self.speed * math.cos(math.radians(self.angle))  # x 좌표 이동
        self.y += self.speed * math.sin(math.radians(self.angle))  # y 좌표 이동
        self.rect.center = (self.x, self.y)  # 이동 후 rect 중심 좌표 업데이트

    # 탄환 그리기 함수
    def draw(self, screen):
        screen.blit(self.image, self.rect)  # 화면에 탄환 이미지 그리기

# 탄환 패턴 생성 함수
def spawn_radial_bullets(x, y, speed, bullet_count):
    bullets = []
    angle_gap = 360 / bullet_count  # 각도 간격 계산
    for i in range(bullet_count):
        angle = i * angle_gap
        bullets.append(Bullet(x, y, angle, speed))  # 새로운 탄환 추가
    return bullets

# 게임 초기화
car_pos = [WIDTH // 2 + 30, HEIGHT - 100]  # 자동차 시작 위치
car_speed = 5  # 자동차 속도
car_rect = pygame.Rect(car_pos[0], car_pos[1], 50, 50)  # 자동차 위치 rect 설정
pickup_zone = pygame.Rect(WIDTH - 150, HEIGHT // 2 - 25, 50, 50)  # 픽업존 위치 설정
drop_zone = pygame.Rect(50, HEIGHT // 2 - 25, 50, 50)  # 드롭존 위치 설정
carrying_item = False  # 물체를 운반 중인지 여부

# 초기 변수 설정
car_direction = "front"  # 초기 자동차 방향
current_image = car_images[car_direction]  # 현재 자동차 이미지
bullets = []  # 생성된 탄환 목록
radial_spawn_timer = 60  # 탄환 생성 타이머
remaining_items = 5  # 남은 운반 물체 개수
lives = 3  # 초기 목숨 개수

# 무적 및 하트 상태 설정
start_time = time.time()  # 무적 시작 시간
invincibility_duration = 2  # 무적 지속 시간
is_invincible = True  # 무적 상태 여부

# 물체 집기 및 내려놓기 메시지 변수
pickup_message = ""
drop_message = ""
pickup_time = None
drop_time = None
message_duration = 2  # 메시지 표시 시간 (초)

clock = pygame.time.Clock()
running = True  # 게임 루프 상태
game_over = False  # 게임 오버 여부
game_clear = False  # 게임 클리어 여부

while running:
    screen.fill(WHITE)  # 화면을 하얀색으로 채움
    
    # 게임 종료 메시지 표시
    if game_over:
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()   # 
        pygame.time.delay(2000)  # 메시지 표시 후 2초 대기
        break

    if game_clear:
        game_clear_text = font.render("Clear!", True, (0, 128, 0))
        screen.blit(game_clear_text, (WIDTH // 2 - game_clear_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)  # 메시지 표시 후 2초 대기
        break

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # 게임 루프 종료
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  # ESC 키로 게임 종료

    # 무적 상태 확인
    if is_invincible and (time.time() - start_time >= invincibility_duration):
        is_invincible = False  # 무적 상태 해제

    # 탄환 패턴 생성
    if radial_spawn_timer >= FPS:
        bullets.extend(spawn_radial_bullets(WIDTH // 2, HEIGHT // 2, 3, 12))
        radial_spawn_timer = 0

    radial_spawn_timer += 0.2

    # 키보드 입력 및 자동차 방향 업데이트
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_rect.left > 0:
        car_rect.x -= car_speed
        car_direction = "left"
    elif keys[pygame.K_RIGHT] and car_rect.right < WIDTH:
        car_rect.x += car_speed
        car_direction = "right"
    elif keys[pygame.K_UP] and car_rect.top > 0:
        car_rect.y -= car_speed
        car_direction = "back"
    elif keys[pygame.K_DOWN] and car_rect.bottom < HEIGHT:
        car_rect.y += car_speed
        car_direction = "front"

    # 자동차 이미지 업데이트
    current_image = car_images[car_direction]

    # 탄환 업데이트 및 그리기
    for bullet in bullets[:]:
        bullet.update()
        bullet.draw(screen)
        # 탄환이 화면을 벗어나면 제거
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)
        elif car_rect.collidepoint(bullet.x, bullet.y) and not is_invincible:
            print("탄환 충돌!")
            lives -= 1
            car_rect.topleft = (WIDTH // 2 + 30, HEIGHT - 100)
            start_time = time.time()
            is_invincible = True

            if lives <= 0:
                game_over = True

    # 로봇팔 동작
    if car_rect.colliderect(pickup_zone) and not carrying_item:
        carrying_item = True
        pickup_message = "물체를 집었습니다!"
        pickup_time = time.time()

    elif car_rect.colliderect(drop_zone) and carrying_item:
        carrying_item = False
        drop_message = "물체를 내려놓았습니다!"
        drop_time = time.time()
        remaining_items -= 1
        if remaining_items <= 0:
            game_clear = True
        
    radial_spawn_timer += (5 - remaining_items) * 0.08

    # 남은 물체 개수와 하트 표시
    items_text = font.render(f"남은 물체 개수: {remaining_items}", True, (0, 0, 0))
    lives_text = font.render(f"하트: {'♥' * lives}", True, (255, 0, 0))
    screen.blit(items_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    # 메시지 표시 (픽업 및 드롭)
    if pickup_time and time.time() - pickup_time < message_duration:
        pickup_text = font.render(pickup_message, True, (0, 0, 0))
        screen.blit(pickup_text, (WIDTH // 2 - pickup_text.get_width() // 2, 100))
    else:
        pickup_message = ""

    if drop_time and time.time() - drop_time < message_duration:
        drop_text = font.render(drop_message, True, (0, 0, 0))
        screen.blit(drop_text, (WIDTH // 2 - drop_text.get_width() // 2, 150))
    else:
        drop_message = ""

    # 픽업 및 드롭존 이미지 표시
    screen.blit(pickup_image, pickup_zone.topleft)
    screen.blit(drop_image, drop_zone.topleft)

    # 자동차 그리기
    screen.blit(current_image, car_rect.topleft)

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
