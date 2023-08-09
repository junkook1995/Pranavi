import tkinter as tk
from tkinter import messagebox
import pygame
from pygame import mixer

BALL_RADIUS = 15
BALL_SPEED = 3
GRAVITY = 0.5
score = 0
TIME_LIMIT_EASY = 60
TIME_LIMIT_MEDIUM = 30
TIME_LIMIT_HARD = 10

timer_text = None
is_game_running = False
remaining_time = 0

pygame.mixer.init()
wrong_sound = pygame.mixer.Sound(r"C:\Users\admin\Downloads\243700__ertfelda__incorrect.wav")
correct_sound = pygame.mixer.Sound(r"C:\Users\admin\Downloads\421002__eponn__correct.wav")
game_over_sound = pygame.mixer.Sound(r"C:\Users\admin\Downloads\144033188-deep-male-voice-god-character-_1_.wav")
start_sound = pygame.mixer.Sound(r"C:\Users\admin\Downloads\433644__dersuperanton__game-over-sound.wav")
def play_sound():
        pygame.mixer.music.load(r"C:\Users\admin\Downloads\641014__igorchagas__enigmatic-polyphony.wav")
        pygame.mixer.music.play()
def stop_sound():
        pygame.mixer.music.stop()



canvas = None
score_label_game = None
back_button_game = None
difficulty_selected = False
difficulty_frame = None

game_over = False

def draw_ball(x, y):
    canvas.delete("ball")
    canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill='yellow', tags="ball")

def move_ball(target_x, target_y, triangle_vertices):
    ball_x = 50
    ball_y = 50
    ball_velocity = 0
    while ball_x < target_x:
        if not difficulty_selected:
            return
        ball_x += BALL_SPEED
        draw_ball(ball_x, ball_y)
        canvas.update()
        canvas.after(50)
    while ball_y < target_y:
        if not difficulty_selected:
            return
        ball_y += ball_velocity
        ball_velocity += GRAVITY
        draw_ball(ball_x, ball_y)
        canvas.update()

    result = is_inside_triangle(target_x, target_y, triangle_vertices)
    if result:
        update_score(100)
        correct_sound.play()
    else:
        update_score(-50)
        wrong_sound.play()

def is_inside_triangle(x, y, triangle_vertices):
    x1, y1 = triangle_vertices[0]
    x2, y2 = triangle_vertices[1]
    x3, y3 = triangle_vertices[2]
    AB_equation = ((x2 - x1) * (y - y1)) - ((y2 - y1) * (x - x1))
    BC_equation = ((x3 - x2) * (y - y2)) - ((y3 - y2) * (x - x2))
    CA_equation = ((x1 - x3) * (y - y3)) - ((y1 - y3) * (x - x3))
    if (AB_equation > 0 and BC_equation > 0 and CA_equation > 0) or (AB_equation < 0 and BC_equation < 0 and CA_equation < 0):
        return True
    return False

def draw_triangle(triangle_vertices):
    canvas.delete("triangle")
    canvas.create_polygon(triangle_vertices, fill="#C6A2ED", outline="#3C3147", width=3, tags="triangle")

def update_score(points):
    global score
    score += points
    score_label_game.config(text=f"Score: {score}")

def start_timer(time_limit):
    global is_game_running, remaining_time
    is_game_running = True
    remaining_time = time_limit
    update_timer()

def update_timer():
    global is_game_running, remaining_time, game_over
    if is_game_running and remaining_time > 0:
        timer_text.config(text=f"Time left: {remaining_time} s")
        remaining_time -= 1
        root.after(1000, update_timer)
    else:
        if not game_over:
            is_game_running = False
            timer_text.config(text="Time's up!")
            end_game()

def end_game():
    global game_frame, game_over
    game_frame.pack_forget()
    game_over = True

    game_over_label = tk.Label(root, text="Game Over", bg='lightblue', font=('Arial', 24), fg='black')
    game_over_label.pack(pady=20)
    game_over_sound.play()

    final_score_label = tk.Label(root, text=f"Final Score: {score}", bg='lightblue', font=('Arial', 20), fg='black')
    final_score_label.pack(pady=10)

    play_again_button = tk.Button(root, text="Play Again", bg="#21CECF", fg="#000000", font=('Arial', 16), command=restart_game)
    play_again_button.pack(pady=5)

