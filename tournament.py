import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.animation as animation

import hw3 as P1
import player_teacher as P2

print('Imported Player 1:')
player1 = P1.player_module()
player1.banner()

print('Imported Player 2:')
player2 = P2.player_module()
player2.banner()

# initial all graphical objects
fig = plt.figure(figsize=(6,7), dpi=80)
ax = plt.axes(xlim=(-0.1,+1.1), ylim=(-0.2,+1.2))

marker_scale = 2

# tool for converting the 2d bitmaps to matplotlib paths
def create_path_from_array(bitmap):
    verts = []
    codes = []
    dx = 2./bitmap.shape[1]
    dy = 2./bitmap.shape[0]

    for j in range(bitmap.shape[0]):
        for i in range(bitmap.shape[1]):

            if bitmap[bitmap.shape[0]-j-1,i]==1: # full square
                verts += [(dx*(i+0)-1., dy*(j+0)-1.), # left, bottom
                          (dx*(i+0)-1., dy*(j+1)-1.), # left, top
                          (dx*(i+1)-1., dy*(j+1)-1.), # right, top
                          (dx*(i+1)-1., dy*(j+0)-1.), # right, bottom
                          (dx*(i+0)-1., dy*(j+0)-1.)]
                codes += [mpath.Path.MOVETO,
                          mpath.Path.LINETO,
                          mpath.Path.LINETO,
                          mpath.Path.LINETO,
                          mpath.Path.CLOSEPOLY]

            if bitmap[bitmap.shape[0]-j-1,i]==2: # triangle toward left-bottom
                verts += [(dx*(i+0)-1., dy*(j+0)-1.), # left, bottom
                          (dx*(i+0)-1., dy*(j+1)-1.), # left, top
                          (dx*(i+1)-1., dy*(j+0)-1.), # right, bottom
                          (dx*(i+0)-1., dy*(j+0)-1.)]
                codes += [mpath.Path.MOVETO,
                          mpath.Path.LINETO,
                          mpath.Path.LINETO,
                          mpath.Path.CLOSEPOLY]

            if bitmap[bitmap.shape[0]-j-1,i]==3: # triangle toward right-bottom
                verts += [(dx*(i+0)-1., dy*(j+0)-1.), # left, bottom
                          (dx*(i+1)-1., dy*(j+1)-1.), # right, top
                          (dx*(i+1)-1., dy*(j+0)-1.), # right, bottom
                          (dx*(i+0)-1., dy*(j+0)-1.)]
                codes += [mpath.Path.MOVETO,
                          mpath.Path.LINETO,
                          mpath.Path.LINETO,
                          mpath.Path.CLOSEPOLY]

            if bitmap[bitmap.shape[0]-j-1,i]==4: # triangle toward right-top
                verts += [(dx*(i+0)-1., dy*(j+1)-1.), # left, top
                          (dx*(i+1)-1., dy*(j+1)-1.), # right, top
                          (dx*(i+1)-1., dy*(j+0)-1.), # right, bottom
                          (dx*(i+0)-1., dy*(j+1)-1.)]
                codes += [mpath.Path.MOVETO,
                          mpath.Path.LINETO,
                          mpath.Path.LINETO,
                          mpath.Path.CLOSEPOLY]

            if bitmap[bitmap.shape[0]-j-1,i]==5: # triangle toward left-top
                verts += [(dx*(i+0)-1., dy*(j+0)-1.), # left, bottom
                          (dx*(i+0)-1., dy*(j+1)-1.), # left, top
                          (dx*(i+1)-1., dy*(j+1)-1.), # right, top
                          (dx*(i+0)-1., dy*(j+0)-1.)]
                codes += [mpath.Path.MOVETO,
                          mpath.Path.LINETO,
                          mpath.Path.LINETO,
                          mpath.Path.CLOSEPOLY]

    return mpath.Path(verts, codes)

# bitmaps for invaders, ufo, and the players
bitmap_invader1 = np.array([[0,4,2,0,0,0,0,0,3,5,0],
                            [0,0,4,2,0,0,0,3,5,0,0],
                            [0,3,1,1,1,1,1,1,1,2,0],
                            [3,1,1,0,1,1,1,0,1,1,2],
                            [1,1,1,1,1,1,1,1,1,1,1],
                            [1,0,1,1,1,1,1,1,1,0,1],
                            [1,0,1,0,0,0,0,0,1,0,1],
                            [0,0,4,1,1,0,1,1,5,0,0]])

bitmap_invader2 = np.array([[0,0,1,2,0,0,0,3,1,0,0],
                            [1,0,0,1,0,0,0,1,0,0,1],
                            [1,3,1,1,1,1,1,1,1,2,1],
                            [1,1,1,0,1,1,1,0,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1,1],
                            [4,1,1,1,1,1,1,1,1,1,5],
                            [0,0,3,1,5,0,4,1,2,0,0],
                            [3,1,5,0,0,0,0,0,4,1,2]])

bitmap_invader3 = np.array([[0,0,0,3,1,1,1,1,2,0,0,0],
                            [3,1,1,1,1,1,1,1,1,1,1,2],
                            [1,1,1,1,1,1,1,1,1,1,1,1],
                            [1,1,2,0,4,1,1,5,0,3,1,1],
                            [1,1,1,1,1,1,1,1,1,1,1,1],
                            [0,0,3,1,1,0,0,1,1,2,0,0],
                            [0,3,1,5,4,1,1,5,4,1,2,0],
                            [1,1,5,0,0,0,0,0,0,4,1,1]])

