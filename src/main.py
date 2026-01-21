import pygame
import sys
from data_manager import DataManager
from assets import load_prize_images
from inventory import Inventory
from gacha import GachaSystem

prize_images = load_prize_images()

# Initialize Pygame
pygame.init()
user = DataManager()
inventory = Inventory()
gacha = GachaSystem()
last_prize = None

# Windows Settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gachapon Game")

# Preset Colors
ACTIVE_COLOR = (240, 240, 240)
WHITE = (255, 255, 255)
BACKGROUND_GRAY =(186, 186, 186)
BUTTON_GRAY = (198, 198, 198)
BUTTON_SHADOW_GRAY = (147, 147, 147)
LIGHT_GRAY = (217, 217, 217)
YELLOW = (255, 246, 0)

prize_colors = {
"duck": (255, 246, 0),
"dog": (191, 59, 252),
"bear": (252, 59, 62),
"robot": (59, 104, 252),
}

prize_names_display = {
    "duck": "Golden Duck",
    "dog": "Lucky Dog",
    "bear": "Teddy Bear",
    "robot": "Mini Robot",
}

# Clock
clock = pygame.time.Clock()
running = True

# Variables
user_total_points = ""
user_total_itens = ""
username_text = ""
password_text = ""
rptpassword_text = ""
login_username = ""
login_password = ""
active_field = None
scroll_y = 0
scroll_speed = 40

# Setting Current Screen
current_screen = "menu"

# Fonts
try:
    font_title = pygame.font.Font("assets/fonts/KronaOne-Regular.ttf", 64)
    font_buttons = pygame.font.Font("assets/fonts/KronaOne-Regular.ttf", 36 )
    font_warning = pygame.font.Font("assets/fonts/KronaOne-Regular.ttf", 24)
    font_rarity = pygame.font.Font("assets/fonts/KronaOne-Regular.ttf", 23)
except:
    font_title = pygame.font.SysFont(None, 60)
    font_buttons = pygame.font.SysFont(None, 36)
    font_warning = pygame.font.SysFont(None, 24)
    font_rarity = pygame.font.SysFont(None, 23)

# --- BUTTON DRAW FUNCTION --- #
def draw_button(x, y, w, h, text, font, text_color, button_color, shadow_color, border_color, border_width=2):
    # SHADOW
    pygame.draw.rect(screen, shadow_color, (x, y + 10, w, h), border_radius=16)
    # BUTTON BODY
    pygame.draw.rect(screen, button_color, (x, y, w, h), border_radius=16)
    # BUTTON BORDER
    pygame.draw.rect(screen, border_color, (x, y, w, h), border_radius=16, width=border_width)
    txt = font.render(text, True, text_color)
    txt_rect = txt.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(txt, txt_rect)

    return pygame.Rect(x, y, w, h)