def back_to_start():
    global game_frame, game_over
    game_frame.pack_forget()
    start_frame.pack(pady=20)
    game_over = False  # Reset the game_over flag when going back to the main menu

def restart_game():
    global score, remaining_time, game_over, game_frame
    score = 0
    remaining_time = 0
    game_over = False
    game_frame.pack_forget()  # Ensure the game_frame is destroyed before creating a new one
    game_frame = tk.Frame(root, bg='lightblue')

    main()

def handle_shoot_game(x_entry, y_entry, triangle_vertices):
    try:
        shoot_x = int(x_entry.get())
        shoot_y = int(y_entry.get())
        move_ball(shoot_x, shoot_y, triangle_vertices)
        x_entry.delete(0, tk.END)
        y_entry.delete(0, tk.END)
    except ValueError:
        print("Invalid input. Please enter valid x and y coordinates.")

def show_help():
    help_text = "Help text: \nThis is a simple triangle shooting game.\nClick the 'Start Game' button to begin.\n"\
                "Enter the x and y coordinates in the input boxes and click 'Shoot' to shoot the ball.\n"\
                "The ball will move horizontally towards the specified x-coordinate and drop due to gravity.\n"\
                "If the ball lands inside the triangle, you will score a point; otherwise, you lose a point.\n"\
                "You have three chances to shoot. Good luck!"
    messagebox.showinfo("Help", help_text)

def show_instructions():
    instructions = "Instructions: \nClick 'Start Game' to begin the game.\n"\
                    "Enter the x and y coordinates to shoot the ball towards the triangle.\n"\
                    "The ball will move horizontally towards the x-coordinate and drop due to gravity.\n"\
                    "Your goal is to shoot the ball inside the triangle to score points.\n"\
                    "Each successful shot earns you 1 point, and each miss deducts 1 point.\n"\
                    "You have three chances to shoot, and the game will keep track of your score.\n"\
                    "Enjoy the game and have fun!Press esc to exit from the game\n"
    messagebox.showinfo("Instructions", instructions)

def play_game():
    global difficulty_selected
    difficulty_selected = True
    select_difficulty()

def back_to_start():
    difficulty_frame.pack_forget()
    game_frame.pack_forget()
    start_frame.pack(pady=20)

def select_difficulty():
    global start_frame
    global difficulty_frame
    start_frame.pack_forget()
    global back_button_game
    start_frame.pack_forget()
    game_frame.pack(padx=10, pady=10)

    if back_button_game is None:
        back_button_game = tk.Button(game_frame, text="Back to Menu", bg="#21CECF", fg="#000000", font=('Arial', 16), command=back_to_start)
        back_button_game.pack(pady=5)

    back_button_game.place(x=300, y=350)

    difficulty_frame = tk.Frame(root, bg='lightblue')
    difficulty_frame.pack(pady=20)

    difficulty_label = tk.Label(difficulty_frame, text="Select Difficulty:", bg='lightblue', font=('Arial', 14), fg='black')
    difficulty_label.pack(pady=10)

    easy_button = tk.Button(difficulty_frame, text="Easy", bg="#21CECF", fg="#000000", font=('Arial', 16), command=start_easy_game)
    easy_button.pack(pady=5)

    medium_button = tk.Button(difficulty_frame, text="Medium", bg="#21CECF", fg="#000000", font=('Arial', 16), command=start_medium_game)
    medium_button.pack(pady=5)

    hard_button = tk.Button(difficulty_frame, text="Hard", bg="#21CECF", fg="#000000", font=('Arial', 16), command=start_hard_game)
    hard_button.pack(pady=5)

    back_button_difficulty = tk.Button(difficulty_frame, text="Back to Menu", bg="#21CECF", fg="#000000", font=('Arial', 16), command=back_to_start)
    back_button_difficulty.pack(pady=5)

def generate_equilateral_triangle(side_length):
    x1, y1 = 100,300
    x2, y2 = x1 + side_length, y1
    x3, y3 = x1 + side_length / 2, y1 - (3 ** 0.5 / 2) * side_length
    return [(x1, y1), (x2, y2), (x3, y3)]

