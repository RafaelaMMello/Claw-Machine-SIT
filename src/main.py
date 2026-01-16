import pygame
import sys
import csv
import os

# Inicializa o Pygame
pygame.init()

# Configurações da janela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gachapon Game")

# Cores
ACTIVE_COLOR = (240, 240, 240)
WHITE = (255, 255, 255)
BACKGROUND_GRAY =(186, 186, 186)
BUTTON_GRAY = (198, 198, 198)
BUTTON_SHADOW_GRAY = (147, 147, 147)

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
    font_title = pygame.font.Font("assets/fonts/KronaOne-Regular.ttf", 64)
    font_buttons = pygame.font.Font("assets/fonts/KronaOne-Regular.ttf", 36 )
    font_warning = pygame.font.Font("assets/fonts/KronaOne-Regular.ttf", 24)
except:
    font_title = pygame.font.SysFont(None, 60)
    font_buttons = pygame.font.SysFont(None, 24)
    font_warning = pygame.font.SysFont(None, 20)

# --- button draw function --- #
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

# --- Input field draw function --- #
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

# --- MENU ---
def draw_menu():
    screen.fill(BACKGROUND_GRAY)
    title = font_title.render("Gachapon Game", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 87)))

    btn_guest = draw_button((width // 2 - 258 // 2), 240, 258, 64, "Guest", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_login = draw_button((width // 2 - 258 // 2), 322, 258, 64, "Login", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_signup = draw_button((width // 2 - 258 // 2), 404, 258, 64, "Sign Up", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)

    return btn_guest, btn_login, btn_signup

# --- GUEST ---
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

# --- LOGIN ---
def draw_login(login_username, login_password, active_field):
    screen.fill(BACKGROUND_GRAY)
    title = font_title.render("Login", True, WHITE)
    screen.blit(title, title.get_rect(center=(width // 2, 87)))

    username_box = draw_input_box((width // 2 - 258 // 2), 248, 258, 64, login_username, active_field == "login_username", "Username")
    password_box = draw_input_box((width // 2 - 258 // 2), 330, 258, 64, login_password, active_field == "login_password", "Password", is_password=True)

    btn_login = draw_button((width // 2 - 258 // 2), 412, 258, 64, "Continue", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)
    btn_back = draw_button((width // 2 - 258 // 2), 494, 258, 64, "Back", font_buttons, WHITE, BUTTON_GRAY, BUTTON_SHADOW_GRAY, BUTTON_SHADOW_GRAY)

    return username_box, password_box, btn_login, btn_back
  
# --- SIGN UP ---
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

# --- register user
def save_user_to_csv(username, password, filepath="data\\users.csv"):
    # Se o arquivo não existir, cria com cabeçalho
    file_exists = os.path.exists(filepath)

    # Garante que não há duplicatas
    if file_exists:
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    return False  # usuário já existe

    # Escreve o novo usuário
    with open(filepath, "a", newline="", encoding="utf-8") as file:
        fieldnames = ["username", "password"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({"username": username, "password": password})
    return True


# --- check login
def check_login(username, password, filepath="data\\users.csv"):
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username and row["password"] == password:
                return True
    return False

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
                            print(f"✅ Usuário registrado: {username_text}")
                            current_screen = "menu"
                        else:
                            print("⚠️ Usuário já existe!")
                        username_text = ""
                        password_text = ""
                        rptpassword_text = ""
                        active_field = None
                    else:
                        print("❌ Senhas não coincidem!")
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
                    if check_login(login_username, login_password):
                        print(f"✅ Login bem-sucedido: {login_username}")
                        current_screen = "menu"
                    else:
                        print("❌ Usuário ou senha incorretos.")
                    login_username = ""
                    login_password = ""
                    active_field = None
                else:
                    active_field = None

        # Captura digitação
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
                    print(f"Usuário registrado: {username_text}")
                elif current_screen == "login":
                    print(f"Login: {login_username}")
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


    # --- Renderização ---
    if current_screen == "menu":
        btn_guest, btn_login, btn_signup = draw_menu()
    elif current_screen == "guest":
        btn_continue, btn_signup, btn_back = draw_guest()
    elif current_screen == "login":
        login_username_box, login_password_box, btn_login_submit, btn_back = draw_login(login_username, login_password, active_field)
    elif current_screen == "signup":
        signup_username_box, signup_password_box, signup_password_confirm_box, btn_register, btn_back = draw_signup(username_text, password_text, rptpassword_text, active_field)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()