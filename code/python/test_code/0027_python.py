# From: ASUS ROG Strix G16CHR-XS776S Specs
# Date: 2025-10-04T17:35:32.276000
# Context: ### Santa Letter App: A Fun Parent-Child Christmas Wish Builder

Absolutely, I can code this for you! Based on your description, I've built a **simple desktop prototype app** using Python and Pygame (...

import pygame
import sys
import json
from datetime import datetime
import os

# Initialize Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Santa's Wish Workshop")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Colors
WHITE = (255, 255, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)

# Hardcoded gifts (from 2025 Amazon deals, under $50, age-filtered)
GIFTS = [
    {"name": "Crayola Magic Light Brush", "price": 20, "age_min": 3, "desc": "Mess-free painting fun!", "link": "https://www.amazon.com/Crayola-Color-Wonder-Magic-Painting/dp/B084Y3DLFJ"},
    {"name": "Jellycat Frog Plush", "price": 25, "age_min": 1, "desc": "Cuddly amphibian friend!", "link": "https://www.amazon.com/Stuffed-Animals-Plush-Toys-Jellycat-Games/s?rh=n%253A166461011%252Cp_89%253AJellycat"},
    {"name": "Melissa & Doug Puzzle", "price": 15, "age_min": 3, "desc": "Wooden animal puzzle!", "link": "https://www.amazon.com/melissa-doug-puzzles/s?k=melissa%2Band%2Bdoug%2Bpuzzles"},
    {"name": "Hungry Caterpillar Train", "price": 30, "age_min": 1, "desc": "Colorful wooden train set!", "link": "https://www.amazon.com/KIDS-PREFERRED-Hungry-Caterpillar-Wooden/dp/B08WRSCMG3"},
    {"name": "Infantino Sensory Blocks", "price": 20, "age_min": 0, "desc": "Press & stack for baby!", "link": "https://www.amazon.com/Infantino-Sensory-Press-Stay-Blocks/dp/B00VXMY36G"}
]

# Simple auth (demo only - expand with hashing/DB for real app)
USERS = {"parent": {"user": "mom", "pass": "santa123"}}
state = {"mode": "login", "budget": 0, "age": 0, "selected_gifts": [], "custom_text": "", "naughty_nice": 50, "parent_help": False}

def draw_text(text, font, color, x, y):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))

