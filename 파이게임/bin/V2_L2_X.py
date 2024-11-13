import pygame
import os
import random
import math
import time

# 초기 설정
pygame.init()
display_info = pygame.display.Info()
WIDTH = display_info.current_w
HEIGHT = int(WIDTH * 9 / 16)  # 16:9 비율 유지
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("물류 수송 게임")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FPS = 60

# 글꼴 설정
font = pygame.font.Font("font/Maplestory Bold.ttf", 36)

# 탄환 클래스 정의
class Bullet:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.radius = 5

    def update(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

# 패턴 생성 함수
def spawn_radial_bullets(x, y, speed, bullet_count):
    bullets = []
    angle_gap = 360 / bullet_count
    for i in range(bullet_count):
        angle = i * angle_gap
        bullets.append(Bullet(x, y, angle, speed))
    return bullets

# 게임 초기화
car_pos = [WIDTH // 2 + 30, HEIGHT - 100]
car_speed = 5
car_rect = pygame.Rect(car_pos[0], car_pos[1], 50, 50)
pickup_zone = pygame.Rect(WIDTH - 150, HEIGHT // 2 - 25, 50, 50)
drop_zone = pygame.Rect(50, HEIGHT // 2 - 25, 50, 50)
carrying_item = False

# 초기 변수 설정
bullets = []
radial_spawn_timer = 60
remaining_items = 5
lives = 3

# 무적 및 하트 상태 설정
start_time = time.time()
invincibility_duration = 2
is_invincible = True

# 물체 집기 및 내려놓기 메시지 변수
pickup_message = ""
drop_message = ""
pickup_time = None
drop_time = None
message_duration = 2  # 메시지 표시 시간 (초)

clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # 무적 상태 확인
    if is_invincible and (time.time() - start_time >= invincibility_duration):
        is_invincible = False

    # 탄환 패턴 생성
    if radial_spawn_timer >= FPS:
        bullets.extend(spawn_radial_bullets(WIDTH // 2, HEIGHT // 2, 3, 12))
        radial_spawn_timer = 0

    radial_spawn_timer += 0.2

    # 키보드 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_rect.left > 0:
        car_rect.x -= car_speed
    if keys[pygame.K_RIGHT] and car_rect.right < WIDTH:
        car_rect.x += car_speed
    if keys[pygame.K_UP] and car_rect.top > 0:
        car_rect.y -= car_speed
    if keys[pygame.K_DOWN] and car_rect.bottom < HEIGHT:
        car_rect.y += car_speed

    # 탄환 업데이트 및 그리기
    for bullet in bullets[:]:
        bullet.update()
        bullet.draw(screen)
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)
        elif car_rect.collidepoint(bullet.x, bullet.y) and not is_invincible:
            print("탄환 충돌!")
            lives -= 1
            car_rect.topleft = (WIDTH // 2 + 30, HEIGHT - 100)
            start_time = time.time()
            is_invincible = True
            if lives <= 0:
                print("게임 오버!")
                running = False

    # 로봇팔 동작
    if car_rect.colliderect(pickup_zone) and not carrying_item:
        carrying_item = True
        pickup_message = "물체 수송 준비 완료!"  # 집었을 때 메시지
        pickup_time = time.time()

    elif car_rect.colliderect(drop_zone) and carrying_item:
        carrying_item = False
        drop_message = "물체 수송 완료!"  # 내려놓았을 때 메시지
        drop_time = time.time()
        remaining_items -= 1
        if remaining_items <= 0:
            print("모든 물체를 옮겼습니다! 게임 종료.")
            running = False

    radial_spawn_timer += (5 - remaining_items) * 0.08

    # 남은 물체 개수와 하트 표시
    items_text = font.render(f"남은 물체 개수: {remaining_items}", True, (0, 0, 0))
    lives_text = font.render(f"하트: {'♥' * lives}", True, RED)
    screen.blit(items_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    # 메시지 표시 (픽업 및 드롭)
    if pickup_time and time.time() - pickup_time < message_duration:
        pickup_text = font.render(pickup_message, True, (0, 0, 0))
        screen.blit(pickup_text, (WIDTH // 2 - pickup_text.get_width() // 2, 100))
    else:
        pickup_message = ""  # 시간 초과 시 메시지 제거

    if drop_time and time.time() - drop_time < message_duration:
        drop_text = font.render(drop_message, True, (0, 0, 0))
        screen.blit(drop_text, (WIDTH // 2 - drop_text.get_width() // 2, 150))
    else:
        drop_message = ""  # 시간 초과 시 메시지 제거

    # 픽업 및 드롭존 표시
    pygame.draw.rect(screen, BLUE, pickup_zone)
    pygame.draw.rect(screen, GREEN, drop_zone)

    # 자동차 그리기
    pygame.draw.rect(screen, (0, 0, 255), car_rect)

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
