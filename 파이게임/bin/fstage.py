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
FPS = 60

# 글꼴 설정
font = pygame.font.Font("font/Maplestory Bold.ttf", 36)

# 자동차 이미지 불러오기 (크기 조정: 40x40)
car_images = {
    "left": pygame.transform.scale(pygame.image.load(os.path.join("image", "left.png")), (40, 40)),
    "right": pygame.transform.scale(pygame.image.load(os.path.join("image", "right.png")), (40, 40)),
    "front": pygame.transform.scale(pygame.image.load(os.path.join("image", "front.png")), (40, 40)),
    "back": pygame.transform.scale(pygame.image.load(os.path.join("image", "back.png")), (40, 40))
}

# 장애물 이미지 불러오기 및 크기 조정
obstacle_images = [pygame.image.load(os.path.join("image", f"티니핑_{i}.png")) for i in range(1, 11)]
obstacle_images = [pygame.transform.scale(img, (30, 30)) for img in obstacle_images]

# 픽업 및 드롭존 이미지 불러오기 및 크기 조정
pickup_image = pygame.image.load(os.path.join("image", "basket.png"))
pickup_image = pygame.transform.scale(pickup_image, (100, 100))
drop_image = pygame.image.load(os.path.join("image", "robot.png"))
drop_image = pygame.transform.scale(drop_image, (100, 100))

# 픽업 및 드롭존 위치 및 크기 설정
pickup_zone = pickup_image.get_rect(topleft=(WIDTH - 150, HEIGHT // 2 - 50))
drop_zone = drop_image.get_rect(topleft=(50, HEIGHT // 2 - 50))

# 탄환 클래스 정의 (장애물 이미지 사용)
class Bullet:
    def __init__(self, x, y, angle, speed, image):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 여러 가지 장애물 패턴 생성 함수
def spawn_pattern(x, y, pattern_type):
    bullets = []
    if pattern_type == "radial":
        for i in range(12):
            angle = i * 30
            bullets.append(Bullet(x, y, angle, 4, random.choice(obstacle_images)))
    elif pattern_type == "spiral":
        for i in range(6):
            angle = (i * 30) + time.time() * 20  # 시간에 따라 회전
            bullets.append(Bullet(x, y, angle, 3, random.choice(obstacle_images)))
    elif pattern_type == "wave":
        for i in range(6):
            angle = 180 + math.sin(pygame.time.get_ticks() / 500) * 45
            bullets.append(Bullet(x + i * 50, y, angle, 4, random.choice(obstacle_images)))
    return bullets

# 게임 초기화
car_pos = [WIDTH // 2 + 30, HEIGHT - 100]
car_speed = 5
car_rect = pygame.Rect(car_pos[0], car_pos[1], 40, 40)
carrying_item = False

# 초기 변수 설정
car_direction = "front"
current_image = car_images[car_direction]
bullets = []
radial_spawn_timer = 60
remaining_items = 5
lives = 3

# 무적 및 하트 상태 설정
start_time = time.time()
invincibility_duration = 2
is_invincible = True

# 메시지 변수
pickup_message = ""
drop_message = ""
pickup_time = None
drop_time = None
message_duration = 2  # 메시지 표시 시간 (초)

# 게임 종료 메시지 변수
game_over_message = ""
clear_message = ""
end_time = None

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

    # 장애물 패턴 생성 및 타이머 조정
    if radial_spawn_timer >= FPS:
        pattern_type = random.choice(["radial", "spiral", "wave"])
        bullets.extend(spawn_pattern(WIDTH // 2, HEIGHT // 2, pattern_type))
        radial_spawn_timer = 0

    radial_spawn_timer += 1.5

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
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)
        elif car_rect.collidepoint(bullet.x, bullet.y) and not is_invincible:
            lives -= 1
            car_rect.topleft = (WIDTH // 2 + 30, HEIGHT - 100)
            start_time = time.time()
            is_invincible = True
            if lives <= 0:
                game_over_message = "게임 오버!"
                end_time = time.time()
                running = False

    # 픽업 및 드롭 메시지 표시
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
            clear_message = "클리어!"
            end_time = time.time()
            running = False

    # 메시지 표시
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

    # 남은 물체 개수와 하트 표시
    items_text = font.render(f"남은 물체 개수: {remaining_items}", True, (0, 0, 0))
    lives_text = font.render(f"하트: {'♥' * lives}", True, (255, 0, 0))
    screen.blit(items_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    radial_spawn_timer += 0.4 * (5 - remaining_items)

    # 픽업 및 드롭존 이미지 표시
    screen.blit(pickup_image, pickup_zone.topleft)
    screen.blit(drop_image, drop_zone.topleft)

    # 자동차 그리기
    screen.blit(current_image, car_rect.topleft)

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(FPS)

# 게임 종료 시 메시지 표시
if game_over_message:
    while time.time() - end_time < 2:
        screen.fill(WHITE)
        game_over_text = font.render(game_over_message, True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

if clear_message:
    while time.time() - end_time < 2:
        screen.fill(WHITE)
        clear_text = font.render(clear_message, True, (0, 128, 0))
        screen.blit(clear_text, (WIDTH // 2 - clear_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

pygame.quit()
