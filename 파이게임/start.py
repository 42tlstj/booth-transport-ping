import pygame
import sys
import os

# Pygame 초기화
pygame.init()

# 화면 설정
display_info = pygame.display.Info()
WIDTH = display_info.current_w
HEIGHT = int(WIDTH * 9 / 16)  # 16:9 비율 유지
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("3 Stage Selector")

# 색상 및 배경 설정
WHITE = (255, 255, 255)
screen.fill(WHITE)

# 폰트 설정
font_path = "font/Maplestory Bold.ttf"
font = pygame.font.Font(font_path, 36)

# 텍스트 렌더링
text_click_stage = font.render("플레이를 원하는 단계를 클릭해주세요!", True, (0, 0, 0))
text_wait = font.render("버튼을 누르고 잠시 기다려주세요 (좀 느려요)", True, (0, 0, 0))

# 텍스트 위치
text_click_stage_rect = text_click_stage.get_rect(center=(WIDTH // 2, HEIGHT - 100))
text_wait_rect = text_wait.get_rect(center=(WIDTH // 2, HEIGHT - 50))

# 이미지 로드
image1 = pygame.image.load('image/step1.png')
image2 = pygame.image.load('image/step2.png')
image3 = pygame.image.load('image/step3.png')

# 이미지 크기 조정
image_size = (367, 600)
image1 = pygame.transform.scale(image1, image_size)
image2 = pygame.transform.scale(image2, image_size)
image3 = pygame.transform.scale(image3, image_size)

# 이미지 위치
image1_rect = image1.get_rect(topleft=(50, 50))
image2_rect = image2.get_rect(topleft=(450, 50))
image3_rect = image3.get_rect(topleft=(850, 50))

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if image1_rect.collidepoint(event.pos):
                os.system('stage1.py')
            elif image2_rect.collidepoint(event.pos):
                os.system('stage2.py')
            elif image3_rect.collidepoint(event.pos):
                os.system('stage3.py')

    # 화면 그리기
    screen.fill(WHITE)
    screen.blit(image1, image1_rect)
    screen.blit(image2, image2_rect)
    screen.blit(image3, image3_rect)
    screen.blit(text_click_stage, text_click_stage_rect)
    screen.blit(text_wait, text_wait_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
