# load all required mods 引入模组和初始化pygame
import pygame
import random
import time
import json
from os import path

# add mix init for better performance 加上mixer pre init 改善声音效果
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

# set dir for loading sound and image files 设置路径用来方便导入声音和图片:
units_dir = path.join(path.dirname(__file__), 'units')
backgrounds_dir = path.join(path.dirname(__file__), 'backgrounds')
sound_dir = path.join(path.dirname(__file__), 'music')
ani_dir = path.join(path.dirname(__file__), 'animation')

# load sound and background music 载入声音和背景音乐
getbomb_s = pygame.mixer.Sound(path.join(sound_dir, "getbomb.wav"))
crash_s = pygame.mixer.Sound(path.join(sound_dir, "explode.ogg"))
shoot_s = pygame.mixer.Sound(path.join(sound_dir, "shoot.wav"))
hit_s = pygame.mixer.Sound(path.join(sound_dir, "hit.wav"))
levelup_s = pygame.mixer.Sound(path.join(sound_dir, "levelup.wav"))
music_s = pygame.mixer.music.load(path.join(sound_dir, "Calluses_II.ogg"))
meteor_s = pygame.mixer.Sound(path.join(sound_dir, "meteor_rain.wav"))
victory_s=pygame.mixer.Sound(path.join(sound_dir, "victory.wav"))
# screen size 屏幕尺寸
width = 800
height = 600
display_size = (width, height)
# define color 颜色:
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 200, 0)

# define global variable 定义全局变量
global haha  # score  variable 即时得分
haha = 0
global level  # game level variable 难度
level = 0
global best  # final score variable 最终得分


# Use json file to store player's highest score 用json文件来储存玩家最终得分
with open('playersave.json', 'r') as j:
    k = json.load(j)
best = int(k['best'])


# Define game screen and title 定义游戏庄口大小和标题
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption('Space Odyssey')

# define font for the ingame text 定义游戏内文字的字体
pygame.font.get_init()
ziti = pygame.font.get_default_font()


#load intro manu image 菜单图片
intro_img = pygame.image.load(path.join(backgrounds_dir, 'intro.png')).convert()
#load player image 玩家图片
image1 = pygame.image.load(path.join(units_dir, 'dabai.png')).convert()
#load playerlife icon image 玩家图片(小)
image11 = pygame.transform.scale(pygame.image.load(path.join(units_dir, 'dabai_small.png')).convert(), (20, 20))
image11.set_colorkey(black)
#load boss images to Bosses_img list Boss图片
Bosses_img = []
for i in range(2):
    Bosses_img.append(pygame.image.load(path.join(units_dir, f'boss{i}.png')).convert())
#load meteor icon images
meteor_img_small = pygame.image.load(path.join(units_dir, 'spaceMeteors0.png')).convert()
meteor_img_small = pygame.transform.scale(meteor_img_small, (30, 30))
meteor_img_small.set_colorkey(black)
#load meteor images for the meteor rain fucntion 载入陨石图片
meteor_img = []
for i in range(4):
    meteor_img.append(pygame.image.load(path.join(units_dir, f'spaceMeteors{i}.png')).convert())
enemy_img = []
#load difffent enemy images to enemy_img list 载入不同的敌人图片
for i in range(1, 7):
    enemy_img.append(pygame.image.load(path.join(units_dir, f'e0{i}.png')).convert())
#load bullit image 载入玩家子弹图片
image3 = pygame.image.load(path.join(units_dir, 'bullet.png')).convert()
#load small enemyship image  载入敌人小飞机图片
subenemy_img = []
for i in range(4):
    subenemy_img.append(pygame.image.load(path.join(units_dir, f'xiaozhushou{i}.png')).convert())
#load explosion images to explosion_animation list 载入爆炸图片
explosion_animation = []
for i in range(9):
    explosion_animation.append(pygame.image.load(path.join(ani_dir, f'regularExplosion0{i}.png')).convert())
# load back ground images to backgroud list 载入每关背景图片
background = []
for i in range(3):
    background.append(pygame.image.load(path.join(backgrounds_dir, f'b{i}.png')).convert())
