import pygame
import sys
import csv
import os

# Initialize Pygame
pygame.init()

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

# Clock
clock = pygame.time.Clock()
running = True

# Variables
username_text = ""
password_text = ""
rptpassword_text = ""
login_username = ""
login_password = ""
active_field = None
scroll_y = 0
scroll_speed = 40

# Current Screen
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

    btn_guest = draw_button((width // 2 - 258 // 2), 240, 258, 64, "Guest", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_login = draw_button((width // 2 - 258 // 2), 322, 258, 64, "Login", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_signup = draw_button((width // 2 - 258 // 2), 404, 258, 64, "Sign Up", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)

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
    
    btn_continue = draw_button((width // 2 - 258 // 2), 322, 258, 64, "Continue", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_signup = draw_button((width // 2 - 258 // 2), 404, 258, 64, "Sign Up", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_back = draw_button((width // 2 - 258 // 2), 486, 258, 64, "Back", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    return btn_continue, btn_signup, btn_back

# --- LOGIN SCREEN --- #
def draw_login(login_username, login_password, active_field):
    screen.fill(BACKGROUND_GRAY)
    title = font_title.render("Login", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 87)))

    username_box = draw_input_box((width // 2 - 258 // 2), 248, 258, 64, login_username, active_field == "login_username", "Username")
    password_box = draw_input_box((width // 2 - 258 // 2), 330, 258, 64, login_password, active_field == "login_password", "Password", is_password=True)

    btn_login = draw_button((width // 2 - 258 // 2), 412, 258, 64, "Continue", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_back = draw_button((width // 2 - 258 // 2), 494, 258, 64, "Back", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)

    return username_box, password_box, btn_login, btn_back
  
# --- SIGN UP SCREEN --- #
def draw_signup(signup_username, signup_password, signup_password_confirm, active_field):
    screen.fill(BACKGROUND_GRAY)
    title = font_title.render("Sign Up", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 87)))
    
    username_box = draw_input_box((width // 2 - 258 // 2), 198, 258, 64, signup_username, active_field == "signup_username", "Username")
    password_box = draw_input_box((width // 2 - 258 // 2), 280, 258, 64, signup_password, active_field == "signup_password", "Password", is_password=True)
    password_confirm_box = draw_input_box((width // 2 - 258 // 2), 362, 258, 64, signup_password_confirm, active_field == "signup_password_confirm", "Password", is_password=True)

    btn_register = draw_button((width // 2 - 258 // 2), 444, 258, 64, "Register", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_back = draw_button((width // 2 - 258 // 2), 526, 258, 64, "Back", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)

    return username_box, password_box, password_confirm_box, btn_register, btn_back

# --- WELCOME (GUEST) SCREEN --- #
def draw_welcome_guest():
    screen.fill(BACKGROUND_GRAY)
    title = font_title.render("Welcome", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 48)))
    
    subtitle = font_title.render("Guest", True, WHITE)
    screen.blit(subtitle, subtitle.get_rect(center=(width // 2, 111)))
    
    btn_play = draw_button((width // 2 - 258 // 2), 404, 258, 64, "Play", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_rarity = draw_button((width // 2 - 258 // 2), 486, 258, 64, "Rarity", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    
    return btn_play, btn_rarity

# --- WELCOME (USER) SCREEN --- #
def draw_welcome_user(username):
    screen.fill(BACKGROUND_GRAY)
    
    title = font_title.render("Welcome", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 48)))
        
    subtitle = font_title.render(username, True, WHITE)
    screen.blit(subtitle, subtitle.get_rect(center=(width // 2, 111)))
    
    
    btn_play = draw_button((width // 2 - 258 // 2), 322, 258, 64, "Play", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_inventory = draw_button((width // 2 - 258 // 2), 404, 258, 64, "Inventory", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_rarity = draw_button((width // 2 - 258 // 2), 486, 258, 64, "Rarity", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    
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
    legendary_percentage = font_rarity.render("01%", True, WHITE)
    super_percentage = font_rarity.render("10%", True, WHITE)
    rare_percentage = font_rarity.render("30%", True, WHITE)
    common_percentage = font_rarity.render("70%", True, WHITE)
    
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

    btn_back = draw_button((width // 2 - 258 // 2), 494, 258, 64, "Back", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    return btn_back

# --- GACHAPON SCREEN --- #
def draw_gachapon():
    screen.fill(BACKGROUND_GRAY)
    
    # TITLE
    title = font_title.render("Gachapon", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 87)))
    
    # DESCRIPTIONS
    legendary_desc = font_warning.render("Legendary - 200", True, WHITE)
    super_rare_desc = font_warning.render("Super rare - 150", True, WHITE)
    rare_desc = font_warning.render("Rare - 100", True, WHITE)
    commun_desc = font_warning.render("Commun - 25", True, WHITE)
    
    screen.blit(legendary_desc, legendary_desc.get_rect(topleft=(494, 232)))
    screen.blit(super_rare_desc, super_rare_desc.get_rect(topleft=(494, 288)))
    screen.blit(rare_desc, rare_desc.get_rect(topleft=(494, 343)))
    screen.blit(commun_desc, commun_desc.get_rect(topleft=(494, 399)))

    # GACHABALLS IMAGES
    legendary_ball = pygame.image.load("assets\images\gachapon_screen\legendary gacha ball closed.png").convert_alpha()
    super_rare_ball = pygame.image.load("assets\images\gachapon_screen\super rare gacha ball closed.png").convert_alpha()
    rare_ball = pygame.image.load("assets\images\gachapon_screen\\rare gacha ball closed.png").convert_alpha()
    common_ball = pygame.image.load("assets\images\gachapon_screen\commun gacha ball closed.png").convert_alpha()
    
    screen.blit(legendary_ball, legendary_ball.get_rect(topleft=(407, 213)))
    screen.blit(super_rare_ball, super_rare_ball.get_rect(topleft=(407, 269)))
    screen.blit(rare_ball, rare_ball.get_rect(topleft=(407, 324)))
    screen.blit(common_ball, common_ball.get_rect(topleft=(407, 380)))
    
    # GACHAPON IMAGE
    gachapon_image = pygame.image.load("assets\images\gachapon_screen\gachapon.png").convert_alpha()
    screen.blit(gachapon_image, gachapon_image.get_rect(topleft=(110, 210)))

    # BUTTON
    btn_roll = draw_button(465, 448, 258, 64, "Roll", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_back = draw_button(465, 530, 258, 64, "Back", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    return btn_roll, btn_back

# --- INVENTORY SCREEN --- #
def draw_inventory(username, scroll_y):
    content_height = 1600
    content_surface = pygame.Surface((600, content_height), pygame.SRCALPHA)
    content_surface.fill((0, 0, 0, 0))

    # --- DESENHAR CONTEÚDO DO INVENTÁRIO ---
    start_y = 0
    for i in range(10):
        y = start_y + i * 160
        pygame.draw.rect(content_surface, LIGHT_GRAY, (40, y, 139, 139), border_radius=16)

    # --- FUNDO GERAL ---
    screen.fill(BACKGROUND_GRAY)

    # --- TÍTULO FIXO ---
    title = font_title.render("Inventory", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 81)))

    # --- BOTÃO VOLTAR (fixo) ---
    btn_back = draw_button(
        (width // 2 - 258 // 2),
        494,
        258,
        64,
        "Back",
        font_buttons,
        WHITE,
        BUTTON_GRAY,
        BUTTON_SHADOW_GRAY,
        BUTTON_SHADOW_GRAY,
    )

    # --- ÁREA CENTRAL VISÍVEL (VIEWPORT) ---
    view_width = 562
    view_height = 322
    view_x = (width - view_width) // 2
    view_y = 167
    view_rect = pygame.Rect(view_x, view_y, view_width, view_height)

    # --- CLIPPING (limita o desenho do conteúdo à área central) ---
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

    return btn_back, content_height, view_height  # <- retornamos view_height também

# --- REGISTER USER FUNCTION --- #
def save_user_to_csv(username, password, filepath="data\\users.csv"):
    # VERIFY IF THE FILE EXIST 
    file_exists = os.path.exists(filepath)

    # CHECK DOUBLES
    if file_exists:
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    return False  # USER ALREADY EXIST

    # NEW USER
    with open(filepath, "a", newline="", encoding="utf-8") as file:
        fieldnames = ["username", "password"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({"username": username, "password": password})
    return True


# --- CHECK LOGIN FUNCTION --- #
def check_login(username, password, filepath="data\\users.csv"):
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username and row["password"] == password:
                return True
    return False

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
                        success = save_user_to_csv(username_text, password_text)
                        if success:
                            print(f"✅ USER CREATED: {username_text}")
                            current_user = username_text
                            current_screen = "welcome_user"
                        else:
                            print("⚠️ USER ALREADY EXIST!")
                        username_text = ""
                        password_text = ""
                        rptpassword_text = ""
                        active_field = None
                    else:
                        print("❌ PASSWORD WRONG!")
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
                    if check_login(login_username, login_password):
                        current_user = login_username
                        print(f"✅ LOGIN: {current_user}")
                        current_screen = "welcome_user"
                    else:
                        print("❌ USER OR PASSWORD INCORRECT.")
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
                elif btn_back.collidepoint(mouse_pos) and current_screen=="":
                    current_screen = "welcome_guest"

            # --- GACHAPON --- #
            elif current_screen == "gachapon":
                if btn_roll.collidepoint(mouse_pos) and current_user!="":
                    print(f"EARNED X POINTS | NEW ITEM TO THE INVENTORY OF {current_user}")
                elif btn_roll.collidepoint(mouse_pos) and current_user == "":
                    print("EARNED X POINTS | NO ACCOUNT")
                elif btn_back.collidepoint(mouse_pos) and current_user!="":
                    current_screen =  "welcome_user"
                elif btn_back.collidepoint(mouse_pos) and current_user == "":
                    current_screen =  "welcome_guest"

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
    if current_screen == "menu":
        btn_guest, btn_login, btn_signup = draw_menu()
    elif current_screen == "guest":
        btn_continue, btn_signup_guest, btn_back = draw_guest()
    elif current_screen == "login":
        login_username_box, login_password_box, btn_login_submit, btn_back = draw_login(login_username, login_password, active_field)
    elif current_screen == "signup":
        signup_username_box, signup_password_box, signup_password_confirm_box, btn_register, btn_back = draw_signup(username_text, password_text, rptpassword_text, active_field)
    elif current_screen == "welcome_guest":
        btn_play, btn_rarity = draw_welcome_guest()
    elif current_screen == "welcome_user":
        btn_play, btn_rarity, btn_inventory = draw_welcome_user(current_user)
    elif current_screen == "rarity":
        btn_back = draw_rarity()
    elif current_screen == "gachapon":
        btn_roll, btn_back = draw_gachapon()
    elif current_screen == "inventory":
        btn_roll, content_height, view_height = draw_inventory(current_user, scroll_y)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()