def generate_isosceles_triangle(base_length, height=None):
    if height is None:
        height = base_length * (3 ** 0.000005) / 1
    x1, y1 = 100,350
    x2, y2 = x1 + base_length, y1
    x3, y3 = x1 + base_length / 2, y1 - height
    return [(x1, y1), (x2, y2), (x3, y3)]

def generate_scalene_triangle():
    x1, y1 = 100, 300
    x2, y2 = 400, 300
    x3, y3 = 50, 175
    return [(x1, y1), (x2, y2), (x3, y3)]

def start_easy_game():
    difficulty_frame.pack_forget()
    game_frame.pack(padx=10, pady=10)
    vertices = generate_equilateral_triangle(300)
    start_game_with_difficulty(vertices, TIME_LIMIT_EASY)
    start_sound.play()

def start_medium_game():
    difficulty_frame.pack_forget()
    game_frame.pack(padx=10, pady=10)
    vertices = generate_isosceles_triangle(300)
    start_game_with_difficulty(vertices, TIME_LIMIT_MEDIUM)
    start_sound.play()

def start_hard_game():
    difficulty_frame.pack_forget()
    game_frame.pack(padx=10, pady=10)
    vertices = generate_scalene_triangle()
    start_game_with_difficulty(vertices, TIME_LIMIT_HARD)
    start_sound.play()

def start_game_with_difficulty(vertices, time_limit):
    global game_frame
    game_frame.pack(padx=10, pady=10)

    global canvas
    global score_label_game
    global x_entry
    global y_entry

    global timer_text
    timer_text = tk.Label(game_frame, text="", bg="#8BDAE0", font=('Arial', 14), fg='black')
    timer_text.pack(pady=5)

    canvas = tk.Canvas(game_frame, width=600, height=400, bg="#F79FEF")
    canvas.pack(padx=10, pady=10)

    draw_triangle(vertices)

    score_label_game = tk.Label(game_frame, text="Score: 0", bg="#21CECF", font=('Arial', 20))
    score_label_game.pack(pady=5)
    x_label = tk.Label(game_frame, text="Enter the x-coordinate:", bg="#8BDAE0", font=('Arial', 14), fg='black')
    x_label.pack(pady=5)
    x_entry = tk.Entry(game_frame, font=('Arial', 14))
    x_entry.pack(pady=5)

    y_label = tk.Label(game_frame, text="Enter the y-coordinate:", bg="#8BDAE0", font=('Arial', 14), fg='black')
    y_label.pack(pady=5)
    y_entry = tk.Entry(game_frame, font=('Arial', 14))
    y_entry.pack(pady=5)

    shoot_button = tk.Button(game_frame, text="Shoot", bg="#21CECF", fg='black', font=('Arial', 16), command=lambda: handle_shoot_game(x_entry, y_entry, vertices))
    shoot_button.pack(pady=10)

    remaining_time = time_limit
    start_timer(time_limit)


def main():
    global game_frame
    global start_frame
    global root
    global difficulty_frame

    root = tk.Tk()
    root.title("Triangle Game")
    root.configure(bg='lightblue')

    start_frame = tk.Frame(root, bg='lightblue')
    start_frame.pack(pady=20)

    instruction_label = tk.Label(start_frame, text="Click on a button to get started", bg='lightblue', font=('Arial', 14), fg='black')
    instruction_label.pack(pady=10)

    start_button = tk.Button(start_frame, text="Start Game", bg="#21CECF", fg="#000000", font=('Arial', 16), command=play_game)
    start_button.pack(pady=5)

    help_button = tk.Button(start_frame, text="Help", bg="#21CECF", fg="#000000", font=('Arial', 16), command=show_help)
    help_button.pack(pady=5)

    instruction_button = tk.Button(start_frame, text="Instructions", bg="#21CECF", fg="#000000", font=('Arial', 16), command=show_instructions)
    instruction_button.pack(pady=5)

    game_frame = tk.Frame(root, bg='lightblue')

    

    play_sound_button = tk.Button(root, text="MUSIC ON", bg = "#21CECF" ,fg="#000000", command=play_sound)
    play_sound_button.pack(side = "left" , padx=60)

    stop_sound_button = tk.Button(root, text=" MUSIC OFF", bg = "#21CECF" ,fg="#000000", command=stop_sound)
    stop_sound_button.pack(side = "right" , padx=60)

    root.mainloop()