bitmap_invader4 = np.array([[0,0,0,3,1,1,2,0,0,0],
                            [0,0,3,1,1,1,1,2,0,0],
                            [0,3,1,1,1,1,1,1,2,0],
                            [3,1,1,0,1,1,0,1,1,2],
                            [4,1,1,1,1,1,1,1,1,5],
                            [0,0,3,1,2,3,1,2,0,0],
                            [0,3,5,0,1,1,0,4,2,0],
                            [3,5,3,1,5,4,1,2,4,2]])

bitmap_ufo      = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,3,1,1,1,1,1,1,2,0,0,0,0],
                            [0,0,3,1,1,1,1,1,1,1,1,1,1,2,0,0],
                            [0,3,1,1,1,1,1,1,1,1,1,1,1,1,2,0],
                            [3,1,1,0,1,1,0,1,1,0,1,1,0,1,1,2],
                            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                            [0,4,1,1,1,5,4,1,1,5,4,1,1,1,5,0],
                            [0,0,4,1,5,0,0,0,0,0,0,4,1,5,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

bitmap_superufo = np.array([[0,2,0,0,0,0,0,3,1,1,1,1,2,0,0,0,0,0,3,0],
                            [0,1,2,0,3,1,1,1,1,1,1,1,1,1,1,2,0,3,1,0],
                            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
                            [0,3,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,1,2,0],
                            [3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
                            [1,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,1],
                            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                            [1,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,1],
                            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                            [5,4,1,0,1,5,4,1,1,5,4,1,1,5,4,1,0,1,5,4],
                            [0,0,4,0,5,0,0,4,5,0,0,4,5,0,0,4,0,5,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])


bitmap_player1  = np.array([[3,5,0,0,3,1,2,0,0,4,2],
                            [1,0,0,0,1,1,1,0,0,0,1],
                            [1,0,0,3,1,1,1,2,0,0,1],
                            [1,0,0,1,1,1,1,1,0,0,1],
                            [1,1,1,1,1,0,1,1,1,1,1],
                            [1,0,0,1,1,0,1,1,0,0,1],
                            [1,1,1,1,1,1,1,1,1,1,1],
                            [1,0,0,4,1,1,1,5,0,0,1],
                            [4,1,2,0,0,0,0,0,3,1,5]])

bitmap_player2  = np.array([[3,5,0,0,3,1,2,0,0,4,2],
                            [1,0,0,0,1,1,1,0,0,0,1],
                            [1,0,0,3,1,1,1,2,0,0,1],
                            [1,0,0,1,1,1,1,1,0,0,1],
                            [1,1,1,1,0,1,0,1,1,1,1],
                            [1,0,0,1,0,1,0,1,0,0,1],
                            [1,1,1,1,1,1,1,1,1,1,1],
                            [1,0,0,4,1,1,1,5,0,0,1],
                            [4,1,2,0,0,0,0,0,3,1,5]])

bitmap_rescuecap = np.array([[0,0,0,3,1,1,2,0,0,0],
                             [0,0,3,1,0,0,1,2,0,0],
                             [0,3,1,1,0,0,1,1,2,0],
                             [3,1,0,0,0,0,0,0,1,2],
                             [4,1,0,0,0,0,0,0,1,5],
                             [0,4,1,1,0,0,1,1,5,0],
                             [0,0,4,1,0,0,1,5,0,0],
                             [0,0,0,4,1,1,5,0,0,0]])

bitmap_weaponup = np.array([[3,1,1,1,1,1,1,1,1,2],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,0,0,1,0,0,1,0,0,1],
                            [1,0,0,1,0,0,1,0,0,1],
                            [1,2,0,0,0,0,0,0,3,1],
                            [1,1,0,0,1,1,0,0,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [4,1,1,1,1,1,1,1,1,5]])

# now create the paths
path_invader1  = create_path_from_array(bitmap_invader1)
path_invader2  = create_path_from_array(bitmap_invader2)
path_invader3  = create_path_from_array(bitmap_invader3)
path_invader4  = create_path_from_array(bitmap_invader4)
path_ufo       = create_path_from_array(bitmap_ufo)
path_superufo  = create_path_from_array(bitmap_superufo)
path_player1   = create_path_from_array(bitmap_player1)
path_player2   = create_path_from_array(bitmap_player2)
path_rescuecap = create_path_from_array(bitmap_rescuecap)
path_weaponup  = create_path_from_array(bitmap_weaponup)

# create drawable objects (static)
ax.plot([-0.05,0.35],[-0.15,-0.15],lw=9,color='0.1')
ax.plot([-0.05,0.35],[-0.15,-0.15],lw=7,color='#FFFFF0')
ax.plot([+0.65,+1.05],[-0.15,-0.15],lw=9,color='0.1')
ax.plot([+0.65,+1.05],[-0.15,-0.15],lw=7,color='#FFFFF0')

# create drawable objects (non-static)
plt_invader1,  = ax.plot([], [], marker=path_invader1,  ms = 7*marker_scale, mec='#900000', mfc='#F00000', ls='None', alpha=0.6)
plt_invader2,  = ax.plot([], [], marker=path_invader2,  ms = 7*marker_scale, mec='#904000', mfc='#F09000', ls='None', alpha=0.6)
plt_invader3,  = ax.plot([], [], marker=path_invader3,  ms = 7*marker_scale, mec='#909000', mfc='#F0F000', ls='None', alpha=0.6)
plt_invader4,  = ax.plot([], [], marker=path_invader4,  ms = 7*marker_scale, mec='#309000', mfc='#60F000', ls='None', alpha=0.6)
plt_ufo,       = ax.plot([], [], marker=path_ufo,       ms =14*marker_scale, mec='#600090', mfc='#9000F0', ls='None', alpha=0.8)
plt_superufo,  = ax.plot([], [], marker=path_superufo,  ms =56*marker_scale, mec='#600030', mfc='#C00060', ls='None', alpha=0.8)
plt_player1,   = ax.plot([], [], marker=path_player1,   ms =14*marker_scale, mec='#002090', mfc='#0040F0', ls='None', alpha=0.8)
plt_player2,   = ax.plot([], [], marker=path_player2,   ms =14*marker_scale, mec='#007080', mfc='#00A0C0', ls='None', alpha=0.8)
plt_rescuecap, = ax.plot([], [], marker=path_rescuecap, ms = 7*marker_scale, mec='#F06060', mfc='#F09090', ls='None', alpha=0.8)
plt_weaponup,  = ax.plot([], [], marker=path_weaponup,  ms = 7*marker_scale, mec='#606060', mfc='#909090', ls='None', alpha=0.8)

plt_explosion,  = ax.plot([], [], marker=(10,1,0), ms = 21*marker_scale, mec='#FF0000', mfc='#FFA000', ls='None', alpha=0.8)
plt_bullet_inv, = ax.plot([], [], marker='o', ms = 3*marker_scale, mec='#FF0000', mfc='#FF0000',  ls='None', alpha=0.6)
plt_bullet_ply, = ax.plot([], [], marker='d', ms = 3*marker_scale, mec='#0000FF', mfc='#0000FF',  ls='None', alpha=0.6)

plt_tx_center = ax.text(0.5,0.5, '', fontsize = 40, color='#60A0C0', ha='center', va='center')
plt_tx_p1 = ax.text(-0.05,1.13, '', fontsize = 14, color='#B06020', ha='left', va='center')
plt_tx_p2 = ax.text(+1.05,1.13, '', fontsize = 14, color='#B06020', ha='right', va='center')
plt_tx_p1_hp = ax.text(-0.05,-.10, '', fontsize = 10, color='#002090', ha='left', va='center')
plt_tx_p2_hp = ax.text(+1.05,-.10, '', fontsize = 10, color='#007080', ha='right', va='center')

plt_gauge_p1, = ax.plot([],[],lw=7,color='#80D070')
plt_gauge_p2, = ax.plot([],[],lw=7,color='#80D070')
plt_gauge_attack_p1, = ax.plot([],[],lw=4,color='#FFAA00')
plt_gauge_attack_p2, = ax.plot([],[],lw=4,color='#FFAA00')

reference_speed = 0.01 # 0.01 per frame

# class for bullets, invaders, players, etc
class sprite:
    def __init__(self, x_init = 0.5, y_init = 1.2):

        self.x, self.y = x_init, y_init # current position
        self.speed = reference_speed # speed
        self.angle = np.pi*3./2. # direction
        self.hp = 1 # hit points
        self.charge = 0 # frames before shooting
        self.dx = 0.
        self.dy = 0.
        self.enabled = True

        self.type = 1 # 0 - bullet, [1..4] - invader[1..4], 5 - ufo/player1/2, 6 - superufo, 7 - rescurecap
        self.path = 1 # 0 - user controlled, 1 - straight, 2 - curly, 3 - tracing player1, 4 - tracing player2, 5 - random walk, 6 - up-down
        self.pathpar = 0. # parameter for path moving

    def eval_displacement(self): # evaluate the movement toward the next frame
        global sp_player1, sp_player2

        if self.path==2:
            self.angle += self.pathpar
        if self.path==3:
            if  sp_player1.enabled:
                self.angle = np.arctan2(sp_player1.y-self.y, sp_player1.x-self.x)
            elif sp_player2.enabled:
                self.angle = np.arctan2(sp_player2.y-self.y, sp_player2.x-self.x)
        if self.path==4:
            if sp_player2.enabled:
                self.angle = np.arctan2(sp_player2.y-self.y, sp_player2.x-self.x)
            elif sp_player1.enabled:
                self.angle = np.arctan2(sp_player1.y-self.y, sp_player1.x-self.x)
        if self.path==5:
            self.angle += (np.random.rand(1)[0]-0.5)*np.pi/6.
        if self.path==6:
            if self.angle>np.pi and self.y<0.35: self.angle = np.pi*0.5
            if self.angle<np.pi and self.y>0.95: self.angle = np.pi*1.5

        self.dx = (self.speed)*np.cos(self.angle)
        self.dy = (self.speed)*np.sin(self.angle)

    def move(self): # actual move the sprite
        self.x += self.dx
        self.y += self.dy

    def eval_collision(self, obj): # collision detection, only consider the center of obj hitting the square box from self center
        l = 0.025
        if self.type==5: l = 0.05
        if self.type==6: l = 0.20

        if abs(obj.x-self.x)<l and abs(obj.y-self.y)<l: return True
        if abs(obj.x-self.x + (obj.dx-self.dx))<l and abs(obj.y-self.y + (obj.dy-self.dy))<l: return True

        if obj.dx!=self.dx:
            t = (self.x-obj.x+l)/(obj.dx-self.dx)
            if t>0. and t<1.:
                osy = obj.y-self.y + (obj.dy-self.dy) * t
                if abs(osy)<l: return True
            t = (self.x-obj.x-l)/(obj.dx-self.dx)
            if t>0. and t<1.:
                osy = obj.y-self.y + (obj.dy-self.dy) * t
                if abs(osy)<l: return True

        if obj.dy!=self.dy:
            t = (self.y-obj.y+l)/(obj.dy-self.dy)
            if t>0. and t<1.:
                osx = obj.x-self.x + (obj.dx-self.dx) * t
                if abs(osx)<l: return True
            t = (self.y-obj.y-l)/(obj.dy-self.dy)
            if t>0. and t<1.:
                osx = obj.x-self.x + (obj.dx-self.dx) * t
                if abs(osx)<l: return True

        return False

# sprites for player 1 and 2
sp_player1 = sprite(0.25,0.2)
sp_player1.type = 5
sp_player1.path = 0
sp_player1.hp = 10
sp_player2 = sprite(0.75,0.2)
sp_player2.type = 5
sp_player2.path = 0
sp_player2.hp = 10

# additional information for players
sp_player1.score = 0
sp_player2.score = 0
sp_player1.gauge = 1.
sp_player2.gauge = 1.
sp_player1.weapon = 1
sp_player2.weapon = 1
sp_player1.charge2 = 0
sp_player2.charge2 = 0
sp_player1.gauge_attack = 0
sp_player2.gauge_attack = 0
sp_player1.gauge_freeze = 0
sp_player2.gauge_freeze = 0

# sprite holders
splist_invader = []
splist_bullet_inv = []
splist_bullet_ply1 = []
splist_bullet_ply2 = []
splist_explosion = []

invader_level = 1   # start with level 1
invader_fcount = 0  # counts of frames for adding new invader
invader_boss = 0    # add boss!
center_message = ''
center_message_delay = 0
center_message_blink = 0

def init():
    plt_invader1.set_data([], [])
    plt_invader2.set_data([], [])
    plt_invader3.set_data([], [])
    plt_invader4.set_data([], [])
    plt_ufo.set_data([], [])
    plt_player1.set_data([], [])
    plt_player2.set_data([], [])
    plt_explosion.set_data([], [])
    plt_bullet_inv.set_data([], [])
    plt_bullet_ply.set_data([], [])

    plt_tx_center.set(text='')
    plt_tx_p1.set(text='P1 ')
    plt_tx_p2.set(text=' P2')
    plt_tx_p1_hp.set(text='HP ')
    plt_tx_p2_hp.set(text=' HP')
    plt_gauge_p1.set_data([], [])
    plt_gauge_p2.set_data([], [])
    plt_gauge_attack_p1.set_data([], [])
    plt_gauge_attack_p2.set_data([], [])

    return plt_invader1, plt_invader2, plt_invader3, plt_invader4, plt_ufo, plt_player1, plt_player2, plt_rescuecap, plt_weaponup, plt_explosion, plt_bullet_inv, plt_bullet_ply, plt_tx_center, plt_tx_p1, plt_tx_p2, plt_tx_p1_hp, plt_tx_p2_hp, plt_gauge_p1, plt_gauge_p2, plt_gauge_attack_p1, plt_gauge_attack_p2

def animate(i):
    global invader_fcount, invader_level, invader_boss
    global center_message, center_message_delay, center_message_blink

    if i<30: # display the initial message
        plt_tx_center.set(text='Ready?')

        plt_player1.set_data([sp_player1.x],[sp_player1.y])
        plt_player2.set_data([sp_player2.x],[sp_player2.y])

        return plt_invader1, plt_invader2, plt_invader3, plt_invader4, plt_ufo, plt_player1, plt_player2, plt_rescuecap, plt_weaponup, plt_explosion, plt_bullet_inv, plt_bullet_ply, plt_tx_center, plt_tx_p1, plt_tx_p2, plt_tx_p1_hp, plt_tx_p2_hp, plt_gauge_p1, plt_gauge_p2, plt_gauge_attack_p1, plt_gauge_attack_p2
    elif i==30:
        center_message = 'Go!'
        center_message_delay = 30

    if invader_boss>0: # boss mode

        if invader_boss==1: # add new boss

            sp = sprite()
            sp.type = 6
            sp.path = 6
            sp.hp = 60+60*invader_level
            sp.x = 0.5
            sp.y = 1.35
            sp.angle = np.pi*1.5
            sp.speed *= 0.1

            splist_invader.append(sp)
            invader_boss=2

    elif invader_fcount==0: # add new invaders

        sp = sprite()
        choice = np.random.randint(100)
        if choice==0 or choice==1: # rescuecap or weapon
            sp.type = 7+choice
            sp.path = 1
            sp.angle = -np.pi*0.5
            sp.speed *= 0.2
            sp.x = np.random.rand(1)[0]*0.8+0.1
        elif choice==2 or choice==3: # ufo
            sp.type = 5
            sp.path = 1
            sp.hp = 5
            if np.random.randint(2)==0:
                sp.x = -0.1
                sp.y = 0.8+np.random.rand(1)[0]*0.2
                sp.angle = 0.
                sp.speed *= 0.2
            else:
                sp.x = +1.1
                sp.y = 0.8+np.random.rand(1)[0]*0.2
                sp.angle = np.pi
                sp.speed *= 0.2
        else: # others
            sp.type = np.random.randint(1,5)
            if sp.type==1:
                sp.path = 1
                sp.speed *= 0.75
            if sp.type==2:
                sp.path = 2
                sp.pathpar = (np.random.rand(1)[0]-0.5)*np.pi/6./10.
                sp.speed *= 0.75
            if sp.type==3:
                sp.path = np.random.randint(3,5)
                sp.speed *= (0.3+0.08*(invader_level-1))
            if sp.type==4:
                sp.path = 5
                sp.speed *= 0.75

            sp.x = np.random.rand(1)[0]
            if sp.x<0.5: sp.angle = np.pi*3./2. + (np.random.rand(1)[0])*np.pi/4.
            else:        sp.angle = np.pi*3./2. - (np.random.rand(1)[0])*np.pi/4.

        splist_invader.append(sp)
        invader_fcount += 1
    else:
        invader_fcount += 1
        if invader_fcount>=12-invader_level: invader_fcount = 0

    # shoot bullets from invader
    for sp in splist_invader:
        if sp.type==7 or sp.type==8: continue # skip the rescuecap/weaponup
        if sp.charge>=160-invader_level*11 and sp.x<1. and sp.x>0. and sp.y<1. and sp.y>0. and np.random.randint(4)==1:
            sp.charge = 0
            bullet = sprite(sp.x,sp.y)
            bullet.speed *= 2.
            bullet.type = 0
            bullet.path = 1
            if np.random.randint(2)==0:
                if sp_player1.enabled:
                    bullet.angle = np.arctan2(sp_player1.y-sp.y, sp_player1.x-sp.x)
                else:
                    bullet.angle = np.arctan2(sp_player2.y-sp.y, sp_player2.x-sp.x)
            else:
                if sp_player2.enabled:
                    bullet.angle = np.arctan2(sp_player2.y-sp.y, sp_player2.x-sp.x)
                else:
                    bullet.angle = np.arctan2(sp_player1.y-sp.y, sp_player1.x-sp.x)
            splist_bullet_inv.append(bullet)
        else:
            if sp.type==5: sp.charge += 2
            elif sp.type==6: sp.charge += 8
            elif sp.type!=3 and sp.type!=4: sp.charge += 1

    # shoot bullets from players
    for ply,bltlist in [[sp_player1,splist_bullet_ply1],[sp_player2,splist_bullet_ply2]]:
        if ply.enabled and ply.weapon>=1:
            if ply.charge>=8:
                ply.charge = 0
                bullet = sprite(ply.x,ply.y)
                bullet.speed *= 4.
                bullet.type = 0
                bullet.path = 1
                bullet.angle = np.pi/2.
                bltlist.append(bullet)
            else:
                ply.charge += 1
        if ply.enabled and ply.weapon>=2:
            if ply.charge2>=8+(3-ply.weapon)*8:
                ply.charge2 = 0
                blt1,blt2 = sprite(ply.x,ply.y),sprite(ply.x,ply.y)
                blt1.speed *= 4.
                blt2.speed *= 4.
                blt1.type,blt2.type = 0,0
                blt1.path,blt2.path = 1,1
                blt1.angle,blt2.angle = np.pi/2.-np.pi/12,np.pi/2.+np.pi/12
                bltlist.append(blt1)
                bltlist.append(blt2)
            else:
                ply.charge2 += 1

    # evaluate all of the displacements
    enemy_data = []

    for sp in splist_invader:
        sp.eval_displacement()
        enemy_data.append((sp.type,sp.x,sp.y,sp.dx,sp.dy))

    for sp in splist_bullet_inv:
        sp.eval_displacement()
        enemy_data.append((sp.type,sp.x,sp.y,sp.dx,sp.dy))

    for sp in splist_bullet_ply1:
        sp.eval_displacement()

    for sp in splist_bullet_ply2:
        sp.eval_displacement()

    # decision for players

    if sp_player1.enabled:

        player_data = []
        player_data.append((sp_player1.x,sp_player1.y,sp_player1.hp,sp_player1.score,sp_player1.gauge,sp_player1.weapon))
        player_data.append((sp_player2.x,sp_player2.y,sp_player2.hp,sp_player2.score,sp_player2.gauge,sp_player2.weapon))

        ret = player1.decision(player_data,enemy_data)

        # check ret is valid or not
        if type((1.,2.))!=type(()) or len(ret)!=2 or (not np.isfinite(ret[0])) or (not np.isfinite(ret[1])):
            print('player1 invalid return:',ret)
            ret = (0.,0.)

        sp_player1.speed = ret[0]*reference_speed
        if sp_player1.speed<0.: sp_player1.speed = 0.
        if sp_player1.speed>reference_speed: sp_player1.speed = reference_speed
        sp_player1.angle = ret[1]

        if sp_player1.gauge_freeze>0:
            sp_player1.speed = reference_speed
            sp_player1.angle = np.pi*(sp_player1.gauge_freeze%2)
            sp_player1.gauge_freeze-=1

        if sp_player1.gauge_attack==0:
            sp_player1.gauge += (reference_speed-sp_player1.speed)/reference_speed*4.
            if sp_player1.gauge>=1000.:
                sp_player1.gauge = 1.
                sp_player1.gauge_attack = 10
        else:
            sp_player1.gauge_attack -= 1

        sp_player1.dx = (sp_player1.speed)*np.cos(sp_player1.angle)
        sp_player1.dy = (sp_player1.speed)*np.sin(sp_player1.angle)

    if sp_player2.enabled:

        player_data = []
        player_data.append((sp_player2.x,sp_player2.y,sp_player2.hp,sp_player2.score,sp_player2.gauge,sp_player2.weapon))
        player_data.append((sp_player1.x,sp_player1.y,sp_player1.hp,sp_player1.score,sp_player1.gauge,sp_player1.weapon))

        ret = player2.decision(player_data,enemy_data)

        # check ret is valid or not
        if type((1.,2.))!=type(()) or len(ret)!=2 or (not np.isfinite(ret[0])) or (not np.isfinite(ret[1])):
            print('player2 invalid return:',ret)
            ret = (0.,0.)

        sp_player2.speed = ret[0]*reference_speed
        if sp_player2.speed<0.: sp_player2.speed = 0.
        if sp_player2.speed>reference_speed: sp_player2.speed = reference_speed
        sp_player2.angle = ret[1]

        if sp_player2.gauge_freeze>0:
            sp_player2.speed = reference_speed
            sp_player2.angle = np.pi*(sp_player2.gauge_freeze%2)
            sp_player2.gauge_freeze-=1

        if sp_player2.gauge_attack==0:
            sp_player2.gauge += (reference_speed-sp_player2.speed)/reference_speed*4.
            if sp_player2.gauge>=1000.:
                sp_player2.gauge = 1.
                sp_player2.gauge_attack = 10
        else:
            sp_player2.gauge_attack -= 1

        sp_player2.dx = (sp_player2.speed)*np.cos(sp_player2.angle)
        sp_player2.dy = (sp_player2.speed)*np.sin(sp_player2.angle)

    # loop over all bullets from players, check if it hits the invaders
    for sp in splist_bullet_ply1:
        for target in splist_invader:
            if target.type==7 or target.type==8: continue # skip rescuecap/weaponup
            if target.eval_collision(sp):
                target.hp -= 1
                sp.hp -= 1
                if target.type==1 or target.type==2 or target.type==6: sp_player1.score += 10
                if target.type==3 or target.type==4: sp_player1.score += 15
                if target.type==5: sp_player1.score += 20
    for sp in splist_bullet_ply2:
        for target in splist_invader:
            if target.type==7 or target.type==8: continue # skip rescuecap/weaponup
            if target.eval_collision(sp):
                target.hp -= 1
                sp.hp -= 1
                if target.type==1 or target.type==2 or target.type==6: sp_player2.score += 10
                if target.type==3 or target.type==4: sp_player2.score += 15
                if target.type==5: sp_player2.score += 20

    # check if the gauge attack hits the invaders & bullets
    if sp_player1.enabled and sp_player1.gauge_attack>0:
        rho = (10-sp_player1.gauge_attack)*0.06
        for target in splist_invader:
            if target.type==7 or target.type==8: continue # skip rescuecap/weaponup
            dist =  ((target.x-sp_player1.x)**2 + (target.y-sp_player1.y)**2)**0.5
            if dist<rho:
                target.hp -= 1
                if target.type==1 or target.type==2 or target.type==6: sp_player1.score += 10
                if target.type==3 or target.type==4: sp_player1.score += 15
                if target.type==5: sp_player1.score += 20
        for target in splist_bullet_inv:
            dist =  ((target.x-sp_player1.x)**2 + (target.y-sp_player1.y)**2)**0.5
            if dist<rho:
                target.hp -= 1
                sp_player1.score += 5
        if sp_player2.enabled and sp_player2.gauge_freeze==0:
            dist = ((sp_player1.x-sp_player2.x)**2 + (sp_player1.y-sp_player2.y)**2)**0.5
            if dist<rho: sp_player2.gauge_freeze=50

    if sp_player2.enabled and sp_player2.gauge_attack>0:
        rho = (10-sp_player2.gauge_attack)*0.06
        for target in splist_invader:
            if target.type==7 or target.type==8: continue # skip rescuecap/weaponup
            dist =  ((target.x-sp_player2.x)**2 + (target.y-sp_player2.y)**2)**0.5
            if dist<rho:
                target.hp -= 1
                if target.type==1 or target.type==2 or target.type==6: sp_player2.score += 10
                if target.type==3 or target.type==4: sp_player2.score += 15
                if target.type==5: sp_player2.score += 20
        for target in splist_bullet_inv:
            dist =  ((target.x-sp_player2.x)**2 + (target.y-sp_player2.y)**2)**0.5
            if dist<rho:
                target.hp -= 1
                sp_player2.score += 5
        if sp_player1.enabled and sp_player1.gauge_freeze==0:
            dist = ((sp_player1.x-sp_player2.x)**2 + (sp_player1.y-sp_player2.y)**2)**0.5
            if dist<rho: sp_player1.gauge_freeze=50

    # loop over all bullets from the invaders, check if it hits the player
    for sp in splist_bullet_inv:
        if sp_player1.enabled and sp_player1.eval_collision(sp):
            sp_player1.hp -= 1
            if sp_player1.weapon>1: sp_player1.weapon -=1
            sp.hp -= 1
        if sp_player2.enabled and sp_player2.eval_collision(sp):
            sp_player2.hp -= 1
            if sp_player2.weapon>1: sp_player2.weapon -=1
            sp.hp -= 1

    # loop over all invaders+rescuecap/weaponup, check if it hits the player
    for sp in splist_invader:
        if sp.type==6: # boss
            if sp_player1.enabled and sp.eval_collision(sp_player1):
                sp_player1.hp -= 1
                if sp_player1.weapon>1: sp_player1.weapon -=1
                sp.hp -= 1
            if sp_player2.enabled and sp.eval_collision(sp_player2):
                sp_player2.hp -= 1
                if sp_player2.weapon>1: sp_player2.weapon -=1
                sp.hp -= 1
        elif sp.type==7: # rescuecap
            if sp_player1.enabled and sp_player1.eval_collision(sp):
                if sp_player1.hp<12: sp_player1.hp += 1
                sp_player1.score += 20
                sp.hp -= 1
            if sp_player2.enabled and sp_player2.eval_collision(sp):
                if sp_player2.hp<12: sp_player2.hp += 1
                sp_player2.score += 20
                sp.hp -= 1
        elif sp.type==8: # weaponup
            if sp_player1.enabled and sp_player1.eval_collision(sp):
                if sp_player1.weapon<3: sp_player1.weapon += 1
                sp_player1.score += 20
                sp.hp -= 1
            if sp_player2.enabled and sp_player2.eval_collision(sp):
                if sp_player2.weapon<3: sp_player2.weapon += 1
                sp_player2.score += 20
                sp.hp -= 1
        else: # other invaders
            if sp_player1.enabled and sp_player1.eval_collision(sp):
                sp_player1.hp -= 1
                if sp_player1.weapon>1: sp_player1.weapon -=1
                sp.hp -= 1
            if sp_player2.enabled and sp_player2.eval_collision(sp):
                sp_player2.hp -= 1
                if sp_player2.weapon>1: sp_player2.weapon -=1
                sp.hp -= 1

    # move and draw the invaders
    sx, sy = [[] for n in range(8)], [[] for n in range(8)]
    for sp in splist_invader[:]:
        sp.move()

        if sp.x<-0.1 or sp.x>1.1 or sp.y<-0.2 or sp.y>1.4:
            splist_invader.remove(sp)
            continue
        if sp.enabled and sp.hp<=0:
            sp.hp = 0
            sp.enabled = False
            if sp.type==6: # boss!
                if invader_level<7:
                    invader_level += 1
                    center_message = 'Level '+str(invader_level)
                    center_message_delay = 40
                invader_boss = 0
            splist_invader.remove(sp)
            if sp.type!=7:
                splist_explosion.append(sp)
            continue

        sx[sp.type-1].append(sp.x)
        sy[sp.type-1].append(sp.y)

    plt_invader1.set_data(sx[0],sy[0])
    plt_invader2.set_data(sx[1],sy[1])
    plt_invader3.set_data(sx[2],sy[2])
    plt_invader4.set_data(sx[3],sy[3])
    plt_ufo.set_data(sx[4],sy[4])
    plt_superufo.set_data(sx[5],sy[5])
    plt_rescuecap.set_data(sx[6],sy[6])
    plt_weaponup.set_data(sx[7],sy[7])

    # move and draw the bullets from the invaders
    sx, sy = [], []
    for sp in splist_bullet_inv[:]:
        sp.move()
        if sp.x<-0.1 or sp.x>1.1 or sp.y<-0.2 or sp.y>1.2:
            splist_bullet_inv.remove(sp)
            continue
        if sp.hp<=0:
            splist_bullet_inv.remove(sp)
            continue
        sx.append(sp.x)
        sy.append(sp.y)
    plt_bullet_inv.set_data(sx,sy)

    # move and draw the bullets from the players
    sx, sy = [], []
    for sp in splist_bullet_ply1[:]:
        sp.move()
        if sp.x<-0.1 or sp.x>1.1 or sp.y<-0.2 or sp.y>1.2:
            splist_bullet_ply1.remove(sp)
            continue
        if sp.hp<=0:
            splist_bullet_ply1.remove(sp)
            continue
        sx.append(sp.x)
        sy.append(sp.y)

    for sp in splist_bullet_ply2[:]:
        sp.move()
        if sp.x<-0.1 or sp.x>1.1 or sp.y<-0.2 or sp.y>1.2:
            splist_bullet_ply2.remove(sp)
            continue
        if sp.hp<=0:
            splist_bullet_ply2.remove(sp)
            continue
        sx.append(sp.x)
        sy.append(sp.y)

    plt_bullet_ply.set_data(sx,sy)

    # now move the players, and draw them
    sp_player1.move()
    sp_player2.move()

    if sp_player1.x>1.: sp_player1.x = 1.
    if sp_player1.y>1.: sp_player1.y = 1.
    if sp_player2.x>1.: sp_player2.x = 1.
    if sp_player2.y>1.: sp_player2.y = 1.
    if sp_player1.x<0.: sp_player1.x = 0.
    if sp_player1.y<0.: sp_player1.y = 0.
    if sp_player2.x<0.: sp_player2.x = 0.
    if sp_player2.y<0.: sp_player2.y = 0.

    if sp_player1.enabled and sp_player1.hp<=0:
        sp_player1.hp = 0
        sp_player1.enabled = False
        splist_explosion.append(sp_player1)

    if sp_player1.enabled:
        plt_player1.set_data([sp_player1.x],[sp_player1.y])
    else:
        plt_player1.set_data([],[])

    if sp_player2.enabled and sp_player2.hp<=0:
        sp_player2.hp = 0
        sp_player2.enabled = False
        splist_explosion.append(sp_player2)

    if sp_player2.enabled:
        plt_player2.set_data([sp_player2.x],[sp_player2.y])
    else:
        plt_player2.set_data([],[])

    # display the explosions
    sx, sy = [], []
    for sp in splist_explosion[:]:
        sx.append(sp.x)
        sy.append(sp.y)
        if sp.type==5:
            for i in range(6):
                sx.append(sp.x+(np.random.rand(1)[0]-0.5)*0.1)
                sy.append(sp.y+(np.random.rand(1)[0]-0.5)*0.1)
        if sp.type==6:
            for i in range(96+sp.hp*4):
                sx.append(sp.x+(np.random.rand(1)[0]-0.5)*0.4)
                sy.append(sp.y+(np.random.rand(1)[0]-0.5)*0.4)

        sp.hp -= 1
        if sp.type==5 and sp.hp<=-6: splist_explosion.remove(sp)
        if sp.type==6 and sp.hp<=-18: splist_explosion.remove(sp)
        if sp.type!=5 and sp.type!=6 and sp.hp<=-3: splist_explosion.remove(sp)

    plt_explosion.set_data(sx,sy)

    plt_tx_p1.set(text='P1  '+str(sp_player1.score))
    plt_tx_p2.set(text=str(sp_player2.score)+'  P2')

    hp_disp = sp_player1.hp
    if hp_disp>12: hp_disp=12
    plt_tx_p1_hp.set(text='HP  '+r'$\blacksquare$'*hp_disp)
    hp_disp = sp_player2.hp
    if hp_disp>12: hp_disp=12
    plt_tx_p2_hp.set(text=r'$\blacksquare$'*hp_disp+'  HP')

    plt_gauge_p1.set_data([-0.05,-0.05+sp_player1.gauge*0.001*0.4],[-0.15,-0.15])
    plt_gauge_p2.set_data([+1.05-sp_player2.gauge*0.001*0.4,+1.05],[-0.15,-0.15])

    # display the gauge attack
    sx, sy = [], []
    if sp_player1.gauge_attack>0:
        for i in range(91):
            rho = (10-sp_player1.gauge_attack)*0.06
            phi = np.pi*2.*i/90.
            sx.append(sp_player1.x + rho*np.cos(phi))
            sy.append(sp_player1.y + rho*np.sin(phi))
    plt_gauge_attack_p1.set_data(sx,sy)

    sx, sy = [], []
    if sp_player2.gauge_attack>0:
        for i in range(91):
            rho = (10-sp_player2.gauge_attack)*0.06
            phi = np.pi*2.*i/90.
            sx.append(sp_player2.x + rho*np.cos(phi))
            sy.append(sp_player2.y + rho*np.sin(phi))
    plt_gauge_attack_p2.set_data(sx,sy)

    # level up
    if (sp_player1.score+sp_player2.score>1500  and invader_level<=1) or \
       (sp_player1.score+sp_player2.score>4000  and invader_level<=2) or \
       (sp_player1.score+sp_player2.score>7500  and invader_level<=3) or \
       (sp_player1.score+sp_player2.score>12000 and invader_level<=4) or \
       (sp_player1.score+sp_player2.score>17500 and invader_level<=5) or \
       (sp_player1.score+sp_player2.score>24000 and invader_level<=6) or \
       (sp_player1.score+sp_player2.score>24000 and (sp_player1.score+sp_player2.score-24000)%7500==0):
           if invader_boss==0:
               center_message = '!!WARNING!!'
               center_message_delay = 60
               center_message_blink = 1
               invader_boss = 1

    # the game over message
    if not sp_player1.enabled and not sp_player2.enabled:
        center_message = 'Game Over'
        center_message_delay = 999

    if center_message_delay>0:
        if center_message_blink>0 and center_message_delay%10<5:
            plt_tx_center.set(text='')
        else:
            plt_tx_center.set(text=center_message)
        if center_message_delay!=999: center_message_delay -= 1
    else:
        plt_tx_center.set(text='')
        center_message_blink = 0

    return plt_invader1, plt_invader2, plt_invader3, plt_invader4, plt_ufo, plt_player1, plt_player2, plt_rescuecap, plt_weaponup, plt_explosion, plt_bullet_inv, plt_bullet_ply, plt_tx_center, plt_tx_p1, plt_tx_p2, plt_tx_p1_hp, plt_tx_p2_hp, plt_gauge_p1, plt_gauge_p2, plt_gauge_attack_p1, plt_gauge_attack_p2


# main animation function call
anim = animation.FuncAnimation(fig, animate, init_func=init, interval=40)

# plt.tight_layout()
plt.show()