# load gem image 载入宝石图片
gem_img = pygame.image.load(path.join(units_dir, 'gem0.png')).convert()
gem_img.set_colorkey(black)
victory_img=pygame.image.load(path.join(backgrounds_dir, f'victory.png')).convert()

# instantiate eight sprite groups 实例化所有精灵群组
mrbeans = pygame.sprite.Group()
bullets = pygame.sprite.Group()
zhujiaos = pygame.sprite.Group()
explosions = pygame.sprite.Group()
meteors = pygame.sprite.Group()
bosses = pygame.sprite.Group()
missles = pygame.sprite.Group()
gems = pygame.sprite.Group()


# boss class  定义boss类
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        global level
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Bosses_img[level], (150, 150))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = width - self.rect.w - 20
        self.rect.centery = height / 2
        self.vy = 2
        self.lives = 100 + 50 * level
        self.last_time = pygame.time.get_ticks()
    #boss move and attack logic BOSS运动和攻击逻辑更新方法
    def update(self):
        self.rect.y += self.vy
        if self.rect.y < 0:
            self.vy = 2
        if self.rect.y > height - self.rect.h:
            self.vy = -2
        now = pygame.time.get_ticks()
        if now - self.last_time > 3000:
            self.split()
            self.last_time = pygame.time.get_ticks()
    #boss attack method BOSS攻击方法
    def split(self):
        for i in range(12 + 2 * level):
            zhujiao = Zhujiao(self.rect.centerx, self.rect.centery, 2 + level)
            zhujiaos.add(zhujiao)
    #boss died method BOSS 死亡方法
    def explosion(self):
        pygame.mixer.Sound.play(hit_s)
        self.last_time = pygame.time.get_ticks()
        now = pygame.time.get_ticks()
        explosion = Explosion(self.rect.center, self.rect.bottom - self.rect.top)
        explosions.add(explosion)
        while now - self.last_time <= 3000:
            screen.blit(dabai.image, dabai.rect)
            bosses.draw(screen)
            explosions.draw(screen)
            if now - self.last_time > 5000:
                pygame.mixer.Sound.play(hit_s)
                explosion = Explosion(self.rect.center, self.rect.bottom - self.rect.top)
                explosions.add(explosion)
            draw_ui()
            self.rect.y += self.vy
            pygame.display.flip()
            pygame.time.Clock().tick(60)
            now = pygame.time.get_ticks()


# bomb class, use to create a meteor rain from the top of screen   陨石类 主要用于制造从屏幕上方落下的流星雨

class MeteorRain(pygame.sprite.Sprite):
    def __init__(self,place):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(meteor_img[random.randint(0, 3)], (90, 90))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = place
        self.rect.centery = 0
        self.vx = random.randrange(-2, 2)
        self.vy = random.randint(5, 7)
        self.last_time = pygame.time.get_ticks()
        self.image_origin = self.image.copy()
        self.i = 0
#Moveing logic update  陨石更新运动的方法
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        # now=pygame.time.get_ticks()
        # #The following commented paragraph contains a rotation effect for each meteor.Uncomment this praragraph will add rotaion effect to meteor rain 中间这段反注释掉可以让流星获得旋转效果 我因为感觉太乱所以没启用
        # if now-self.last_time>60:
        #     old_center=self.rect.center
        #     self.image=pygame.transform.rotate(self.image_origin,self.i)
        #     self.rect=self.image.get_rect()
        #     self.rect.center=old_center
        #     self.i+=1
        #     self.last_time=now
        if self.rect.y > 600:
            self.kill()
    #Meteor explosion method #陨石爆炸方法
    def explosion(self):
        explosion = Explosion(self.rect.center, self.rect.right - self.rect.left)
        explosions.add(explosion)


# #add button for manu unfinished work : 按钮功能  暂时还没做 以后添加
# class Button(pygame.sprite.Sprite):
#     def __init__(self,num,size,x,y):
#     pygame.sprite.Sprite.__init__(self)
#     self.image=pygame.transform.scale(buttons[num],(size,size))
#     self.rect = self.image.get_rect()
#     self.rect.x=x
#     self.rect.y=y


