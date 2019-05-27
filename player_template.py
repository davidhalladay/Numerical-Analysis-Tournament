import numpy as np

class player_module:

    # constructor, allocate any private date here
    def __init__(self):
        self.init_x, self.init_y = -1., -1.

    # Please update the banner according to your information
    def banner(self):
        print('-'*40)
        print('Author: Wan-Cyuan Fan')
        print('ID: b04502105')
        print('-'*40)

    # Decision making function for moving your ship, toward next frame:
    # simply return the speed and the angle
    # ----------------------------------------------
    # The value of "speed" must be between 0 and 1.
    # speed = 1 : full speed, moving 0.01 in terms of space coordination in next frame
    # speed = x : moving 0.01*x in terms of space coordination
    # speed = 0 : just don't move
    #
    # The value of angle must be between 0 and 2*pi.
    #
    # if speed is less than 1, it will store the gauge value by 4*(1-speed).
    # If the gauge value reach 1000, it will perform the "gauge attack" and destory
    # any enemy within a circle of 0.6 radius
    #
    def decision(self,player_data, enemy_data):

        speed, angle = 0., 0.
        balence_y = 0.2

        # your data
        player1_x      = player_data[0][0]
        player1_y      = player_data[0][1]
        player1_hp     = player_data[0][2]
        player1_score  = player_data[0][3]
        player1_gauge  = player_data[0][4]
        player1_weapon = player_data[0][5]

        # data for another player
        player2_x      = player_data[1][0]
        player2_y      = player_data[1][1]
        player2_hp     = player_data[1][2]
        player2_score  = player_data[1][3]
        player2_gauge  = player_data[1][4]
        player2_weapon = player_data[1][5]

        # save the initial x position
        if self.init_x==-1. and self.init_y==-1.:
            self.init_x, self.init_y = player1_x, player1_y

        # let's try to move back to the initial position by default
        speed = ((self.init_x-player1_x)**2 + (self.init_y-player1_y)**2)**0.5
        speed /= 0.01 # since the maximum speed is 0.01 unit per frame
        if speed>1.: speed = 1.
        angle = np.arctan2(self.init_y-player1_y,self.init_x-player1_x)

        # loop over the enemies and bullets
        for data in enemy_data:
            will_be_hit = False
            type = data[0] # 0 - bullet, 1..4 - different types of invaders, 5 - ufo, 6 - boss, 7 - rescuecap, 8 - weaponup
            invaders = [1,2,3,4,5]
            boss = [6]
            good = [7,8]
            x    = data[1]
            y    = data[2]
            dx   = data[3] # expected movement in x direction for the next frame
            dy   = data[4] # expected movement in y direction for the next frame

            # calculate the distance toward player1
            dist = ((x-player1_x)**2+(y-player1_y)**2)**0.5
            # judge whether the bullet will hit player1

            # Decision 1 : player will be hit and bullet is inside safety region
            #################################################
            #####           dodging bullet Strategy
            #################################################
            if (type in [0]) and dist < 0.212:
                print("WARNING! You will be hit!")
                will_be_hit = True
                # colculate the collision point x-coor.
                m_data = dy/dx
                x_collision = (player1_y - y + dx/dy * player1_x + dy/dx * x)/(m_data + 1./m_data)
                y_collision = (player1_x - x + dy/dx * player1_y + dx/dy * y)/(m_data + 1./m_data)
                # dis_PL = abs(dy*player1_x - dx*player1_y + dx*y - dy*x)/(dy**2 + dx**2)*0.5
                safe_dist = ((x_collision - x)**2+(y_collision - y)**2)**0.5
                # check safety
                if safe_dist < 0.001:
                    speed = 0.
                    continue
                else:
                    speed = 0.9
                    # bullet will hit the left-down sidee
                    if x_collision < player1_x and y_collision < player1_y :
                        angle = np.arctan2(abs(player1_y-y_collision),abs(player1_x-x_collision))
                    # bullet will hit the right-down side
                    elif x_collision >= player1_x and y_collision < player1_y :
                        angle = np.arctan2(abs(player1_y-y_collision),player1_x-x_collision)
                    # bullet will hit the left-up side
                    elif x_collision < player1_x and y_collision >= player1_y :
                        angle = np.arctan2((player1_y-y_collision),abs(player1_x-x_collision))
                    # bullet will hit the right-up side
                    else :
                        angle = np.arctan2((player1_y-y_collision),(player1_x-x_collision))
                    break

            if type == 6 and dist < 0.283:
                speed = 1.0
                if x > player1_x: angle = np.pi
                if x < player1_x: angle = 0
                break

            #if type == 6 and dist >= 0.283 and y >= 0.85 and player1_y >= 0.8 and (player1_x > 0.8 or player1_x < 0.2):
            #    speed = 1.0
            #    angle = 3.*np.pi/2.
            #    break

            if (type in [1,2]) and dist < 0.22:
                if x < player1_x: angle = 0.    # escape to right
                elif x >= player1_x: angle = np.pi # escape to left
                break

            if (type in [4]) and dist < 0.12:
                print("WARNING! You will be hit!")
                will_be_hit = True
                # colculate the collision point x-coor.
                m_data = dy/dx
                x_collision = (player1_y - y + dx/dy * player1_x + dy/dx * x)/(m_data + 1./m_data)
                y_collision = (player1_x - x + dy/dx * player1_y + dx/dy * y)/(m_data + 1./m_data)
                # dis_PL = abs(dy*player1_x - dx*player1_y + dx*y - dy*x)/(dy**2 + dx**2)*0.5
                safe_dist = ((x_collision - x)**2+(y_collision - y)**2)**0.5
                # check safety
                if safe_dist < 0.001:
                    speed = 0.
                    continue
                else:
                    speed = 1.0
                    # bullet will hit the left-down sidee
                    if x_collision < player1_x and y_collision < player1_y :
                        angle = np.arctan2(abs(player1_y-y_collision),abs(player1_x-x_collision))
                    # bullet will hit the right-down side
                    elif x_collision >= player1_x and y_collision < player1_y :
                        angle = np.arctan2(abs(player1_y-y_collision),player1_x-x_collision)
                    # bullet will hit the left-up side
                    elif x_collision < player1_x and y_collision >= player1_y :
                        angle = np.arctan2((player1_y-y_collision),abs(player1_x-x_collision))
                    # bullet will hit the right-up side
                    else :
                        angle = np.arctan2((player1_y-y_collision),(player1_x-x_collision))
                    break

            # eating weapon
            if type == 8 and player1_weapon <= 5:
                if abs(player1_x - x) >= 0.3 and abs(player1_y - y) < 0.4:
                    if player1_y < player2_y and player1_y < 0.4:
                        speed = ((x - player1_x)**2 + (y - player1_y)**2)**0.5
                        speed /= 0.01 # since the maximum speed is 0.01 unit per frame
                        if speed>1.: speed = 1.
                        angle = np.arctan2(y-player1_y,x-player1_x)
                        break
                    elif player1_y > y:
                        speed = 1.0
                        angle = np.arctan2(y-player1_y,x-player1_x)
                        break
                    else:
                        speed = 1.0
                        if x>player1_x: angle = 0.    # run to right
                        if x<player1_x: angle = np.pi # run to left
                        break
                elif 0.3 > abs(player1_x - x) >= 0. and abs(player1_y - y) < 0.1:
                    if player1_y < player2_y and player1_y < 0.4:
                        speed = 1.0
                        speed = ((x - player1_x)**2 + (y - player1_y)**2)**0.5
                        speed /= 0.01 # since the maximum speed is 0.01 unit per frame
                        if speed>1.: speed = 1.
                        angle = np.arctan2(y-player1_y,x-player1_x)
                        break
                    elif player1_y > y:
                        speed = 1.0
                        angle = np.arctan2(y-player1_y,x-player1_x)
                        break
                    else:
                        speed = 1.0
                        if x>player1_x: angle = 0.    # run to right
                        if x<player1_x: angle = np.pi # run to left
                        break

            # eating rescuecap
            if type == 7 and player1_hp < 12:
                if abs(player1_x - x) >= 0.4 and abs(player1_y - y) < 0.4:
                    if player1_y < player2_y and player1_y < 0.4 and player1_y < y:
                        speed = ((x - player1_x)**2 + (y - player1_y)**2)**0.5
                        speed /= 0.01 # since the maximum speed is 0.01 unit per frame
                        if speed>1.: speed = 1.
                        angle = np.arctan2(y-player1_y,x-player1_x)
                        break
                    elif player1_y > y:
                        speed = 1.
                        angle = np.arctan2(y-player1_y,x-player1_x)
                        break
                    else:
                        speed = 1.0
                        if x>player1_x: angle = 0.    # run to right
                        if x<player1_x: angle = np.pi # run to left
                        break

                elif 0.4 >= abs(player1_x - x) >= 0. and abs(player1_y - y) < 0.1:
                    if player1_y < player2_y and player1_y < 0.4:
                        speed = 1.0
                        speed = ((x - player1_x)**2 + (y - player1_y)**2)**0.5
                        speed /= 0.01 # since the maximum speed is 0.01 unit per frame
                        if speed>1.: speed = 1.
                        angle = np.arctan2(y-player1_y,x-player1_x)
                        break
                    elif player1_y > y:
                        speed = 1.0
                        angle = np.arctan2(y-player1_y,x-player1_x)
                        break
                    else:
                        speed = 1.0
                        if x>player1_x: angle = 0.    # run to right
                        if x<player1_x: angle = np.pi # run to left
                        break
            #################################################
            #####          attacking enemy Strategy
            #################################################

            # if boss comming

            if type in boss :
                speed = abs(x-player1_x)
                speed /= 0.01
                if speed > 1.: speed = 1.
                if player1_y >= 0.23:
                    if x>player1_x: angle = np.arctan2(-0.4,1.)    # escape to right
                    if x<player1_x: angle = np.arctan2(-0.4,-1) # escape to left
                elif player1_y < 0.17:
                    if x>player1_x: angle = np.arctan2(0.4,1.)    # escape to right
                    if x<player1_x: angle = np.arctan2(0.4,-1.) # escape to left
                else:
                    if abs(x - player1_x) <= 0.01 and player1_y < 0.3:
                        speed = 0
                    speed = 0.5
                    if x>player1_x: angle = 0.    # escape to right
                    if x<player1_x: angle = np.pi # escape to left
                continue


            # if there is an enemy and is close enough, attack it
            if type!=7 and type!=8 and dist >= 0.25 and dist < 0.9:
                speed = abs(x-player1_x)
                speed /= 0.01
                if speed > 1.: speed = 1.
                if player1_y >= 0.22:
                    if x>player1_x: angle = np.arctan2(-0.4,1.)    # escape to right
                    if x<player1_x: angle = np.arctan2(-0.4,-1) # escape to left
                elif player1_y < 0.18:
                    if x>player1_x: angle = np.arctan2(0.4,1.)    # escape to right
                    if x<player1_x: angle = np.arctan2(0.4,-1.) # escape to left
                else:
                    speed = 0.6
                    if x>player1_x: angle = 0.    # escape to right
                    if x<player1_x: angle = np.pi # escape to left
                continue

        return speed, angle
