import pygame
import os
import random

# 초기 설정
pygame.init()
display_info = pygame.display.Info()

# 비율 설정 (16:9 또는 4:3)
ASPECT_RATIO = 16 / 9
WIDTH = display_info.current_w
HEIGHT = int(WIDTH / ASPECT_RATIO)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("물류 수송 게임")

# 색상 및 속성 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
FPS = 60

# 이미지 로드
car_images = {
    "left": pygame.image.load(os.path.join("image", "left.png")),
    "right": pygame.image.load(os.path.join("image", "right.png")),
    "front": pygame.image.load(os.path.join("image", "front.png")),
    "back": pygame.image.load(os.path.join("image", "back.png"))
}
current_image = car_images["front"]

# 자동차 초기화
car_pos = [100, HEIGHT - 100]
car_speed = 5
car_rect = current_image.get_rect(topleft=car_pos)

# 장애물 이미지 로드 및 초기화
obstacle_images = [pygame.image.load(os.path.join("image", f"티니핑_{i}.png")) for i in range(1, 11)]
obstacles = []
for img in obstacle_images:
    img = pygame.transform.scale(img, (50, 50))  # 작은 크기로 변환
    pos_x = random.randint(200, WIDTH - 100)
    pos_y = random.randint(100, HEIGHT - 200)
    direction = random.choice(["horizontal", "vertical"])
    obstacles.append({"img": img, "rect": img.get_rect(topleft=(pos_x, pos_y)), "dir": direction, "speed": 2})

# 로봇팔 및 물체 위치 설정
pickup_zone = pygame.Rect(WIDTH - 150, HEIGHT // 2 - 25, 50, 50)
drop_zone = pygame.Rect(50, HEIGHT // 2 - 25, 50, 50)
carrying_item = False

# 게임 루프
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC 키로 종료
                running = False
    
    # 키보드 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_rect.left > 0:
        car_rect.x -= car_speed
        current_image = car_images["left"]
    if keys[pygame.K_RIGHT] and car_rect.right < WIDTH:
        car_rect.x += car_speed
        current_image = car_images["right"]
    if keys[pygame.K_UP] and car_rect.top > 0:
        car_rect.y -= car_speed
        current_image = car_images["back"]
    if keys[pygame.K_DOWN] and car_rect.bottom < HEIGHT:
        car_rect.y += car_speed
        current_image = car_images["front"]
    
    # 장애물 이동 및 그리기
    for obstacle in obstacles:
        if obstacle["dir"] == "horizontal":
            obstacle["rect"].x += obstacle["speed"]
            if obstacle["rect"].right >= WIDTH or obstacle["rect"].left <= 200:
                obstacle["speed"] *= -1  # 경계에 도달하면 반대 방향으로 이동
        elif obstacle["dir"] == "vertical":
            obstacle["rect"].y += obstacle["speed"]
            if obstacle["rect"].bottom >= HEIGHT or obstacle["rect"].top <= 100:
                obstacle["speed"] *= -1  # 경계에 도달하면 반대 방향으로 이동
        
        screen.blit(obstacle["img"], obstacle["rect"])
        if car_rect.colliderect(obstacle["rect"]):
            print("충돌 발생!")
            car_rect.x, car_rect.y = 100, HEIGHT - 100  # 시작 위치로 되돌리기

    # 로봇팔 동작
    if car_rect.colliderect(pickup_zone) and not carrying_item:
        carrying_item = True
        print("물체를 집었습니다!")
    elif car_rect.colliderect(drop_zone) and carrying_item:
        carrying_item = False
        print("물체를 내려놓았습니다!")
    
    # 픽업 및 드롭존 표시
    pygame.draw.rect(screen, BLUE, pickup_zone)
    pygame.draw.rect(screen, GREEN, drop_zone)

    # 자동차 그리기
    screen.blit(current_image, car_rect)
    
    # 화면 업데이트
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
