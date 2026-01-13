import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da janela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Claw Machine Game")

# Cores
WHITE = (255, 255, 255)
ORANGE = (255, 136, 72)
LIGHT_GRAY = (217, 217, 217)
DARK_GRAY = (194, 192, 192)
ACTIVE_COLOR = (240, 240, 240)

# Relógio
clock = pygame.time.Clock()
running = True

# Variáveis de texto
username_text = ""
password_text = ""
rptpassword_text = ""
login_username = ""
login_password = ""
active_field = None

# Tela atual
current_screen = "menu"

# Fontes
try:
    fonte_title = pygame.font.Font("assets/fonts/KronaOne-Regular.ttf", 48)
    font_buttons = pygame.font.Font("assets/fonts/KronaOne-Regular.ttf", 24)
    font_warning = pygame.font.Font("assets/fonts/KronaOne-Regular.ttf", 16)
except:
    fonte_title = pygame.font.SysFont(None, 60)
    font_buttons = pygame.font.SysFont(None, 24)
    font_warning = pygame.font.SysFont(None, 20)

# --- button draw function --- #
def draw_button(x, y, w, h, text, font, text_color, button_color, shadow_color):
    pygame.draw.rect(screen, shadow_color, (x, y + 10, w, h), border_radius=16)
    pygame.draw.rect(screen, button_color, (x, y, w, h), border_radius=16)
    txt = font.render(text, True, text_color)
    txt_rect = txt.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(txt, txt_rect)
    return pygame.Rect(x, y, w, h)