import tkinter as tk
from tkinter import messagebox
import pygame
from pygame import mixer

BALL_RADIUS = 15
BALL_SPEED = 3
GRAVITY = 0.5
score = 0
TIME_LIMIT_EASY = 60
TIME_LIMIT_MEDIUM = 30
TIME_LIMIT_HARD = 10

timer_text = None
is_game_running = False
remaining_time = 0

pygame.mixer.init()
correct_sound = pygame.mixer.Sound(r"C:\Users\admin\Downloads\421002__eponn__correct.wav")
wrong_sound = pygame.mixer.Sound(r"C:\Users\admin\Downloads\243700__ertfelda__incorrect.wav")
game_over_sound = pygame.mixer.Sound(r"C:\Users\admin\Downloads\433644__dersuperanton__game-over-sound.wav")
start_sound = pygame.mixer.Sound(r"C:\Users\admin\Downloads\144033188-deep-male-voice-god-character-_1_.wav")

def play_sound():
        pygame.mixer.music.load(r"C:\Users\admin\Downloads\641014__igorchagas__enigmatic-polyphony.wav")
        pygame.mixer.music.play()
def stop_sound():
        pygame.mixer.music.stop()



canvas = None
score_label_game = None
back_button_game = None
difficulty_selected = False
difficulty_frame = None

game_over = False

def draw_ball(x, y):
    canvas.delete("ball")
    canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill='yellow', tags="ball")

def move_ball(target_x, target_y, triangle_vertices):
    ball_x = 50
    ball_y = 50
    ball_velocity = 0
    while ball_x < target_x:
        if not difficulty_selected:
            return
        ball_x += BALL_SPEED
        draw_ball(ball_x, ball_y)
        canvas.update()
        canvas.after(50)
    while ball_y < target_y:
        if not difficulty_selected:
            return
        ball_y += ball_velocity
        ball_velocity += GRAVITY
        draw_ball(ball_x, ball_y)
        canvas.update()

    result = is_inside_triangle(target_x, target_y, triangle_vertices)
    if result:
        update_score(100)
        correct_sound.play()
    else:
        update_score(-50)
        wrong_sound.play()

def is_inside_triangle(x, y, triangle_vertices):
    x1, y1 = triangle_vertices[0]
    x2, y2 = triangle_vertices[1]
    x3, y3 = triangle_vertices[2]
    AB_equation = ((x2 - x1) * (y - y1)) - ((y2 - y1) * (x - x1))
    BC_equation = ((x3 - x2) * (y - y2)) - ((y3 - y2) * (x - x2))
    CA_equation = ((x1 - x3) * (y - y3)) - ((y1 - y3) * (x - x3))
    if (AB_equation > 0 and BC_equation > 0 and CA_equation > 0) or (AB_equation < 0 and BC_equation < 0 and CA_equation < 0):
        return True
    return False

def draw_triangle(triangle_vertices):
    canvas.delete("triangle")
    canvas.create_polygon(triangle_vertices, fill="#C6A2ED", outline="#3C3147", width=3, tags="triangle")

def update_score(points):
    global score
    score += points
    score_label_game.config(text=f"Score: {score}")

def start_timer(time_limit):
    global is_game_running, remaining_time
    is_game_running = True
    remaining_time = time_limit
    update_timer()

def update_timer():
    global is_game_running, remaining_time, game_over
    if is_game_running and remaining_time > 0:
        timer_text.config(text=f"Time left: {remaining_time} s")
        remaining_time -= 1
        root.after(1000, update_timer)
    else:
        if not game_over:
            is_game_running = False
            timer_text.config(text="Time's up!")
            end_game()

def end_game():
    global game_frame, game_over
    game_frame.pack_forget()
    game_over = True

    game_over_label = tk.Label(root, text="Game Over", bg='lightblue', font=('Arial', 24), fg='black')
    game_over_label.pack(pady=20)
    game_over_sound.play()

    final_score_label = tk.Label(root, text=f"Final Score: {score}", bg='lightblue', font=('Arial', 20), fg='black')
    final_score_label.pack(pady=10)

    play_again_button = tk.Button(root, text="Play Again", bg="#21CECF", fg="#000000", font=('Arial', 16), command=restart_game)
    play_again_button.pack(pady=5)

