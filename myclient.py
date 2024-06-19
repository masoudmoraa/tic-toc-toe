import pygame as pg
import socket     
import threading        

class Connection:
    def __init__(self) -> None:
        # Initialize socket for communication
        self.the_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.PORT = 12345
        self.IP = "127.0.0.1"

    def connect_to_server(self, size, name) -> None:
        # Connect to the server and send the size of the board and player's name
        self.the_socket.connect((self.IP, self.PORT))
        self.the_socket.send((str(size) + name).encode())

    def make_move(self, sign, cell) -> None:
        # Send the player's move to the server
        self.the_socket.send((sign + str(cell)).encode())

    def send_message(self, message) -> None:
        # Placeholder for sending messages, not implemented yet
        pass

    # needs a new thread, always listening on the socket.
    def recv_message(self) -> str:
        # Receive messages from the server
        message = self.the_socket.recv(1024).decode()
        return message
    
class GUI :
    def __init__(self) -> None:
        # 1 means name
        # 2 means choose game
        # 3 means waiting for opponnet
        # 4 means playing game
        self.menu_number = 0;
        self.screenn = pg.display.set_mode((720, 540))
        self.font24 = pg.font.Font(None, 24)
        self.font32 = pg.font.Font(None, 32)
        self.font40 = pg.font.Font(None, 40)
        self.name = ""
        self.server = Connection()
        self.sign = None
        self.opponent_name = ""
        self.server_message_list = []
        self.winner = None

    def name_menu(self) -> None:
        pg.display.set_caption("Tic Tac Toe")
        input_box = pg.Rect(260, 100, 140, 32)
        color_inactive = pg.Color('lightskyblue3')
        color_active = pg.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            # event handler
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                    self.menu_number = -1

                if event.type == pg.MOUSEBUTTONDOWN:
                    active = False
                    if input_box.collidepoint(event.pos):
                        active = True
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive

                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN:
                            self.menu_number = 1
                            self.name = text
                            done = True
                        elif event.key == pg.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.screenn.fill((30, 30, 30))
            name_surface = self.font32.render("Enter your name ->", True, color)
            txt_surface = self.font32.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            self.screenn.blit(name_surface, (25, 105))
            self.screenn.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pg.draw.rect(self.screenn, color, input_box, 2)

            pg.display.update()
            pg.time.Clock().tick(30)

    def choose_game_menu(self) -> None:
        box1 = pg.Rect(260, 100, 200, 40)
        box2 = pg.Rect(260, 160, 200, 40)
        box3 = pg.Rect(260, 220, 200, 40)
        box4 = pg.Rect(260, 280, 200, 40)
        color_inactive = pg.Color('lightskyblue3')
        color_active = pg.Color('dodgerblue2')
        color1 = color_inactive
        color2 = color_inactive
        color3 = color_inactive
        color4 = color_inactive
        done = False

        while not done:
            # event handler
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                    self.menu_number = -1
                if event.type == pg.MOUSEMOTION:
                    pos = event.pos
                    color1 = color2 = color3 = color4 = color_inactive
                    if box1.collidepoint(pos):
                        color1 = color_active
                    if box2.collidepoint(pos):
                        color2 = color_active
                    if box3.collidepoint(pos):
                        color3 = color_active
                    if box4.collidepoint(pos):
                        color4 = color_active
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if box1.collidepoint(pos):
                        done = True
                        self.menu_number = 23
                    if box2.collidepoint(pos):
                        done = True
                        self.menu_number = 24
                    if box3.collidepoint(pos):
                        done = True
                        self.menu_number = 25
                    if box4.collidepoint(pos):
                        done = True
                        self.menu_number = -1

            self.screenn.fill((30, 30, 30))
            text1 = self.font32.render("3 × 3", True, color1)
            text2 = self.font32.render("4 × 4", True, color2)
            text3 = self.font32.render("5 × 5", True, color3)
            text4 = self.font32.render("Quit ", True, color4)
            pg.draw.rect(self.screenn, color1, box1, 2)
            pg.draw.rect(self.screenn, color2, box2, 2)
            pg.draw.rect(self.screenn, color3, box3, 2)
            pg.draw.rect(self.screenn, color4, box4, 2)
            self.screenn.blit(text1, (333, 108))
            self.screenn.blit(text2, (333, 168))
            self.screenn.blit(text3, (333, 228))
            self.screenn.blit(text4, (333, 288))
            pg.display.update()
            pg.time.Clock().tick(30)

    def search_for_opponent(self, board_size) -> None:
        done = False
        self.server.connect_to_server(board_size, self.name)

        # provide dynamic text until found a match
        t2 = threading.Thread(target = self.dynamic_search_page, args=())
        t2.start()

        while not done :
            message = self.server.recv_message()
            if (message == "waiting for opponent...") :
                pass
            if (message == "Found") :
                if(board_size == 3) : 
                    self.menu_number = 3
                if(board_size == 4) : 
                    self.menu_number = 4
                if(board_size == 5) : 
                    self.menu_number = 5
                done = True
    
    # function to provide dynamic text when user is waiting for opponent
    def dynamic_search_page(self) -> None :
        done = True
        image_x = pg.image.load('./images/x-pre.png')
        image_o = pg.image.load('./images/o-pre.png')
        image_x = pg.transform.scale(image_x, (200, 200))
        image_o = pg.transform.scale(image_o, (200, 200))
        left  = pg.Rect(0, 0, 360, 540)
        right = pg.Rect(360, 0, 360, 540)
        t = ["SEARCHING FOR OPPONENT", "SEARCHING FOR OPPONENT .", "SEARCHING FOR OPPONENT . .", "SEARCHING FOR OPPONENT . . ."]
        i = 0
        while self.menu_number > 20 and done:
            self.screenn.fill((30, 30 ,30))
            pg.draw.rect(self.screenn, (90,0,2), left)
            pg.draw.rect(self.screenn, (2,0,90), right)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.menu_number = -1
            
            self.screenn.blit(image_x, (80, 170))
            self.screenn.blit(image_o, (440, 170))
            text1 = self.font32.render(t[i], True, (240, 240, 240))
            i = (i + 1) % 4 
            self.screenn.blit(text1, (205, 460))
            pg.display.update()
            pg.time.Clock().tick(2)

        return

    def play3(self) -> None :
        done = False
        color_inactive = pg.Color('lightskyblue3')
        color_active = pg.Color('dodgerblue2')

        image_x = pg.image.load('./images/x.png')
        image_o = pg.image.load('./images/o.png')
        
        # 0 : opponent name    1 : sign     2 : turn
        info = (self.server.recv_message()).split(",")
        opponent_name = self.font40.render(info[0], True, color_inactive)
        user_name = self.font40.render(self.name, True, color_inactive)
        
        image_x = pg.transform.scale(image_x, (60, 60))
        image_o = pg.transform.scale(image_o, (60, 60))
        image_x_small = pg.transform.scale(image_x, (34, 34))
        image_o_small = pg.transform.scale(image_o, (34, 34))       

        # set veiw
        self.screenn.fill((30, 30, 30))
        for i in range(4) :
            pg.draw.line(self.screenn, color_inactive, [300 + i*100, 100], [300 + i*100, 400], 4)
            pg.draw.line(self.screenn, color_inactive, [300, 100 + i*100], [600, 100 + i*100], 4)
        self.screenn.blit(opponent_name, (420, 40))
        self.screenn.blit(user_name, (70, 40))
        
        self.sign = info[1]
        if(info[1] == 'X') :
            self.screenn.blit(image_x_small, (20, 38))
            self.screenn.blit(image_o_small, (370, 38))
        else :
            self.screenn.blit(image_o_small, (20, 38))
            self.screenn.blit(image_x_small, (370, 38))
        
        # server message space
        server_space = pg.Rect(305, 455, 415, 135)
        if(info[2] == '1') :
            message = "your turn"
            if(info[1] == 'X') :
                turn = 'X'
            else :
                turn = 'O'
        else :
            message = info[0] + "'s turn"
            if(info[1] == 'X') :
                turn = 'O'
            else :
                turn = 'X'

        t = threading.Thread(target=self.ingame_listener)
        t.start()

        while not done:
            # event handler
            if(len(self.server_message_list) > 0):
                m = self.server_message_list.pop(0)
                m = m.split(",")
                if(m[1] == "invalid") :
                    message = "choose  an empty cell !"
                if(m[1] == "OK") :
                    # show the move
                    cell = int(m[0][1:])
                    x_pos = cell % 3
                    y_pos = cell // 3
                    if(m[0][0] == 'X') :
                        self.screenn.blit(image_x, (x_pos*100 + 320, y_pos*100 + 120))
                    else :
                        self.screenn.blit(image_o, (x_pos*100 + 320, y_pos*100 + 120))

                    # change some configs
                    print("change state")
                    if(turn == 'X') :
                        turn = 'O'
                    else : 
                        turn = 'X'
                    if(turn == info[1]) : 
                        message = "your turn"
                        print("my turn")
                    else : 
                        print("oppo turn")
                        message = info[0] + "'s turn"
                if(m[1] == "wins!") :
                    print("player " + m[0] + " wins")
                    self.winner = m[0]
                    self.menu_number = 7
                    done = True
                    break

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                    self.menu_number = -1
        
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if(pos[0] > 300 and pos[0] < 600 and pos[1] > 100 and pos[1] < 400) :
                        number_of_cell = ((pos[0] - 300) // 100) + ((pos[1] - 100) // 100) * 3
                        if (turn == info[1]) :
                            print("send modve")
                            self.server.make_move(info[1], number_of_cell)
                        else :
                            message = "It's not your turn"

            server_message = self.font24.render(message, True, color_inactive)
            pg.draw.rect(self.screenn, (30,30,30), server_space)
            self.screenn.blit(server_message, (320, 470))
            pg.display.update()
            pg.time.Clock().tick(5)

    def ingame_listener(self) -> None :
        done = False
        while not done :
            m = self.server.recv_message()
            if(len(m) == 0) :
                break
            self.server_message_list.append(m)
            m.split(",")
            if m[1] == "wins!" :
                break
        return



    def play4(self) -> None :
        done = False
        color_inactive = pg.Color('lightskyblue3')
        color_active = pg.Color('dodgerblue2')

        image_x = pg.image.load('./images/x.png')
        image_o = pg.image.load('./images/o.png')
        
        # 0 : opponent name    1 : sign     2 : turn
        info = (self.server.recv_message()).split(",")
        opponent_name = self.font40.render(info[0], True, color_inactive)
        user_name = self.font40.render(self.name, True, color_inactive)
        
        image_x = pg.transform.scale(image_x, (50, 50))
        image_o = pg.transform.scale(image_o, (50, 50))
        image_x_small = pg.transform.scale(image_x, (34, 34))
        image_o_small = pg.transform.scale(image_o, (34, 34)) 


        self.screenn.fill((30, 30, 30))
        for i in range(5) :
            pg.draw.line(self.screenn, color_inactive, [300 + i*80, 100], [300 + i*80, 420], 4)
            pg.draw.line(self.screenn, color_inactive, [300, 100 + i*80], [620, 100 + i*80], 4)

        self.screenn.blit(opponent_name, (420, 40))
        self.screenn.blit(user_name, (70, 40))
        
        self.sign = info[1]
        if(info[1] == 'X') :
            self.screenn.blit(image_x_small, (20, 38))
            self.screenn.blit(image_o_small, (370, 38))
        else :
            self.screenn.blit(image_o_small, (20, 38))
            self.screenn.blit(image_x_small, (370, 38))
        
        # server message space
        server_space = pg.Rect(305, 455, 415, 135)
        if(info[2] == '1') :
            message = "your turn"
            if(info[1] == 'X') :
                turn = 'X'
            else :
                turn = 'O'
        else :
            message = info[0] + "'s turn"
            if(info[1] == 'X') :
                turn = 'O'
            else :
                turn = 'X'

        t = threading.Thread(target=self.ingame_listener)
        t.start()

        while not done:
            # event handler
            if(len(self.server_message_list) > 0):
                m = self.server_message_list.pop(0)
                m = m.split(",")
                if(m[1] == "invalid") :
                    message = "choose an empty cell!"
                if(m[1] == "OK") :
                    # show the move
                    cell = int(m[0][1:])
                    x_pos = cell % 4
                    y_pos = cell // 4
                    if(m[0][0] == 'X') :
                        self.screenn.blit(image_x, (x_pos*80 + 315, y_pos*80 + 115))
                    else :
                        self.screenn.blit(image_o, (x_pos*80 + 315, y_pos*80 + 115))

                    # change some configs
                    print("change state")
                    if(turn == 'X') :
                        turn = 'O'
                    else : 
                        turn = 'X'
                    if(turn == info[1]) : 
                        message = "your turn"
                        print("my turn")
                    else : 
                        print("oppo turn")
                        message = info[0] + "'s turn"
                if(m[1] == "wins!") :
                    print("player " + m[0] + " wins")
                    self.winner = m[0]
                    self.menu_number = 7
                    done = True
                    break

            # event handler
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                    self.menu_number = -1
        
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if(pos[0] > 300 and pos[0] < 620 and pos[1] > 100 and pos[1] < 420) :
                        number_of_cell = ((pos[0] - 300) // 80) + ((pos[1] - 100) // 80) * 4
                        print(number_of_cell)
                        if (turn == info[1]) :
                            print("send modve")
                            self.server.make_move(info[1], number_of_cell)
                        else :
                            message = "It's not your turn"

            server_message = self.font24.render(message, True, color_inactive)
            pg.draw.rect(self.screenn, (30,30,30), server_space)
            self.screenn.blit(server_message, (320, 470))
            pg.display.update()
            pg.time.Clock().tick(5)

    def play5(self) -> None :
        done = False
        color_inactive = pg.Color('lightskyblue3')
        color_active = pg.Color('dodgerblue2')

        image_x = pg.image.load('x.png')
        image_o = pg.image.load('o.png')
        
        # 0 : opponent name    1 : sign     2 : turn
        info = (self.server.recv_message()).split(",")
        opponent_name = self.font40.render(info[0], True, color_inactive)
        user_name = self.font40.render(self.name, True, color_inactive)
        
        image_x = pg.transform.scale(image_x, (44, 44))
        image_o = pg.transform.scale(image_o, (44, 44))
        image_x_small = pg.transform.scale(image_x, (34, 34))
        image_o_small = pg.transform.scale(image_o, (34, 34)) 

        self.screenn.fill((30, 30, 30))
        for i in range(6) :
            pg.draw.line(self.screenn, color_inactive, [300 + i*70, 100], [300 + i*70, 450], 4)
            pg.draw.line(self.screenn, color_inactive, [300, 100 + i*70], [650, 100 + i*70], 4)

        self.screenn.blit(opponent_name, (420, 40))
        self.screenn.blit(user_name, (70, 40))
        
        self.sign = info[1]
        if(info[1] == 'X') :
            self.screenn.blit(image_x_small, (20, 38))
            self.screenn.blit(image_o_small, (370, 38))
        else :
            self.screenn.blit(image_o_small, (20, 38))
            self.screenn.blit(image_x_small, (370, 38))
        
        # server message space
        server_space = pg.Rect(305, 455, 415, 135)
        if(info[2] == '1') :
            message = "your turn"
            if(info[1] == 'X') :
                turn = 'X'
            else :
                turn = 'O'
        else :
            message = info[0] + "'s turn"
            if(info[1] == 'X') :
                turn = 'O'
            else :
                turn = 'X'

        t = threading.Thread(target=self.ingame_listener)
        t.start()
        
        while not done:
            # event handler
            if(len(self.server_message_list) > 0):
                m = self.server_message_list.pop(0)
                m = m.split(",")
                if(m[1] == "invalid") :
                    message = "choose an empty cell!"
                if(m[1] == "OK") :
                    # show the move
                    cell = int(m[0][1:])
                    x_pos = cell % 5
                    y_pos = cell // 5
                    if(m[0][0] == 'X') :
                        self.screenn.blit(image_x, (x_pos*70 + 314, y_pos*70 + 114))
                    else :
                        self.screenn.blit(image_o, (x_pos*70 + 314, y_pos*70 + 114))

                    # change some configs
                    print("change state")
                    if(turn == 'X') :
                        turn = 'O'
                    else : 
                        turn = 'X'
                    if(turn == info[1]) : 
                        message = "your turn"
                        print("my turn")
                    else : 
                        print("oppo turn")
                        message = info[0] + "'s turn"
                if(m[1] == "wins!") :
                    print("player " + m[0] + " wins")
                    self.winner = m[0]
                    self.menu_number = 7
                    done = True
                    break

            # event handler
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                    self.menu_number = -1
        
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if(pos[0] > 300 and pos[0] < 650 and pos[1] > 100 and pos[1] < 450) :
                        number_of_cell = ((pos[0] - 300) // 70) + ((pos[1] - 100) // 70) * 5
                        if (turn == info[1]) :
                            print("send modve")
                            self.server.make_move(info[1], number_of_cell)
                        else :
                            message = "It's not your turn"

            server_message = self.font24.render(message, True, color_inactive)
            pg.draw.rect(self.screenn, (30,30,30), server_space)
            self.screenn.blit(server_message, (320, 470))
            pg.display.update()
            pg.time.Clock().tick(5)

    def result(self) -> None :
        print("winner :  ", self.winner)
        print("me     :  ", self.sign)
        if(self.winner == self.sign) :
            final = "You Won!"
            final_color = (0,150,230)
        else :
            final = "You Lost!"
            final_color = (150,10,10)
            
        done = False
        box1 = pg.Rect(75, 200, 150, 40)
        box2 = pg.Rect(75, 260, 150, 40)
        color_inactive = pg.Color(128,128,128)
        color_active = pg.Color(195,195,195)
        color1 = color_inactive
        color2 = color_inactive
        black_space = pg.Rect(50, 0, 200, 540)

        while not done:
            # event handler
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                    self.menu_number = -1
        
                if event.type == pg.MOUSEMOTION:
                    pos = event.pos
                    color1 = color2 = color_inactive
                    if box1.collidepoint(pos):
                        color1 = color_active
                    if box2.collidepoint(pos):
                        color2 = color_active

                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if box1.collidepoint(pos):
                        done = True
                        self.menu_number = 1
                        self.clear()
                    if box2.collidepoint(pos):
                        done = True
                        self.menu_number = -1


            pg.draw.rect(self.screenn, (10,10,10), black_space)
            text1 = self.font32.render("Menu", True, color1)
            text2 = self.font32.render("Quit", True, color2)
            final_res = self.font40.render(final, True, final_color)
            pg.draw.rect(self.screenn, color1, box1, 2)
            pg.draw.rect(self.screenn, color2, box2, 2)
            self.screenn.blit(final_res, (90, 110))
            self.screenn.blit(text1, (122, 210))
            self.screenn.blit(text2, (127, 270))

            pg.display.update()
            pg.time.Clock().tick(30)

    def clear(self) -> None :
        self.server = Connection()
        self.sign = None
        self.opponent_name = ""
        self.server_message_list = []
        self.winner = None

if __name__ == '__main__':
    pg.init()
    game_window = GUI()
    
    # Main game loop
    while True :
        # close the program
        if(game_window.menu_number == -1) :
            break
        # menu that users enter their name
        if(game_window.menu_number == 0) :
            game_window.name_menu();
        # user choose the size of board
        if(game_window.menu_number == 1) :
            game_window.choose_game_menu()
        # showing another screen when user is waiting for play
        if(game_window.menu_number > 20) :
            game_window.search_for_opponent(game_window.menu_number % 10)
        # 3*3 board game handler
        if(game_window.menu_number == 3) :
            game_window.play3()
        # 4*4 board game handler
        if(game_window.menu_number == 4) :
            game_window.play4()
        # 5*5 board game handler
        if(game_window.menu_number == 5) :
            game_window.play5()
        # manage menu after the game
        if(game_window.menu_number == 7) :
            game_window.result()
    pg.quit()