# explosion class, with center and size arguments,creates suitable explosion for all sprites  爆炸类 接受位置和大小的参数 为所有精灵制造适应其大小的爆炸 包括子弹击中效果

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pygame.transform.scale(explosion_animation[0], (self.size, self.size))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_time = pygame.time.get_ticks()
#update method, used to create animation effect #爆炸类的更新方法 用来制造动画效果
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_time > 60:
            if self.frame < len(explosion_animation):
                self.image = pygame.transform.scale(explosion_animation[self.frame], (self.size, self.size))
                self.image.set_colorkey((0, 0, 0))
                self.frame += 1
                self.last_time = pygame.time.get_ticks()
            else:
                self.kill()


# define player class 定义 玩家 类


class Dabai(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image1, (40, 46))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centery = height / 2
        self.rect.centerx = width / 20
        self.lives = 3
        self.hp = 100
        self.energy = 0
        self.die_flag = False
        self.dietime = pygame.time.get_ticks()
        self.bombs = 1

    # update method to detect player inputs and add special effect to player sprite . 玩家类的更新方法 主要用于检测键盘输入和添加吃到宝石后的效果
    def update(self, dabai_speed):
        if self.energy > 100:
            pygame.mixer.Sound.play(getbomb_s)
            self.energy = 0
            self.bombs += 1
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect.x -= dabai_speed
        if key[pygame.K_d]:
            self.rect.x += dabai_speed
        if key[pygame.K_s]:
            self.rect.y += dabai_speed
        if key[pygame.K_w]:
            self.rect.y -= dabai_speed
        # set boundary 防止出界
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > height:
            self.rect.bottom = height
        elif self.die_flag == True:
            now = pygame.time.get_ticks()
            if now - self.dietime <= 1500:
                self.rect.x = 2 * width
            else:
                self.die_flag = False
                self.rect.centery = height / 2
                self.rect.centerx = width / 20
        global heihei
        if boss_flag:
            for i in bosses:
                heihei = i
        else:
            for i in mrbeans:
                heihei = i

    # define player's shooting method #射击方法

    def shoot(self):
        pygame.mixer.Sound.play(shoot_s)
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        bullets.add(bullet)
        if level>0:
            bullet1 = Bullet(self.rect.centerx, self.rect.centery+15)
            bullets.add(bullet1)

    #define the lighting ball method #制造自动跟踪的球状闪电的方法
    def missle(self):
        missle = Missle(self.rect.centerx, self.rect.centery)
        missles.add(missle)
    # player's explosion method 爆炸方法

    def explosion(self):
        explosion = Explosion(self.rect.center, self.rect.right - self.rect.left)
        explosions.add(explosion)
        self.kill()
    # add bullet shooting effects 添加子弹发射效果

    def shotexplosion(self):
        explosion = Explosion(self.rect.center, 5)
        explosions.add(explosion)

# define gem class 定义宝石类