# --- Input field draw function --- #
def draw_input_box(x, y, w, h, text, active, placeholder="", is_password=False):
    color = ACTIVE_COLOR if active else LIGHT_GRAY
    shadow_color = DARK_GRAY

    pygame.draw.rect(screen, shadow_color, (x, y + 10, w, h), border_radius=16)
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=16)

    if text == "" and not active:
        display_text = placeholder
        txt_color = (150, 150, 150)
    else:
        display_text = "*" * len(text) if is_password and text else text
        txt_color = ORANGE

    txt = font_buttons.render(display_text, True, txt_color)
    txt_rect = txt.get_rect(midleft=(x + 15, y + h // 2))
    screen.blit(txt, txt_rect)
    return pygame.Rect(x, y, w, h)

# --- MENU ---
def draw_menu():
    screen.fill(ORANGE)
    title = fonte_title.render("Claw Machine", True, WHITE)
    rect_title = title.get_rect(center=(width // 2, 144))
    screen.blit(title, rect_title)

    btn_guest = draw_button(260, 274, 279, 76, "Guest", font_buttons, ORANGE, LIGHT_GRAY, DARK_GRAY)
    btn_login = draw_button(260, 374, 279, 76, "Login", font_buttons, ORANGE, LIGHT_GRAY, DARK_GRAY)
    btn_signup = draw_button(260, 474, 279, 76, "Sign Up", font_buttons, ORANGE, LIGHT_GRAY, DARK_GRAY)

    return btn_guest, btn_login, btn_signup

# --- GUEST ---
def draw_guest():
    screen.fill(ORANGE)
    guest_title = fonte_title.render("Guest", True, WHITE)
    rect_guest = guest_title.get_rect(center=(width // 2, 144))
    screen.blit(guest_title, rect_guest)

    warning = font_warning.render("IF YOU CONTINUE WITHOUT LOGIN", True, WHITE)
    warning2 = font_warning.render("YOU CAN'T REGISTER YOUR POINTS", True, WHITE)
    screen.blit(warning, warning.get_rect(center=(width // 2, 210)))
    screen.blit(warning2, warning2.get_rect(center=(width // 2, 235)))

    btn_signup_guest = draw_button(260, 320, 279, 76, "Sign Up", font_buttons, ORANGE, LIGHT_GRAY, DARK_GRAY)
    btn_continue = draw_button(260, 420, 279, 76, "Continue", font_buttons, ORANGE, LIGHT_GRAY, DARK_GRAY)
    btn_back = draw_button(260, 520, 279, 50, "Back", font_buttons, ORANGE, LIGHT_GRAY, DARK_GRAY)

    return btn_continue, btn_signup_guest, btn_back

# --- Sign up ---
def draw_signup(username_text, password_text, rptpassword_text, active_field):
    screen.fill(ORANGE)
    title = fonte_title.render("Sign Up", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 100)))

    username_box = draw_input_box(260, 200, 279, 60, username_text, active_field == "username", "Username")
    password_box = draw_input_box(260, 280, 279, 60, password_text, active_field == "password", "Password", is_password=True)
    rptpassword_box = draw_input_box(260, 360, 279, 60, rptpassword_text, active_field == "rptpassword", "Password Again", is_password=True)

    btn_register = draw_button(260, 450, 279, 70, "Register", font_buttons, ORANGE, LIGHT_GRAY, DARK_GRAY)
    btn_back = draw_button(260, 535, 279, 50, "Back", font_buttons, ORANGE, LIGHT_GRAY, DARK_GRAY)
    
    return username_box, password_box, rptpassword_box, btn_register, btn_back

# --- Login ---
def draw_login(login_username, login_password, active_field):
    screen.fill(ORANGE)
    title = fonte_title.render("Login", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 100)))

    username_box = draw_input_box(260, 240, 279, 60, login_username, active_field == "login_username", "Username")
    password_box = draw_input_box(260, 320, 279, 60, login_password, active_field == "login_password", "Password", is_password=True)

    btn_login = draw_button(260, 420, 279, 70, "Login", font_buttons, ORANGE, LIGHT_GRAY, DARK_GRAY)
    btn_back = draw_button(260, 510, 279, 50, "Back", font_buttons, ORANGE, LIGHT_GRAY, DARK_GRAY)

    return username_box, password_box, btn_login, btn_back

# Inicializar variáveis de botões
btn_guest = btn_login = btn_signup = pygame.Rect(0, 0, 0, 0)
btn_continue = btn_back = btn_signup_guest = pygame.Rect(0, 0, 0, 0)
username_box = password_box = rptpassword_box = btn_register = pygame.Rect(0, 0, 0, 0)
login_username_box = login_password_box = btn_login_submit = pygame.Rect(0, 0, 0, 0)

# --- LOOP PRINCIPAL ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            # --- Clique no MENU ---
            if current_screen == "menu":
                if btn_guest.collidepoint(mouse_pos):
                    current_screen = "guest"
                elif btn_login.collidepoint(mouse_pos):
                    current_screen = "login"
                    active_field = None
                elif btn_signup.collidepoint(mouse_pos):
                    current_screen = "signup"
                    active_field = None

            # --- Clique no GUEST ---
            elif current_screen == "guest":
                if btn_continue.collidepoint(mouse_pos):
                    print("Continuar sem login")
                elif btn_signup_guest.collidepoint(mouse_pos):
                    current_screen = "signup"
                    active_field = None
                elif btn_back.collidepoint(mouse_pos):
                    current_screen = "menu"
                    
            # --- SIGN UP ---
            elif current_screen == "signup":
                if username_box.collidepoint(mouse_pos):
                    active_field = "username"
                elif password_box.collidepoint(mouse_pos):
                    active_field = "password"
                elif rptpassword_box.collidepoint(mouse_pos):
                    active_field = "rptpassword"
                elif btn_back.collidepoint(mouse_pos):
                    current_screen = "menu"
                    active_field = None
                    username_text = ""
                    password_text = ""
                    rptpassword_text = ""
                elif btn_register.collidepoint(mouse_pos):
                    if password_text == rptpassword_text and password_text != "":
                        print(f"Usuário registrado: {username_text}")
                        current_screen = "menu"
                        username_text = ""
                        password_text = ""
                        rptpassword_text = ""
                        active_field = None
                    else:
                        print("Senhas não coincidem!")
                else:
                    active_field = None

            # --- LOGIN ---
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
                    print(f"Login: {login_username}")
                    current_screen = "menu"
                    login_username = ""
                    login_password = ""
                    active_field = None
                else:
                    active_field = None

        # Captura digitação
        if event.type == pygame.KEYDOWN and active_field:
            if event.key == pygame.K_BACKSPACE:
                if active_field == "username":
                    username_text = username_text[:-1]
                elif active_field == "password":
                    password_text = password_text[:-1]
                elif active_field == "rptpassword":
                    rptpassword_text = rptpassword_text[:-1]
                elif active_field == "login_username":
                    login_username = login_username[:-1]
                elif active_field == "login_password":
                    login_password = login_password[:-1]
            elif event.key == pygame.K_RETURN:
                if current_screen == "signup" and password_text == rptpassword_text:
                    print(f"Usuário registrado: {username_text}")
                elif current_screen == "login":
                    print(f"Login: {login_username}")
            else:
                char = event.unicode
                if active_field == "username" and len(username_text) < 20:
                    username_text += char
                elif active_field == "password" and len(password_text) < 20:
                    password_text += char
                elif active_field == "rptpassword" and len(rptpassword_text) < 20:
                    rptpassword_text += char
                elif active_field == "login_username" and len(login_username) < 20:
                    login_username += char
                elif active_field == "login_password" and len(login_password) < 20:
                    login_password += char

    # --- Renderização ---
    if current_screen == "menu":
        btn_guest, btn_login, btn_signup = draw_menu()
    elif current_screen == "guest":
        btn_continue, btn_signup_guest, btn_back = draw_guest()
    elif current_screen == "login":
        login_username_box, login_password_box, btn_login_submit, btn_back = draw_login(login_username, login_password, active_field)
    elif current_screen == "signup":
        username_box, password_box, rptpassword_box, btn_register, btn_back = draw_signup(username_text, password_text, rptpassword_text, active_field)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()