def back_to_start():
    global game_frame, game_over
    game_frame.pack_forget()
    start_frame.pack(pady=20)
    game_over = False  # Reset the game_over flag when going back to the main menu

def restart_game():
    global score, remaining_time, game_over, game_frame
    score = 0
    remaining_time = 0
    game_over = False
    game_frame.pack_forget()  # Ensure the game_frame is destroyed before creating a new one
    game_frame = tk.Frame(root, bg='lightblue')

    main()

def handle_shoot_game(x_entry, y_entry, triangle_vertices):
    try:
        shoot_x = int(x_entry.get())
        shoot_y = int(y_entry.get())
        move_ball(shoot_x, shoot_y, triangle_vertices)
        x_entry.delete(0, tk.END)
        y_entry.delete(0, tk.END)
    except ValueError:
        print("Invalid input. Please enter valid x and y coordinates.")

def show_help():
    help_text = "Help text: \nThis is a simple triangle shooting game.\nClick the 'Start Game' button to begin.\n"\
                "Enter the x and y coordinates in the input boxes and click 'Shoot' to shoot the ball.\n"\
                "The ball will move horizontally towards the specified x-coordinate and drop due to gravity.\n"\
                "If the ball lands inside the triangle, you will score a point; otherwise, you lose a point.\n"\
                "You have three chances to shoot. Good luck!"
    messagebox.showinfo("Help", help_text)

def show_instructions():
    instructions = "Instructions: \nClick 'Start Game' to begin the game.\n"\
                    "Enter the x and y coordinates to shoot the ball towards the triangle.\n"\
                    "The ball will move horizontally towards the x-coordinate and drop due to gravity.\n"\
                    "Your goal is to shoot the ball inside the triangle to score points.\n"\
                    "Each successful shot earns you 1 point, and each miss deducts 1 point.\n"\
                    "You have three chances to shoot, and the game will keep track of your score.\n"\
                    "Enjoy the game and have fun!Press esc to exit from the game\n"
    messagebox.showinfo("Instructions", instructions)

def play_game():
    global difficulty_selected
    difficulty_selected = True
    select_difficulty()

def back_to_start():
    difficulty_frame.pack_forget()
    game_frame.pack_forget()
    start_frame.pack(pady=20)

def select_difficulty():
    global start_frame
    global difficulty_frame
    start_frame.pack_forget()
    global back_button_game
    start_frame.pack_forget()
    game_frame.pack(padx=10, pady=10)

    if back_button_game is None:
        back_button_game = tk.Button(game_frame, text="Back to Menu", bg="#21CECF", fg="#000000", font=('Arial', 16), command=back_to_start)
        back_button_game.pack(pady=5)

    back_button_game.place(x=300, y=350)

    difficulty_frame = tk.Frame(root, bg='lightblue')
    difficulty_frame.pack(pady=20)

    difficulty_label = tk.Label(difficulty_frame, text="Select Difficulty:", bg='lightblue', font=('Arial', 14), fg='black')
    difficulty_label.pack(pady=10)

    easy_button = tk.Button(difficulty_frame, text="Easy", bg="#21CECF", fg="#000000", font=('Arial', 16), command=start_easy_game)
    easy_button.pack(pady=5)

    medium_button = tk.Button(difficulty_frame, text="Medium", bg="#21CECF", fg="#000000", font=('Arial', 16), command=start_medium_game)
    medium_button.pack(pady=5)

    hard_button = tk.Button(difficulty_frame, text="Hard", bg="#21CECF", fg="#000000", font=('Arial', 16), command=start_hard_game)
    hard_button.pack(pady=5)

    back_button_difficulty = tk.Button(difficulty_frame, text="Back to Menu", bg="#21CECF", fg="#000000", font=('Arial', 16), command=back_to_start)
    back_button_difficulty.pack(pady=5)

def generate_equilateral_triangle(side_length):
    x1, y1 = 100,300
    x2, y2 = x1 + side_length, y1
    x3, y3 = x1 + side_length / 2, y1 - (3 ** 0.5 / 2) * side_length
    return [(x1, y1), (x2, y2), (x3, y3)]