def animate_roll_letter():
    # Simple parchment roll animation
    for i in range(0, SCREEN_WIDTH, 10):
        screen.fill(WHITE)
        # Draw "letter" rectangle shrinking
        pygame.draw.rect(screen, (255, 248, 220), (SCREEN_WIDTH//2 - i//2, SCREEN_HEIGHT//2 - 50, i, 100))
        draw_text("Rolling up your letter...", small_font, BLACK, SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 60)
        pygame.display.flip()
        clock.tick(60)
    # "Whisk away" sparkle effect
    for _ in range(30):
        screen.fill(BLUE)  # North Pole sky
        # Fake sparkles (circles)
        for _ in range(5):
            pygame.draw.circle(screen, GOLD, (pygame.math.Vector2(SCREEN_WIDTH//2, SCREEN_HEIGHT//2).rotate(pygame.time.get_ticks() / 10)[:2]), 5)
        draw_text("Off to the North Pole!", small_font, WHITE, SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 + 50)
        pygame.display.flip()
        clock.tick(30)

def save_wishlist():
    wishlist = {
        "date": datetime.now().isoformat(),
        "selected_gifts": state["selected_gifts"],
        "custom": state["custom_text"],
        "total": sum(g["price"] for g in state["selected_gifts"]),
        "links": [g["link"] for g in state["selected_gifts"]],
        "naughty_nice": state["naughty_nice"]
    }
    with open("santa_wishlist.txt", "w") as f:
        f.write(json.dumps(wishlist, indent=2))
    print("Wishlist saved! Check santa_wishlist.txt for Amazon links.")

# Main loop
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if state["mode"] == "parent_setup":
                if event.key == pygame.K_RETURN:
                    state["mode"] = "child_select"
            elif state["mode"] == "child_select":
                # Custom text input (simplified - use for demo)
                if event.key == pygame.K_RETURN and state["custom_text"]:
                    state["mode"] = "letter_build"
            elif state["mode"] == "letter_build":
                if event.key == pygame.K_SPACE:  # Send letter
                    animate_roll_letter()
                    # Santa response
                    screen.fill(GREEN)
                    draw_text("Ho ho ho! Dear [Child], your wishes are noted. Keep being nice! - Santa", small_font, WHITE, 50, SCREEN_HEIGHT//2)
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    save_wishlist()
                    state["mode"] = "done"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if state["mode"] == "login":
                # Parent login button (rect check)
                if 300 <= mouse_pos[0] <= 500 and 400 <= mouse_pos[1] <= 450:
                    # Dummy check - in real, validate input
                    state["mode"] = "parent_setup"
            elif state["mode"] == "child_select":
                # Gift selection (click to add if in budget/age)
                for i, gift in enumerate([g for g in GIFTS if g["age_min"] <= state["age"]]):
                    rect = pygame.Rect(50 + (i % 3) * 250, 100 + (i // 3) * 150, 200, 120)
                    if rect.collidepoint(mouse_pos) and sum(s["price"] for s in state["selected_gifts"]) + gift["price"] <= state["budget"]:
                        state["selected_gifts"].append(gift)
            elif state["mode"] == "letter_build":
                # Naughty/nice slider (click to adjust 0-100)
                if 100 <= mouse_pos[0] <= 700:
                    state["naughty_nice"] = (mouse_pos[0] - 100) // 6

    # Render based on mode
    if state["mode"] == "login":
        draw_text("Parent Login", font, RED, SCREEN_WIDTH//2 - 100, 100)
        draw_text("User: mom | Pass: santa123", small_font, BLACK, SCREEN_WIDTH//2 - 120, 200)
        pygame.draw.rect(screen, GREEN, (300, 400, 200, 50))
        draw_text("Sign In", small_font, WHITE, 350, 410)
    elif state["mode"] == "parent_setup":
        draw_text("Set Budget & Age", font, BLUE, SCREEN_WIDTH//2 - 120, 100)
        # Input sim (use keys for budget/age in full version)
        draw_text(f"Budget: ${state['budget']} | Age: {state['age']}", small_font, BLACK, 50, 200)
        draw_text("Press ENTER to save & switch to child", small_font, BLACK, 50, 300)
        # Demo: Auto-set if 0
        if state["budget"] == 0: state["budget"] = 50
        if state["age"] == 0: state["age"] = 5
    elif state["mode"] == "child_select":
        draw_text("Shopping Spree with Santa!", font, GREEN, SCREEN_WIDTH//2 - 150, 50)
        draw_text(f"Budget Left: ${state['budget'] - sum(g['price'] for g in state['selected_gifts'])}", small_font, RED, 50, 80)
        # Draw gift cards
        filtered_gifts = [g for g in GIFTS if g["age_min"] <= state["age"]]
        for i, gift in enumerate(filtered_gifts):
            x, y = 50 + (i % 3) * 250, 100 + (i // 3) * 150
            pygame.draw.rect(screen, BLUE, (x, y, 200, 120))
            draw_text(gift["name"], small_font, WHITE, x+10, y+10)
            draw_text(f"${gift['price']}", small_font, GOLD, x+10, y+40)
            draw_text(gift["desc"][:20], pygame.font.Font(None, 18), WHITE, x+10, y+60)
        draw_text("Click gifts to add! Press ENTER for custom wish.", small_font, BLACK, 50, SCREEN_HEIGHT - 50)
        if state["parent_help"]:
            draw_text("Parent Help ON - Guide your child!", small_font, GREEN, SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100)
    elif state["mode"] == "letter_build":
        draw_text("Build Your Letter!", font, GOLD, SCREEN_WIDTH//2 - 120, 50)
        # Selected gifts list
        y = 100
        for gift in state["selected_gifts"]:
            draw_text(f"- {gift['name']} (${gift['price']})", small_font, BLACK, 50, y)
            y += 30
        draw_text("Custom Wish:", small_font, BLACK, 50, y)
        draw_text(state["custom_text"] or "Type your special request...", small_font, BLACK, 100, y+30)
        # Naughty/Nice meter
        pygame.draw.rect(screen, GRAY := (200, 200, 200), (100, y+60, 600, 20))
        nice_width = (state["naughty_nice"] / 100) * 600
        pygame.draw.rect(screen, GREEN if state["naughty_nice"] > 50 else RED, (100, y+60, nice_width, 20))
        draw_text("Naughty <--- Nice", small_font, BLACK, 100, y+90)
        draw_text("SPACE to send to Santa!", small_font, BLACK, 50, SCREEN_HEIGHT - 50)
    elif state["mode"] == "done":
        draw_text("Letter Sent! Check email for links, Parent!", font, GREEN, SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2)
        draw_text("Merry Christmas!", small_font, RED, SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 50)
        pygame.time.wait(5000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()