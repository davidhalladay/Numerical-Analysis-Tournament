import numpy as np

class player_module:

    # constructor, allocate any private date here
    def __init__(self):
        self.init_x, self.init_y = -1., -1.

    # Please update the banner according to your information
    def banner(self):
        print('-'*40)
        print('Author: your_name_here')
        print('ID: bxxxxxxxx')
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
            type = data[0] # 0 - bullet, 1..4 - different types of invaders, 5 - ufo, 6 - boss, 7 - rescuecap, 8 - weaponup
            x    = data[1]
            y    = data[2]
            dx   = data[3] # expected movement in x direction for the next frame
            dy   = data[4] # expected movement in y direction for the next frame
            boss = [6]
            # calculate the distance toward player1
            dist = ((x-player1_x)**2+(y-player1_y)**2)**0.5

            # if the boss is too close
            if type == 8 and dist < 0.25:
                speed = 1.0
                if x<player1_x: angle = 0.    # escape to right
                if x>player1_x: angle = np.pi # escape to left
                break

            if (type in [0,4]) and type != 6 and dist < 0.212:
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
                    if player1_x > 0.005 or player1_x < 0.995:
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
                    else:
                        # bullet will hit the left-down sidee
                        if x_collision < player1_x and y_collision < player1_y :
                            angle = np.pi/2.
                        # bullet will hit the right-down side
                        elif x_collision >= player1_x and y_collision < player1_y :
                            angle = np.pi/2.
                        # bullet will hit the left-up side
                        elif x_collision < player1_x and y_collision >= player1_y :
                            angle = 3*np.pi/2.
                        # bullet will hit the right-up side
                        else :
                            angle = 3*np.pi/2.
                        break
            # boss Strategy
            if (type == 0) and type == 6 and dist < 0.212:
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

            if type == 8 and player1_weapon <= 4:
                if abs(player1_x - x) >= 0.3 and abs(player1_y - y) < 0.4:
                    if player1_y < player2_y and player1_y < 0.4:
                        speed = 1.0
                        if x>player1_x: angle = np.arctan2(1,1)  # run to right
                        if x<player1_x: angle = np.arctan2(1,-1) # run to left
                        break
                    else:
                        speed = 1.0
                        if x>player1_x: angle = 0.    # run to right
                        if x<player1_x: angle = np.pi # run to left
                        break
                elif 0.3 > abs(player1_x - x) >= 0. and abs(player1_y - y) < 0.1:
                    if player1_y < player2_y and player1_y < 0.4:
                        speed = 1.0
                        if x>player1_x: angle = np.arctan2(1,1)    # run to right
                        if x<player1_x: angle = np.arctan2(1,-1) # run to left
                        break
                    else:
                        speed = 1.0
                        if x>player1_x: angle = 0.    # run to right
                        if x<player1_x: angle = np.pi # run to left
                        break

            # eating rescuecap
            if type == 7 and player1_hp < 12:
                if abs(player1_x - x) >= 0.4 and abs(player1_y - y) < 0.4:
                    if player1_y < player2_y and player1_y < 0.4:
                        speed = 1.0
                        if x>player1_x: angle = np.arctan2(1,1)    # run to right
                        if x<player1_x: angle = np.arctan2(1,-1) # run to left
                        break
                    else:
                        speed = 1.0
                        if x>player1_x: angle = 0.    # run to right
                        if x<player1_x: angle = np.pi # run to left
                        break

                elif abs(player1_x - x) >= 0. and abs(player1_y - y) < 0.1:
                    if player1_y < player2_y and player1_y < 0.4:
                        speed = 1.0
                        if x>player1_x: angle = np.arctan2(1,1)    # run to right
                        if x<player1_x: angle = np.arctan2(1,-1) # run to left
                        break
                    else:
                        speed = 1.0
                        if x>player1_x: angle = 0.    # run to right
                        if x<player1_x: angle = np.pi # run to left
                        break

            # if boss comming
            if type in boss :
                speed = abs(x-player1_x)
                speed /= 0.01
                if speed>1.: speed = 1.
                if player1_y > 0.2:
                    if x>player1_x: angle = np.arctan2(-0.1,1.)    # escape to right
                    if x<player1_x: angle = np.arctan2(-0.1,-1) # escape to left
                else:
                    if x>player1_x: angle = np.arctan2(0.1,1.)    # escape to right
                    if x<player1_x: angle = np.arctan2(0.1,-1.) # escape to left
                continue

            # if there is an enemy and is close enough, attack it
            if type!=7 and type!=8 and dist >= 0.25 and dist < 0.9:
                speed = abs(x-player1_x)
                speed /= 0.01
                if speed>1.: speed = 1.
                if player1_y > 0.2:
                    if x>player1_x: angle = np.arctan2(-0.1,1.)    # escape to right
                    if x<player1_x: angle = np.arctan2(-0.1,-1) # escape to left
                else:
                    if x>player1_x: angle = np.arctan2(0.1,1.)    # escape to right
                    if x<player1_x: angle = np.arctan2(0.1,-1.) # escape to left
                continue

            # if the enemy is too close
            if type!=7 and type!=8 and dist < 0.25:
                speed = 1.0
                if x<player1_x: angle = 0.    # escape to right
                if x>player1_x: angle = np.pi # escape to left
                break

        return speed, angle