class Gem(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(gem_img, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.vx=-1
        self.vy=0

    def update(self):
        # if self.rect.centerx>dabai.rect.centerx:
        #     self.vx-=1
        # if self.rect.centerx<dabai.rect.centerx: 
        #     self.vx+=1
        # if self.rect.centery>dabai.rect.centery:
        #     self.vy-=1
        # if self.rect.centery<dabai.rect.centery:
        #     self.vy+=1
        # if self.vx>3:
        #     self.vx=3        
        # if self.vx<-3:
        #     self.vx=-3
        # if self.vy>3:
        #     self.vy=3
        # if self.vy<-3:
        #     self.vy=-3

        self.rect.x += self.vx
        self.rect.y+=self.vy


#define enemy class # 主要敌人类
class MrBean(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img[random.randint(0, 2) + level * 3], (90, 90))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centery = random.randint(0, height - self.rect.h)
        self.rect.centerx = width - 30
        self.vx = random.randrange(-3 - level, -2)
        self.vy = random.randint(-2 - level, 2 + level)
        self.lives = 3 + level
        self.last_time = pygame.time.get_ticks()
        self.flag=True
        self.count=0
    # 基于逻辑运算的状态更新method

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.x < 0:
            self.rect.centery = random.randint(0, height - self.rect.h)
            self.rect.centerx = width - 30
            self.flag=True
            self.count=0
        if self.rect.y < 0:
            self.vy = 2

        now = pygame.time.get_ticks()
        if self.flag:
            if now - self.last_time > 500:
                self.split()
                self.count+=1
                if self.count>1+level:
                    self.flag=False


    # 定义MrBean被子弹打中后的分裂method,初始为2个 根据leveld w而增加

    def split(self):
        a=random.randint(0,1)
        zhujiao = Zhujiao(self.rect.centerx, self.rect.centery,a)
        zhujiaos.add(zhujiao)
        self.last_time = pygame.time.get_ticks()




    # 爆炸method

    def explosion(self):
        explosion = Explosion(self.rect.center, self.rect.right - self.rect.left)
        explosions.add(explosion)

        # 定义Bullet sprite 类

#define bullet class 定义子弹 类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image3, (10, 5))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
    # 子弹运动状态更新

    def update(self):
        self.rect.x += 10

    def explosion(self):
        explosion = Explosion(self.rect.center, self.rect.right - self.rect.left)
        explosions.add(explosion)


#define the lighting ball 自动跟踪球状闪电类
class Missle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(subenemy_img[2], (20, 20))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.vx=0
        self.vy=0
        global heihei
        if boss_flag:
            for i in bosses:
                heihei=i
        else:
            for i in mrbeans:
                heihei=i
    # 运动状态更新

    def update(self):
        if self.rect.centerx>heihei.rect.centerx:
            self.vx-=1
        if self.rect.centerx<heihei.rect.centerx: 
            self.vx+=1
        if self.rect.centery>heihei.rect.centery:
            self.vy-=1
        if self.rect.centery<heihei.rect.centery:
            self.vy+=1
        if self.vx>8:
            self.vx=8        
        if self.vx<-8:
            self.vx=-8
        if self.vy>6:
            self.vy=6
        if self.vy<-6:
            self.vy=-6

        self.rect.x += self.vx
        self.rect.y+=self.vy

    def explosion(self):
        explosion = Explosion(self.rect.center, self.rect.right - self.rect.left)
        explosions.add(explosion)



# define sub emeny class 定义分裂后的敌人类


class Zhujiao(pygame.sprite.Sprite):

    def __init__(self, x, y,size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(subenemy_img[size], (45, 45))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centery = y - 50
        self.rect.centerx = x - 20
        self.vx = random.randint(-5, -2)
        self.vy = random.randint(-3, 3)
        self.type=size
    # 类似Mr_bean.update的基于运算的状态更新method

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        # 出界后删掉! 以免影响游戏性能
        if self.rect.x < 0 or self.rect.y < 0 or self.rect.y > height:
            zhujiaos.remove(self)
        if self.type<2:
            if self.rect.centery>dabai.rect.centery:
                self.vy-=1
            if self.rect.centery<dabai.rect.centery:
                self.vy+=1
            if self.vy>5:
                self.vy=5
            if self.vy<-5:
                self.vy=-5
            if self.rect.centery-dabai.rect.centery<30 and self.rect.centery-dabai.rect.centery>-30:
                self.vx=-12





    # 爆炸method

    def explosion(self):
        explosion = Explosion(self.rect.center, self.rect.right - self.rect.left)
        explosions.add(explosion)

# UI function 新增UI
def draw_ui():
    pygame.draw.rect(screen,green,(30,50,dabai.hp,15))
    pygame.draw.rect(screen,white,(30,50,100,15),2)
    pygame.draw.rect(screen,yellow,(width-170,50,dabai.energy,15))
    pygame.draw.rect(screen,white,(width-170,50,100,15),2)

    life_rect=image11.get_rect()
    life_rect.x=width-(life_rect.width+10)
    life_rect.y=height-60
    for i in range(dabai.lives):
        screen.blit(image11,life_rect)
        life_rect.x-=life_rect.width+10

    bombs_rect=meteor_img_small.get_rect()
    bombs_rect.x=bombs_rect.width
    bombs_rect.y=height-60
    for i in range(dabai.bombs):
        screen.blit(meteor_img_small,bombs_rect)
        bombs_rect.x+=bombs_rect.width+10



# 定义所有显示文本需要调用的一个子函数  所有文字显示参考了pygame官方说明文档

def xianshi(text, font, color):
    biaomian = font.render(text, True, color)
    return biaomian, biaomian.get_rect()

# 定义显示撞毁的函数 字体大小60 居中显示 颜色红色


def text_display(text):
    dahaozi = pygame.font.Font(ziti, 60)
    zi, kuai = xianshi(text, dahaozi, red)
    kuai.center = (width / 2, height / 2)
    screen.blit(zi, kuai)
    pygame.display.flip()

# 定义显示分数的函数 字体大小30 位置右上角 颜色白色


def display_score(score):
    dahaozi = pygame.font.Font(ziti, 30)
    zi, kuai = xianshi(score, dahaozi, white)
    kuai.center = (display_size[0] * 0.85, display_size[1] * 0.05)
    screen.blit(zi, kuai)


# 定义显示分数的函数, 字体大小30 能位置左上角 颜色白色
def display_best(best):
    dahaozi = pygame.font.Font(ziti, 30)
    zi, kuai = xianshi(best, dahaozi, white)
    kuai.center = (display_size[0] * 0.1, display_size[1] * 0.05)
    screen.blit(zi, kuai)


# pygame文档中screen和surface有一个set_alpha的method 可以用来做渐变 这里做了一个死亡画面的渐隐level之间屏幕渐变 alpha值在迭代中随0-250增强
def fade():
    fade = pygame.Surface(display_size)
    fade.fill(black)
    for i in range(300):
        fade.set_alpha(i)
        screen.blit(background[level], (0, 0))
        screen.blit(dabai.image, dabai.rect)
        explosions.draw(screen)
        explosions.update()
        mrbeans.draw(screen)
        bullets.draw(screen)
        zhujiaos.draw(screen)
        screen.blit(fade, (0, 0))
        pygame.display.flip()

# 同上,做了一个新关卡场景的渐变出现 alpha值在迭代中随0-300增强


def emerge():
    emerge = pygame.Surface(display_size)
    screen.fill(black)
    for i in range(300):
        emerge.set_alpha(i)
        emerge.blit(background[level], (0, 0))
        screen.blit(emerge, (0, 0))
        pygame.display.flip()


# 显示撞毁所以把重新开始游戏也加上了
def crash():
    global haha
    global level
    global best
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_s)

    fade()
    text_display(f'''Score:  {haha}   Best:    {best}''')
    haha = 0
    level = 0
# 1.5秒后重生
    for i in range(1500):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                R_flag = False
                # 退出的话储存玩家得分best
                with open('playersave.json', 'w') as j:
                    json.dump({"best": f"{best}"}, j)

                pygame.quit()
                exit()
        pygame.time.delay(1)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    GameRun()

# 定义升级函数 显示升级后在新难度开始游戏


def levelup():
    global level
    if level==1:
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(victory_s)
        screen.fill(black)
        screen.blit(victory_img,(100,50))
        pygame.display.flip()
        pygame.time.delay(4000)
        pygame.quit()
        exit()

    pygame.mixer.Sound.play(levelup_s)
    screen.fill(black)
    text_display('Level    {}'.format(level + 2))
    level += 1
    pygame.time.delay(1200)
    emerge()
    GameRun()

#Start manu #游戏开始菜单
def game_intro():
    intro=True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                R_flag = False
                with open('playersave.json', 'w') as j:
                    json.dump({"best": f"{best}"}, j)
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:

                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                GameRun()


        screen.blit(intro_img,(0,0))
        pygame.display.flip()
        pygame.time.Clock().tick(60)




#main 主程序
def GameRun():
    # 重新声明要改变赋值的全局变量
    global level
    global haha
    global dabai
    global best
    global R_flag
    global boss_flag
    meteors.empty()
    missles.empty()
    gems.empty()
    mrbeans.empty()
    bullets.empty()
    zhujiaos.empty()
    explosions.empty()
    bosses.empty()
    dabai = Dabai()
    mrenemy=MrBean()
    progress=0
    levelha=True
    boss_flag=False
    # 碰撞检测参数
    colliderate = pygame.sprite.collide_rect_ratio

    mrbean = MrBean()
    mrbeans.add(mrbean)
    R_flag = True

    bx = 0
    # 主程序开始
    last_time=pygame.time.get_ticks()
    while R_flag:
        now=pygame.time.get_ticks()
        if now-last_time>1500-haha and not boss_flag and len(mrbeans)<4+level:
            mrbean = MrBean()
            mrbeans.add(mrbean)
            last_time=now
        if progress > 220:
            zhujiaos.empty()  # 判断进度是否达到一定值 达到则boss战               
            mrbeans.empty()
            boss=Boss()
            bosses.add(boss)
            boss_flag=True
            progress=0
        if levelha==False:
            R_flag = False
            levelup()
        for event in pygame.event.get():
            # 判断是否退出
            if event.type == pygame.QUIT:
                R_flag = False
                # 退出的话储存玩家得分best
                with open('playersave.json', 'w') as j:
                    json.dump({"best": f"{best}"}, j)
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # 判断是否按下
                if event.key == pygame.K_RETURN:
                    dabai.shoot()
                    dabai.shotexplosion()
                elif event.key == pygame.K_b:
                    if dabai.bombs>0:
                        pygame.mixer.Sound.play(meteor_s)
                        dabai.bombs-=1
                        x=100
                        for m in range(8):
                            meteor=MeteorRain(x)
                            x+=100
                            meteors.add(meteor)

        # 所有sprite状态更新
        dabai.update(5 + level)
        mrbeans.update()
        bullets.update()
        zhujiaos.update()
        explosions.update()
        meteors.update()
        bosses.update()
        missles.update()
        gems.update()
        # 判断dabai和MrBean是否相撞,相撞消灭dabai 运行crash
        collide = pygame.sprite.spritecollide(dabai, gems, True)
        for i in collide:
            pygame.mixer.Sound.play(levelup_s)
            for j in range(5):
                dabai.missle()

        collide = pygame.sprite.spritecollide(dabai, mrbeans, True,colliderate(0.8))
        for c in collide:
            dabai.hp=dabai.lives-40
            dabai.explosion()
            if dabai.hp<0:
                pygame.mixer.Sound.play(hit_s)
                dabai.dietime=pygame.time.get_ticks()
                dabai.die_flag=True
                dabai.lives-=1
                mrbean = MrBean()
                mrbeans.add(mrbean)
                dabai.explosion()
                dabai.hp=100
            if dabai.lives<0:
                dabai.explosion()
                R_flag = False
                crash()
        # 判断bullets是否击中Mr_bean 击中双方消失 返回值进入hits
        hits = pygame.sprite.groupcollide(bullets, mrbeans, False, False)
        if hits:
            # 击中得分
            haha += 2
            dabai.energy+=2
            progress+=2
            # 反复迭代hits的key值以得到数据类型为sprite的hits value值 使用split method实现被击中的那个MrBean分裂
            for j in hits.keys():
                j.explosion()
                j.kill()
                for k in hits[j]:
                    k.lives -= 1
                    if k.lives <= 0:
                        pygame.mixer.Sound.play(hit_s)
                        k.kill()
                        a=random.randint(0,10)
                        if a>8:
                            gem=Gem(k.rect.centerx,k.rect.centery)
                            gems.add(gem)
                        k.explosion()



        # 判断zhujiao是否和dabai相撞 相撞消灭dabai 运行crash
        collide2 = pygame.sprite.spritecollide(dabai, zhujiaos, True, colliderate(0.8))
        for c in collide2:
            if boss_flag:
                dabai.hp-=101
            else:    
                dabai.hp-=35
            dabai.explosion()
            if dabai.hp<0:
                    dabai.dietime=pygame.time.get_ticks()
                    dabai.die_flag=True
                    dabai.lives-=1
                    dabai.explosion()
                    dabai.hp=100
                    pygame.mixer.Sound.play(hit_s)
            if dabai.lives<0:
                dabai.explosion()
                R_flag = False
                crash()
        if not boss_flag:
            hits2 = pygame.sprite.groupcollide(bullets, zhujiaos, True, True)
            if hits2:
                haha += 1
                dabai.energy+=1
                progress+=1
                for hit in hits2.keys():
                    for e in hits2[hit]:
                        e.explosion()

        # 画出场景和所有sprite
        rain1=pygame.sprite.groupcollide(meteors, zhujiaos, False, True)
        if rain1:
            haha+=1
            dabai.energy+=1
            progress+=1
            for i in rain1.keys():
                for j in rain1[i]:
                    j.explosion()

        rain2=pygame.sprite.groupcollide(meteors, mrbeans, False, True)
        if rain2:
            pygame.mixer.Sound.play(hit_s)
            haha+=2
            dabai.energy+=2
            progress+=2
            for i in rain2.keys():
                for j in rain2[i]:
                    j.explosion()

        rain3=pygame.sprite.groupcollide(meteors, bosses, False, False)
        if rain3:
            haha += 2
            dabai.energy+=2
            for j in rain3.keys():
                j.explosion()
                j.kill()
                for k in rain3[j]:
                    k.lives -= 5
                    if k.lives <= 0:
                        pygame.mixer.Sound.play(hit_s)
                        k.kill()
                        k.explosion()
                        bosses.empty()
                        levelha=False
        hits3 = pygame.sprite.groupcollide(bullets, bosses, False, False)
        if hits3:
            # 击中得分
            haha += 2
            dabai.energy+=2
            # 反复迭代hits的key值以得到数据类型为sprite的hits value值 使用split method实现被击中的那个MrBean分裂
            for j in hits3.keys():
                j.explosion()
                j.kill()
                for k in hits3[j]:
                    k.lives -= 1
                    if k.lives <= 0:
                        pygame.mixer.Sound.play(hit_s)
                        k.kill()
                        k.explosion()
                        bosses.empty()
                        levelha=False

        hits=pygame.sprite.groupcollide(missles, mrbeans, True, True,colliderate(0.5))
        if hits:
            pygame.mixer.Sound.play(hit_s)
            progress+=2
            for i in hits.keys():
                for j in hits[i]:
                    j.explosion()

        if boss_flag:
            hits=pygame.sprite.groupcollide(missles, bosses, False, False)
            if hits:
                # 击中得分
                dabai.energy+=2
                # 反复迭代hits的key值以得到数据类型为sprite的hits value值 使用split method实现被击中的那个MrBean分裂
                for j in hits.keys():
                    j.explosion()
                    j.kill()
                    for k in hits[j]:
                        k.lives -= 1
                        if k.lives <= 0:
                            pygame.mixer.Sound.play(hit_s)
                            k.kill()
                            k.explosion()
                            bosses.empty()
                            levelha=False




        xr = bx % background[level].get_rect().width  # 取xr对于背景图片的相对坐标
        screen.blit(background[level], (xr - background[level].get_rect().width, 0))  # 减去背景图片宽度让xr从最左边开始算
        if xr < width:  # 判断背景图是否离开屏幕最右侧
            screen.blit(background[level], (xr, 0))  # 重画
        bx -= 1  # '宇宙动起来!'
        screen.blit(dabai.image, dabai.rect)
        bosses.draw(screen)
        mrbeans.draw(screen)
        bullets.draw(screen)
        zhujiaos.draw(screen)
        explosions.draw(screen)
        meteors.draw(screen)
        missles.draw(screen)
        gems.draw(screen)
        draw_ui()

        # 更新最佳得分,显示分数和最佳得分
        if haha > best:
            best = haha
        display_best('BEST:' + str(best))
        display_score('SCORE:' + str(haha))

        # 屏幕显示flip! 设定FPS为60
        pygame.display.flip()
        pygame.time.Clock().tick(60)


# 运行主程序
game_intro()