# --- INPUT FIELD DRAW FUNCTION --- #
def draw_input_box(x, y, w, h, text, active, placeholder="", is_password=False):
    color = ACTIVE_COLOR if active else BUTTON_GRAY
    shadow_color = BUTTON_SHADOW_GRAY
    border_color = BUTTON_SHADOW_GRAY
    border_width = 2
    # SHADOW
    pygame.draw.rect(screen, shadow_color, (x, y + 10, w, h), border_radius=16)
    # BODY
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=16)
    # BORDER
    pygame.draw.rect(screen, border_color, (x, y, w, h), border_radius=16, width=border_width)

    # TEXT TO *
    if text == "" and not active:
        display_text = placeholder
        txt_color = (212, 212, 212)
    else:
        display_text = "*" * len(text) if is_password and text else text
        txt_color = BUTTON_SHADOW_GRAY

    txt = font_buttons.render(display_text, True, txt_color)
    txt_rect = txt.get_rect(midleft=(x + 3, y + h // 2))
    screen.blit(txt, txt_rect)
    
    return pygame.Rect(x, y, w, h)

# --- MENU SCREEN --- #
def draw_menu():
    screen.fill(BACKGROUND_GRAY)
    title = font_title.render("Gachapon Game", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 87)))

    btn_guest = draw_button((width // 2 - 258 // 2), 240, 258, 51, "Guest", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_login = draw_button((width // 2 - 258 // 2), 322, 258, 51, "Login", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_signup = draw_button((width // 2 - 258 // 2), 404, 258, 51, "Sign Up", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)

    return btn_guest, btn_login, btn_signup

# --- GUEST SCREEN --- #
def draw_guest():
    screen.fill(BACKGROUND_GRAY)
    title = font_title.render("Continue as guest", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 87)))
    
    warning = font_warning.render("IF YOU CONTINUE AS A GUEST", True, WHITE)
    warning2 = font_warning.render("YOU CAN'T REGISTER YOUR POINTS", True, WHITE)
    screen.blit(warning, warning.get_rect(center=(width // 2, 220)))
    screen.blit(warning2, warning2.get_rect(center=(width // 2, 255)))
    
    btn_continue = draw_button((width // 2 - 258 // 2), 322, 258, 51, "Continue", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_signup = draw_button((width // 2 - 258 // 2), 404, 258, 51, "Sign Up", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_back = draw_button((width // 2 - 258 // 2), 486, 258, 51, "Back", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    return btn_continue, btn_signup, btn_back

# --- LOGIN SCREEN --- #
def draw_login(login_username, login_password, active_field):
    screen.fill(BACKGROUND_GRAY)
    title = font_title.render("Login", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 87)))

    username_box = draw_input_box((width // 2 - 258 // 2), 248, 258, 51, login_username, active_field == "login_username", "Username")
    password_box = draw_input_box((width // 2 - 258 // 2), 330, 258, 51, login_password, active_field == "login_password", "Password", is_password=True)

    btn_login = draw_button((width // 2 - 258 // 2), 412, 258, 51, "Continue", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_back = draw_button((width // 2 - 258 // 2), 494, 258, 51, "Back", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)

    return username_box, password_box, btn_login, btn_back

# --- SIGN UP SCREEN --- #
def draw_signup(signup_username, signup_password, signup_password_confirm, active_field):
    screen.fill(BACKGROUND_GRAY)
    title = font_title.render("Sign Up", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 87)))
    
    username_box = draw_input_box((width // 2 - 258 // 2), 198, 258, 51, signup_username, active_field == "signup_username", "Username")
    password_box = draw_input_box((width // 2 - 258 // 2), 280, 258, 51, signup_password, active_field == "signup_password", "Password", is_password=True)
    password_confirm_box = draw_input_box((width // 2 - 258 // 2), 362, 258, 51, signup_password_confirm, active_field == "signup_password_confirm", "Password", is_password=True)

    btn_register = draw_button((width // 2 - 258 // 2), 444, 258, 51, "Register", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_back = draw_button((width // 2 - 258 // 2), 526, 258, 51, "Back", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)

    return username_box, password_box, password_confirm_box, btn_register, btn_back

# --- WELCOME (GUEST) SCREEN --- #
def draw_welcome_guest():
    screen.fill(BACKGROUND_GRAY)
    title = font_title.render("Welcome", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 48)))
    
    subtitle = font_title.render("Guest", True, WHITE)
    screen.blit(subtitle, subtitle.get_rect(center=(width // 2, 111)))
    
    btn_play = draw_button((width // 2 - 258 // 2), 404, 258, 51, "Play", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_rarity = draw_button((width // 2 - 258 // 2), 486, 258, 51, "Rarity", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    
    return btn_play, btn_rarity

# --- WELCOME (USER) SCREEN --- #
def draw_welcome_user(username):
    screen.fill(BACKGROUND_GRAY)
    
    title = font_title.render("Welcome", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 48)))
        
    subtitle = font_title.render(username, True, WHITE)
    screen.blit(subtitle, subtitle.get_rect(center=(width // 2, 111)))
    
    
    btn_play = draw_button((width // 2 - 258 // 2), 322, 258, 51, "Play", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_inventory = draw_button((width // 2 - 258 // 2), 404, 258, 51, "Inventory", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_rarity = draw_button((width // 2 - 258 // 2), 486, 258, 51, "Rarity", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    
    return btn_play, btn_rarity, btn_inventory
        
# --- RARITY SCREEN --- #
def draw_rarity():
    screen.fill(BACKGROUND_GRAY)
    title = font_title.render("Rarity", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 81)))
    
    # RARITY 
    legendary = font_rarity.render("Legendary", True, WHITE)
    super_rare = font_rarity.render("Super Rare", True, WHITE)
    rare = font_rarity.render("Rare", True, WHITE)
    common = font_rarity.render("Common", True, WHITE)

    screen.blit(legendary, legendary.get_rect(topleft=(11, 229)))
    screen.blit(super_rare, super_rare.get_rect(topleft=(212, 229)))
    screen.blit(rare, rare.get_rect(topleft=(467, 229)))
    screen.blit(common, common.get_rect(topleft = (638, 229)))
    
    # SQUARES
    pygame.draw.rect(screen, LIGHT_GRAY, (23, 265, 139, 139), border_radius=16)
    pygame.draw.rect(screen, LIGHT_GRAY, (228, 265, 139, 139), border_radius=16)
    pygame.draw.rect(screen, LIGHT_GRAY, (433, 265, 139, 139), border_radius=16)
    pygame.draw.rect(screen, LIGHT_GRAY, (638, 265, 139, 139), border_radius=16)

    # PERCENTAGE
    legendary_percentage = font_rarity.render("2%", True, WHITE)
    super_percentage = font_rarity.render("8%", True, WHITE)
    rare_percentage = font_rarity.render("30%", True, WHITE)
    common_percentage = font_rarity.render("60%", True, WHITE)
    
    screen.blit(legendary_percentage, legendary_percentage.get_rect(center=(92, 385)))
    screen.blit(super_percentage, super_percentage.get_rect(center=(297, 385)))
    screen.blit(rare_percentage, rare_percentage.get_rect(center=(502, 385)))
    screen.blit(common_percentage, common_percentage.get_rect(center = (707, 385)))
    
    # IMAGES
    legendary_ball = pygame.image.load("assets\images\\rarity_screen\legendary gacha ball closed.png").convert_alpha()
    super_rare_ball = pygame.image.load("assets\images\\rarity_screen\super rare gacha ball closed.png").convert_alpha()
    rare_ball = pygame.image.load("assets\images\\rarity_screen\\rare gacha ball closed.png").convert_alpha()
    common_ball = pygame.image.load("assets\images\\rarity_screen\common gacha ball closed.png").convert_alpha()

    screen.blit(legendary_ball, legendary_ball.get_rect(topleft=(38, 279)))
    screen.blit(super_rare_ball, super_rare_ball.get_rect(topleft=(243, 279)))
    screen.blit(rare_ball, rare_ball.get_rect(topleft=(448, 279)))
    screen.blit(common_ball, common_ball.get_rect(topleft=(653, 279)))

    btn_back = draw_button((width // 2 - 258 // 2), 494, 258, 51, "Back", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    return btn_back

# --- GACHAPON SCREEN --- #
def draw_gachapon(last_prize):
    screen.fill(BACKGROUND_GRAY)

    # TITLE
    title = font_title.render("Gachapon", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 87)))

    if last_prize:
        prize_name = last_prize.name

        # Image
        if prize_name in prize_images:
            img = prize_images[prize_name]
            img_width, img_height = 200, 200
            img_scaled = pygame.transform.scale(img, (img_width, img_height))
            img_x = 465 + 258 // 2 - img_width // 2
            img_y = 150
            screen.blit(img_scaled, (img_x, img_y))

        display_name = prize_names_display.get(prize_name, prize_name)
        color = prize_colors.get(prize_name, WHITE)
        text = font_warning.render(f"You got a {display_name}!", True, color)
        screen.blit(text, text.get_rect(center=(465 + 258 // 2, 370)))

    else:
        legendary_desc = font_warning.render("Legendary - 200", True, WHITE)
        super_rare_desc = font_warning.render("Super rare - 150", True, WHITE)
        rare_desc = font_warning.render("Rare - 100", True, WHITE)
        commun_desc = font_warning.render("Common - 25", True, WHITE)

        screen.blit(legendary_desc, legendary_desc.get_rect(topleft=(494, 232)))
        screen.blit(super_rare_desc, super_rare_desc.get_rect(topleft=(494, 288)))
        screen.blit(rare_desc, rare_desc.get_rect(topleft=(494, 343)))
        screen.blit(commun_desc, commun_desc.get_rect(topleft=(494, 399)))

    # GACHAPON IMAGE
    gachapon_image = pygame.image.load(
        "assets/images/gachapon_screen/gachapon.png"
    ).convert_alpha()
    screen.blit(gachapon_image, (110, 210))

    # BUTTONS
    btn_roll = draw_button(
        465, 448, 258, 51,
        "Roll", font_buttons,
        WHITE, BUTTON_GRAY,
        BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY
    )
    btn_back = draw_button(
        465, 530, 258, 51,
        "Back", font_buttons,
        WHITE, BUTTON_GRAY,
        BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY
    )

    return btn_roll, btn_back


# --- INVENTORY SCREEN --- #
def draw_inventory(username, scroll_y, user_total_points, user_total_itens):
    items = inventory.load_inventory(username)

    # Prizes list
    fixed_prizes = ["duck", "dog", "bear", "robot"]
    prize_names_display = {
        "duck": "Golden Duck",
        "dog": "Lucky Dog",
        "bear": "Teddy Bear",
        "robot": "Mini Robot",
    }

    owned_counts = {p: 0 for p in fixed_prizes}
    for item in items:
        prize = item["prize"]
        if prize in owned_counts:
            owned_counts[prize] += 1

    num_slots = len(fixed_prizes)
    slot_size = 139
    spacing = 160
    padding = 10
    start_y = 0

    content_height = 632
    content_surface = pygame.Surface((600, content_height), pygame.SRCALPHA)
    content_surface.fill((0, 0, 0, 0))

    # --- DRAW ITENS --- #
    for i, prize_key in enumerate(fixed_prizes):
        y = start_y + i * spacing

        pygame.draw.rect(
            content_surface,
            LIGHT_GRAY,
            (40, y, slot_size, slot_size),
            border_radius=16
        )

        # Image
        if prize_key in prize_images:
            img = prize_images[prize_key]
            img = pygame.transform.smoothscale(
                img,
                (slot_size - padding * 2, slot_size - padding * 2)
            )

            # Change opacity
            if owned_counts[prize_key] == 0:
                img.set_alpha(80)
            else:
                img.set_alpha(255)

            content_surface.blit(img, (40 + padding, y + padding))

        name = prize_names_display.get(prize_key, prize_key.capitalize())
        qty = owned_counts[prize_key]
        color = prize_colors.get(prize_key, WHITE)

        name_text = font_warning.render(name, True, color)
        qty_text = font_warning.render(f"{qty}x", True, color)

        content_surface.blit(name_text, (210, y + 55))
        content_surface.blit(qty_text, (460, y + 55))

    screen.fill(BACKGROUND_GRAY)

    # --- TITLE --- #
    title = font_title.render("Inventory", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 81)))

    # --- POINTS & ITEMS --- #
    points = font_warning.render(f"Points: {user_total_points}", True, WHITE)
    screen.blit(points, points.get_rect(topleft=(117, 120)))

    itens_text = font_warning.render(f"Items: {user_total_itens}", True, WHITE)
    screen.blit(itens_text, itens_text.get_rect(topleft=(488, 120)))

    btn_back = draw_button((width // 2 - 258 // 2),494,258,51,"Back",font_buttons,WHITE,BUTTON_GRAY,BUTTON_SHADOW_GRAY,BUTTON_SHADOW_GRAY,)

    # --- (VIEWPORT) --- #
    view_width = 562
    view_height = 322
    view_x = (width - view_width) // 2
    view_y = 167
    view_rect = pygame.Rect(view_x, view_y, view_width, view_height)

    # --- CLIPPING ---
    screen.set_clip(view_rect)
    screen.blit(content_surface, (view_x, view_y - scroll_y))
    screen.set_clip(None)

    # --- BARRA DE SCROLL FIXA NA ESQUERDA ---
    bar_x = 12
    bar_y = 15
    bar_width = 22
    bar_height = height - 30
    pygame.draw.rect(screen, (121, 121, 121), (bar_x, bar_y, bar_width, bar_height), border_radius=16)

    # Handle da barra
    scroll_bar_height = max(view_height * (bar_height / content_height), 50)
    scroll_bar_y = (scroll_y / (content_height - view_height)) * (bar_height - scroll_bar_height) + bar_y

    handle_width = 18
    handle_x = bar_x + (bar_width - handle_width) // 2
    pygame.draw.rect(screen, WHITE, (handle_x, scroll_bar_y, handle_width, scroll_bar_height), border_radius=16)

    return btn_back, content_height, view_height
    
    # --- PRIZE (GUEST) --- #
def draw_prize_guest():
    screen.fill(BACKGROUND_GRAY)
    
    # TITLE
    title = font_title.render("Gachapon", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 87)))
    
    # CONGRATULATIONS
    congrats = font_warning.render("Congratulations!!!", True, WHITE)
    screen.blit(congrats, congrats.get_rect(topleft=(465, 181)))

    # PRIZE
    prize = font_warning.render("Golden duck", True, YELLOW)
    screen.blit(prize, congrats.get_rect(topleft=(495, 386)))
    
    # GACHAPON IMAGE
    gachapon_image = pygame.image.load("assets\images\gachapon_screen\gachapon.png").convert_alpha()
    screen.blit(gachapon_image, gachapon_image.get_rect(topleft=(110, 210)))

    # BUTTON
    btn_roll = draw_button(465, 448, 258, 51, "Roll", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_back = draw_button(465, 530, 258, 51, "Back", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    return btn_roll, btn_back

# --- PRIZE (USER) --- #
def draw_prize_user(mouse_pos=None, mouse_click=False):
    global last_prize
    screen.fill(BACKGROUND_GRAY)

    # TITLE
    title = font_title.render("Gachapon", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 50)))

    # BOTÕES
    btn_roll = draw_button(465, 500, 258, 51, "Roll", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_inventory = draw_button(465, 580, 258, 51, "Inventory", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)

    if mouse_click and btn_roll.collidepoint(mouse_pos):
        last_prize = gacha.roll()

    if last_prize:
        img = prize_images.get(last_prize.name)
        if img:
            img_width, img_height = 200, 200
            img_scaled = pygame.transform.scale(img, (img_width, img_height))
            img_x = 465 + 258 // 2 - img_width // 2
            img_y = 150
            screen.blit(img_scaled, (img_x, img_y))

        display_name = prize_names_display.get(last_prize.name, last_prize.name)
        color = prize_colors.get(last_prize.name, WHITE)
        text = font_warning.render(f"You got a {display_name}!", True, color)
        screen.blit(text, text.get_rect(center=(465 + 258 // 2, 370)))

    return btn_inventory, btn_roll


# INITIALIZE BUTTONS
btn_guest = btn_login = btn_signup = pygame.Rect(0, 0, 0, 0)
btn_continue = btn_back = btn_signup_guest = pygame.Rect(0, 0, 0, 0)
username_box = password_box = rptpassword_box = btn_register = pygame.Rect(0, 0, 0, 0)
login_username_box = login_password_box = btn_login_submit = pygame.Rect(0, 0, 0, 0)
btn_play = btn_rarity = pygame.Rect(0,0,0,0)

# --- VOID LOOP --- #
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            # --- MENU --- #
            if current_screen == "menu":
                if btn_guest.collidepoint(mouse_pos):
                    current_screen = "guest"
                elif btn_login.collidepoint(mouse_pos):
                    current_screen = "login"
                    active_field = None
                elif btn_signup.collidepoint(mouse_pos):
                    current_screen = "signup"
                    active_field = None

            # --- GUEST --- #
            elif current_screen == "guest":
                if btn_continue.collidepoint(mouse_pos):
                    current_user = ""
                    current_screen = "welcome_guest"
                elif btn_signup_guest.collidepoint(mouse_pos):
                    current_screen = "signup"
                    active_field = None
                elif btn_back.collidepoint(mouse_pos):
                    current_screen = "menu"
                    
            # --- SIGN UP --- #
            elif current_screen == "signup":
                if signup_username_box.collidepoint(mouse_pos):
                    active_field = "signup_username"
                elif signup_password_box.collidepoint(mouse_pos):
                    active_field = "signup_password"
                elif signup_password_confirm_box.collidepoint(mouse_pos):
                    active_field = "signup_password_confirm"
                elif btn_back.collidepoint(mouse_pos):
                    current_screen = "menu"
                    active_field = None
                    username_text = ""
                    password_text = ""
                    rptpassword_text = ""
                elif btn_register.collidepoint(mouse_pos):
                    if password_text == rptpassword_text and password_text != "":
                        success = user.save_user(username_text, password_text)
                        if success:
                            print(f" USER CREATED: {username_text}")
                            current_user = username_text
                            current_screen = "welcome_user"

                        else:
                            print(" USER ALREADY EXIST!")
                        username_text = ""
                        password_text = ""
                        rptpassword_text = ""
                        active_field = None
                    else:
                        print(" PASSWORD WRONG!")
                else:
                    active_field = None

            # --- LOGIN --- #
            elif current_screen == "login":
                if login_username_box.collidepoint(mouse_pos):
                    active_field = "login_username"
                elif login_password_box.collidepoint(mouse_pos):
                    active_field = "login_password"
                elif btn_back.collidepoint(mouse_pos):
                    current_screen = "menu"
                    active_field = None
                    login_username = ""
                    login_password = ""
                elif btn_login_submit.collidepoint(mouse_pos):
                    if user.check_login(login_username, login_password):
                        current_user = login_username
                        print(f" LOGIN: {current_user}")
                        user_total_points = inventory.total_points(current_user)
                        user_total_itens = inventory.total_items(current_user)
                        current_screen = "welcome_user"
                    else:
                        print(" USER OR PASSWORD INCORRECT.")
                    login_username = ""
                    login_password = ""
                    active_field = None
                else:
                    active_field = None
                    
            # --- WELCOME (GUEST) --- #   
            elif current_screen == "welcome_guest":
                if btn_play.collidepoint(mouse_pos):
                    current_screen = "gachapon"
                elif btn_rarity.collidepoint(mouse_pos):
                    current_screen = "rarity"
                    
            #--- WELCOME (USER) --- #     
            elif current_screen == "welcome_user":
                if btn_play.collidepoint(mouse_pos):
                    current_screen = "gachapon"
                elif btn_rarity.collidepoint(mouse_pos):
                    current_screen = "rarity"
                elif btn_inventory.collidepoint(mouse_pos):
                    current_screen = "inventory"
                    
            # --- RARITY --- #
            elif current_screen == "rarity":
                if btn_back.collidepoint(mouse_pos) and current_user!="":
                    current_screen = "welcome_user"
                elif btn_back.collidepoint(mouse_pos) and current_user=="":
                    current_screen = "welcome_guest"

            # --- GACHAPON --- #
            elif current_screen == "gachapon":
                if btn_roll.collidepoint(mouse_pos):
                    if current_user != "":
                        last_prize = gacha.roll()
                        inventory.add_item(current_user, last_prize)
                        user_total_points = inventory.total_points(current_user)
                        user_total_itens = inventory.total_items(current_user)

                        print(
                            f"EARNED {last_prize.points} POINTS | "
                            f"NEW ITEM {last_prize.name} TO {current_user}"
                        )                                            

                    else:
                        last_prize = gacha.roll()
                        print(
                            f"EARNED {last_prize.points} POINTS | "
                            f"NO ACCOUNT (NOT SAVED)"
                        )

                elif btn_back.collidepoint(mouse_pos):
                    last_prize = None
                    current_screen = (
                        "welcome_user" if current_user != "" else "welcome_guest"
                    )
                    
            # --- PRIZE USER --- #
            elif current_screen == "prize_user":
                if btn_inventory.collidepoint(mouse_pos):
                    current_screen = "inventory"
                elif btn_roll.collidepoint(mouse_pos):
                    print(f"EARNED X POINTS | NEW ITEM TO THE INVENTORY OF {current_user}")

            # --- PRIZE GUEST --- #
            elif current_screen == "prize_guest":
                if btn_roll.collidepoint(mouse_pos):
                    print("EARNED X POINTS | NO ACCOUNT")   
                elif btn_back.collidepoint(mouse_pos):
                    current_screen = "gachapon"

            # --- INVENTORY --- #
            elif current_screen == "inventory":
                if btn_back.collidepoint(mouse_pos):
                    current_screen = "welcome_user"
                    
        # CAPTURE THE KEYBOARD 
        if event.type == pygame.KEYDOWN and active_field:
            if event.key == pygame.K_BACKSPACE:
                if active_field == "signup_username":
                    username_text = username_text[:-1]
                elif active_field == "signup_password":
                    password_text = password_text[:-1]
                elif active_field == "signup_password_confirm":
                    rptpassword_text = rptpassword_text[:-1]
                elif active_field == "login_username":
                    login_username = login_username[:-1]
                elif active_field == "login_password":
                    login_password = login_password[:-1]
            elif event.key == pygame.K_RETURN:
                if current_screen == "signup" and password_text == rptpassword_text:
                    print(f"USER REGISTERED: {username_text}")
                elif current_screen == "login":
                    print(f"LOGIN: {login_username}")
            else:
                char = event.unicode
                if active_field == "signup_username" and len(username_text) < 20:
                    username_text += char
                elif active_field == "signup_password" and len(password_text) < 20:
                    password_text += char
                elif active_field == "signup_password_confirm" and len(rptpassword_text) < 20:
                    rptpassword_text += char
                elif active_field == "login_username" and len(login_username) < 20:
                    login_username += char
                elif active_field == "login_password" and len(login_password) < 20:
                    login_password += char
            
            # THE SCROLL
        elif event.type == pygame.MOUSEWHEEL and current_screen == "inventory":
            scroll_y -= event.y * scroll_speed
            scroll_y = max(0, min(scroll_y, content_height - view_height))
            
    # --- RENDERIZATION --- #
    match current_screen:
        case "menu":
            btn_guest, btn_login, btn_signup = draw_menu()
        case "guest":
            tn_continue, btn_signup_guest, btn_back = draw_guest()
        case "login":
            login_username_box, login_password_box, btn_login_submit, btn_back = draw_login(login_username, login_password, active_field)
        case "signup":
            signup_username_box, signup_password_box, signup_password_confirm_box, btn_register, btn_back = draw_signup(username_text, password_text, rptpassword_text, active_field)
        case "welcome_guest":
            btn_play, btn_rarity = draw_welcome_guest()
        case "welcome_user":
            btn_play, btn_rarity, btn_inventory = draw_welcome_user(current_user)
        case "rarity":
            btn_back = draw_rarity()
        case "gachapon":
            btn_roll, btn_back = draw_gachapon(last_prize)
        case "inventory":
            btn_back, content_height, view_height = draw_inventory(current_user, scroll_y, user_total_points, user_total_itens)
        case "prize_guest":
            btn_back, btn_roll = draw_prize_guest()
        case "prize_user":
            btn_inventory, btn_roll = draw_prize_user()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()