def generate_isosceles_triangle(base_length, height=None):
    if height is None:
        height = base_length * (3 ** 0.000005) / 1
    x1, y1 = 100,350
    x2, y2 = x1 + base_length, y1
    x3, y3 = x1 + base_length / 2, y1 - height
    return [(x1, y1), (x2, y2), (x3, y3)]

def generate_scalene_triangle():
    x1, y1 = 100, 300
    x2, y2 = 400, 300
    x3, y3 = 50, 175
    return [(x1, y1), (x2, y2), (x3, y3)]

def start_easy_game():
    difficulty_frame.pack_forget()
    game_frame.pack(padx=10, pady=10)
    vertices = generate_equilateral_triangle(300)
    start_game_with_difficulty(vertices, TIME_LIMIT_EASY)
    start_sound.play()

def start_medium_game():
    difficulty_frame.pack_forget()
    game_frame.pack(padx=10, pady=10)
    vertices = generate_isosceles_triangle(300)
    start_game_with_difficulty(vertices, TIME_LIMIT_MEDIUM)
    start_sound.play()

def start_hard_game():
    difficulty_frame.pack_forget()
    game_frame.pack(padx=10, pady=10)
    vertices = generate_scalene_triangle()
    start_game_with_difficulty(vertices, TIME_LIMIT_HARD)
    start_sound.play()

def start_game_with_difficulty(vertices, time_limit):
    global game_frame
    game_frame.pack(padx=10, pady=10)

    global canvas
    global score_label_game
    global x_entry
    global y_entry

    global timer_text
    timer_text = tk.Label(game_frame, text="", bg="#8BDAE0", font=('Arial', 14), fg='black')
    timer_text.pack(pady=5)

    canvas = tk.Canvas(game_frame, width=600, height=400, bg="#F79FEF")
    canvas.pack(padx=10, pady=10)

    draw_triangle(vertices)

    score_label_game = tk.Label(game_frame, text="Score: 0", bg="#21CECF", font=('Arial', 20))
    score_label_game.pack(pady=5)
    x_label = tk.Label(game_frame, text="Enter the x-coordinate:", bg="#8BDAE0", font=('Arial', 14), fg='black')
    x_label.pack(pady=5)
    x_entry = tk.Entry(game_frame, font=('Arial', 14))
    x_entry.pack(pady=5)

    y_label = tk.Label(game_frame, text="Enter the y-coordinate:", bg="#8BDAE0", font=('Arial', 14), fg='black')
    y_label.pack(pady=5)
    y_entry = tk.Entry(game_frame, font=('Arial', 14))
    y_entry.pack(pady=5)

    shoot_button = tk.Button(game_frame, text="Shoot", bg="#21CECF", fg='black', font=('Arial', 16), command=lambda: handle_shoot_game(x_entry, y_entry, vertices))
    shoot_button.pack(pady=10)

    remaining_time = time_limit
    start_timer(time_limit)


def main():
    global game_frame
    global start_frame
    global root
    global difficulty_frame

    root = tk.Tk()
    root.title("Triangle Game")
    root.configure(bg='lightblue')

    start_frame = tk.Frame(root, bg='lightblue')
    start_frame.pack(pady=20)

    instruction_label = tk.Label(start_frame, text="Click on a button to get started", bg='lightblue', font=('Arial', 14), fg='black')
    instruction_label.pack(pady=10)

    start_button = tk.Button(start_frame, text="Start Game", bg="#21CECF", fg="#000000", font=('Arial', 16), command=play_game)
    start_button.pack(pady=5)

    help_button = tk.Button(start_frame, text="Help", bg="#21CECF", fg="#000000", font=('Arial', 16), command=show_help)
    help_button.pack(pady=5)

    instruction_button = tk.Button(start_frame, text="Instructions", bg="#21CECF", fg="#000000", font=('Arial', 16), command=show_instructions)
    instruction_button.pack(pady=5)

    game_frame = tk.Frame(root, bg='lightblue')

    

    play_sound_button = tk.Button(root, text="MUSIC ON", bg = "#21CECF" ,fg="#000000", command=play_sound)
    play_sound_button.pack(side = "left" , padx=60)

    stop_sound_button = tk.Button(root, text=" MUSIC OFF", bg = "#21CECF" ,fg="#000000", command=stop_sound)
    stop_sound_button.pack(side = "right" , padx=60)

    root.mainloop()

if __name__ == "__main__":
    main()
