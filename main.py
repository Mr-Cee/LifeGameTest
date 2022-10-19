import pygame
import sys
from pygame.locals import *
import pickle
import button
import locale
import os
import time
import json
import io

locale.setlocale(locale.LC_ALL, '')
locale.currency(12345, grouping=True)
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

# Variables
global PlayerCharacter
GameRunning = True
GameWindowWidth = 896
GameWindowHeight = 512
GameScreenWidth = 1920
GameScreenHeight = 1080
MenuState = "main"
PauseTicking = False
isClicked = False
Cheat1, Cheat2 = False, False

pygame.init()
screen = pygame.display.set_mode((GameWindowWidth, GameWindowHeight))
pygame.display.set_caption("Text RPG Game")

background_img = pygame.image.load(
    'Images/Backgrounds/Home.png').convert_alpha()
background_img = pygame.transform.scale(
    background_img,
    (background_img.get_width() / 2, background_img.get_height() / 2))

font = pygame.font.SysFont('Times New Roman', 18)

GameStartTicks = pygame.time.get_ticks()
TimerStartTicks = pygame.time.get_ticks()

clock = pygame.time.Clock()
fps = 60
# Define Colors
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow_BG = (255, 255, 205)
light_gray = (225, 225, 225)
light_orange = (255, 178, 102)
Font_ActiveTextColor = (0, 0, 0)
Font_InActiveTextColor = (125, 125, 125)

### Load Images ###

BTN_Empty_IMG = pygame.image.load(
    'Images/Icons/img_button_blank.png').convert_alpha()

# Load Food Images
BTN_beg_food_img = pygame.image.load(
    'Images/Icons/button_beg_food_active.png').convert_alpha()
food_hotdog = pygame.image.load(
    'Images/Icons/button_hotdog_inactive.png').convert_alpha()
BTN_hamburger_img = pygame.image.load(
    'Images/Icons/button_hamburger_inactive.png').convert_alpha()

# Load Bed Images
sleep_bed_img = pygame.image.load(
    'Images/Icons/button_sleep_active.png').convert_alpha()

# Load Cash Images
BTN_beg_img = pygame.image.load(
    'Images/Icons/button_beg_cash_active.png').convert_alpha()

# Load Housing Images
BTN_apartment_starter_img = pygame.image.load(
    'Images/Icons/img_apartment_starter_inactive.png').convert_alpha()
BTN_apartment_starter_img_active = pygame.image.load(
    'Images/Icons/img_apartment_starter_active.png').convert_alpha()
BTN_apartment_fancy_img_active = pygame.image.load(
    'Images/Icons/img_apartment_fancy_active.png').convert_alpha()
BTN_apartment_fancy_img_inactive = pygame.image.load(
    'Images/Icons/img_apartment_fancy_inactive.png').convert_alpha()
BTN_basic_condo_img = pygame.image.load(
    'Images/Icons/img_button_blank.png').convert_alpha()

# Load Job Buttons
BTN_test_job_img = pygame.image.load(
    'Images/Icons/img_blank_button.png').convert_alpha()
BTN_Fast_food_Worker_inactive_img = pygame.image.load(
    'Images/Icons/img_job_fast_food_worker_inactive.png').convert_alpha()
BTN_Fast_food_Worker_active_img = pygame.image.load(
    'Images/Icons/img_job_fast_food_worker_active.png').convert_alpha()
BTN_job_sales_associate_active_img = pygame.image.load(
    'Images/Icons/img_job_sales_associate_active.png').convert_alpha()
BTN_job_sales_associate_inactive_img = pygame.image.load(
    'Images/Icons/img_job_sales_associate_inactive.png').convert_alpha()

# load GUI icons
Options_img = pygame.image.load('Images/Icons/gear.png').convert_alpha()
Shop_img = pygame.image.load('Images/Icons/shop.png').convert_alpha()
Jobs_img = pygame.image.load('Images/Icons/jobs.png').convert_alpha()
Housing_img = pygame.image.load('Images/Icons/housing.png').convert_alpha()
Home_button_img = pygame.image.load(
    'Images/Icons/home_button.png').convert_alpha()

# Player Variables
DayCount = 0
DayLength = 5
NewDay = False

# Home Variables
CurrentLiving = "Homeless"
LivingID = 0
LivingIDList = {
    0: "Homeless",
    1: "Basic Apartment",
    2: "Fancy Apartment",
    3: "Basic Condo",
    4: "Fancy Condo",
    5: "Basic House",
    6: "Fancy House",
    7: "Small Mansion",
    8: "Large Mansion"
}
LivingBools = {
    int(0): True,
    int(1): False,
    int(2): False,
    int(3): False,
    int(4): False,
    int(5): False,
    int(6): False,
    int(7): False,
    int(8): False
}
LivingIDCost = {
    0: 0,
    1: 500,
    2: 1500,
    3: 5000,
    4: 20000,
    5: 100000,
    6: 500000,
    7: 2500000,
    8: 10000000
}
LivingButtonIMG = {
    0: BTN_test_job_img,
    1: BTN_apartment_starter_img,
    2: BTN_apartment_fancy_img_inactive,
    100: BTN_apartment_starter_img,
    101: BTN_apartment_starter_img_active,
    102: BTN_apartment_fancy_img_active
}

# Shop Variables
ShopID = 0
HasFood = False
ShopList = {0: "Beg for Food",
            1: "Corn Dog",
            2: "Burger",
            3: "Fried Chicken",
            4: "Spaghetti",
            5: "Lasagna",
            6: "Steak"}

ShopListCost = {0: 0,
                1: 3,
                2: 10,
                3: 50,
                4: 200,
                5: 1000,
                6: 5000}
ShopFoodListUnlockCost = {0: 0,
                          1: 100,
                          2: 5000,
                          3: 10000,
                          4: 50000,
                          5: 100000,
                          6: 500000}
ShopFoodListUnlockBools = {0: True,
                           1: False,
                           2: False,
                           3: False,
                           4: False,
                           5: False,
                           6: False}
ShopListHPIncrease = {0: 5,
                      1: 8,
                      2: 11,
                      3: 14,
                      4: 17,
                      5: 20,
                      6: 23
                      }
ShopListFoodIncrease = {0: 10,
                        1: 15,
                        2: 20,
                        3: 25,
                        4: 30,
                        5: 35,
                        6: 40
                        }
ShopListSleepDecrease = {0: 7,
                         1: 11,
                         2: 15,
                         3: 19,
                         4: 23,
                         5: 27,
                         6: 31
                         }
# Job Variables
CurrentJob = "Jobless"
HasJob = False
TestJob = False
JobID = 0
JobList = {
    0: "Jobless",
    1: "Fast Food Worker",
    2: "Sales Associate",
    3: "Mechanic",
    4: "Police Officer",
    # Degree Require for these:
    5: "Teacher",
    6: "Accountant",
    7: "Lawyer",
    8: "Doctor"
}
JobListIncome = {
    0: 0,
    1: 300,
    2: 500,
    3: 750,
    4: 1000,
    5: 1500,
    6: 3000,
    7: 7500,
    8: 10000
}
JobListBools = {
    0: True,
    1: False,
    2: False,
    3: False,
    4: False,
    5: False,
    6: False,
    7: False,
    8: False
}
JobListButtonIMG = {
    0: BTN_test_job_img,
    1: BTN_Fast_food_Worker_inactive_img,
    2: BTN_job_sales_associate_inactive_img,
    100: BTN_Fast_food_Worker_active_img,
    101: BTN_Fast_food_Worker_active_img,
    102: BTN_job_sales_associate_active_img
}

# Health Variables
PlayerHealthCD = 1.5
HP_Token = True
HP_Increase = 25
HP_Food_Decrease_Token = False
HP_Exhaustion_Decrease_Token = False
Sleep_Increase_HP = 8
HP_Decrease = .05
HP_tick = .025

# Sleep Variables
Sleep_Token = False
Sleep_Increase = 15
Sleep_tick = .025
Sleep_Work_Decrease = 10

# Food Variables
Food_Token = False
Food_Increase = 25
Food_tick = .025
Food_Work_Decrease = 10
Sleep_Decrease_Food = 5


class Person:

    def __init__(self, hp, maxhp, hp_auto_regen, food, max_food,
                 food_auto_regen, exhaustion, max_exhaustion,
                 exhaust_auto_regen, cash):
        try:
            with open('PlayerSaveFile.json') as data_file:
                PlayerData = json.load(data_file)
                self.__dict__ = PlayerData
                print("loaded Character")
        except (OSError, IOError):
            print("No save file found")
            print("Creating character now")
            self.hp = hp
            self.max_hp = maxhp
            self.hp_auto_regen = hp_auto_regen
            self.food = food
            self.max_food = max_food
            self.food_auto_regen = food_auto_regen
            self.exhaustion = exhaustion
            self.max_exhaustion = max_exhaustion
            self.exhaust_auto_regen = exhaust_auto_regen
            self.cash = cash


class DayBar:

    def __init__(self, x, y, DayCount, DayLength):
        self.x = x
        self.y = y
        self.DayCount = DayCount
        self.DayLength = DayLength
        self.seconds = 0

    def draw(self):
        global GameStartTicks
        global TimerStartTicks
        global DayCount
        global NewDay

        self.seconds = (pygame.time.get_ticks() - TimerStartTicks) / 1000
        NewDay = False
        if self.seconds > DayLength:
            TimerStartTicks = pygame.time.get_ticks()
            DayCount += 1
            NewDay = True
        ratio = self.seconds / DayLength
        pygame.draw.rect(screen, pygame.Color('yellow'),
                         (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, pygame.Color('orange'),
                         (self.x, self.y, 150 * ratio, 20))

        txt = font.render("Day: " + (str(DayCount)), True,
                          pygame.Color('black'))
        screen.blit(txt, (self.x + 2, self.y))


class HealthBar:

    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        # update with new health
        self.hp = hp
        # calculate health ratio
        ratio = PlayerCharacter.hp / PlayerCharacter.max_hp
        pygame.draw.rect(screen, yellow_BG, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

        titleratio = round(ratio * 100)
        txt = font.render(
            (str(round(PlayerCharacter.hp)) + "/" +
             str(PlayerCharacter.max_hp) + "   " + str(titleratio) + "%"),
            True, blue)
        screen.blit(txt, (self.x + 2, self.y))
        title = font.render("Health", True, pygame.Color('black'))
        screen.blit(title, (self.x + 50, self.y - 25))


class FoodBar:

    def __init__(self, x, y, food, max_food):
        self.x = x
        self.y = y
        self.food = food
        self.max_food = max_food

    def draw(self, food):
        # update with new health
        self.food = food
        # calculate health ratio
        ratio = PlayerCharacter.food / PlayerCharacter.max_food
        pygame.draw.rect(screen, yellow_BG, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, pygame.Color('red'),
                         (self.x, self.y, 150 * ratio, 20))

        titleratio = round(ratio * 100)
        txt = font.render(
            (str(round(PlayerCharacter.food)) + "/" +
             str(PlayerCharacter.max_food) + "   " + str(titleratio) + "%"),
            True, pygame.Color('black'))
        screen.blit(txt, (self.x + 2, self.y))
        title = font.render("Hunger", True, pygame.Color('black'))
        screen.blit(title, (self.x + 40, self.y - 25))


class ExhaustionBar:

    def __init__(self, x, y, exhaustion, max_exhaustion):
        self.x = x
        self.y = y
        self.exhaustion = exhaustion
        self.max_exhaustion = max_exhaustion

    def draw(self, exhaustion):
        # update with new health
        self.exhaustion = exhaustion
        # calculate health ratio
        ratio = PlayerCharacter.exhaustion / PlayerCharacter.max_exhaustion
        pygame.draw.rect(screen, yellow_BG, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, pygame.Color('orange'),
                         (self.x, self.y, 150 * ratio, 20))

        titleratio = round(ratio * 100)
        txt = font.render((str(round(PlayerCharacter.exhaustion)) + "/" +
                           str(PlayerCharacter.max_exhaustion) + "   " +
                           str(titleratio) + "%"), True, blue)
        screen.blit(txt, (self.x + 2, self.y))
        title = font.render("Exhaustion", True, pygame.Color('black'))
        screen.blit(title, (self.x + 25, self.y - 25))


""""        
Object Classes
"""


class House:

    def __init__(self, surface, x, y, image, size_x, size_y, HouseID,
                 HPTickMod, FoodTickMod, SleepTickMod):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface
        self.size_x = size_x
        self.size_y = size_y
        self.x = x
        self.y = y
        self.HouseID = HouseID
        self.HPTickMod = HPTickMod
        self.FoodTickMod = FoodTickMod
        self.SleepTickMod = SleepTickMod

    def draw(self):
        # get mouse position
        pos = pygame.mouse.get_pos()
        global isClicked
        global PlayerCharacter
        global LivingIDList
        global LivingIDCost
        global LivingButtonIMG
        global LivingID
        global CurrentLiving
        global Sleep_tick
        global HP_tick
        global Food_tick
        global HP_Increase
        global Food_Increase
        global Sleep_Increase

        font = pygame.font.SysFont(
            'Times New Roman',
            fit_text_to_width(LivingIDList[self.HouseID],
                              pygame.Color('black'), 105))
        subFont = pygame.font.SysFont(
            'Times New Roman',
            fit_text_to_width("${:,}".format(LivingIDCost[self.HouseID]),
                              pygame.Color('black'), 45))

        if PlayerCharacter.cash >= LivingIDCost[self.HouseID]:
            text = font.render(LivingIDList[self.HouseID], True,
                               Font_ActiveTextColor)
            subText = subFont.render(
                "${:,}".format(LivingIDCost[self.HouseID]), True,
                Font_ActiveTextColor)
        else:
            text = font.render(LivingIDList[self.HouseID], True,
                               Font_InActiveTextColor)
            subText = subFont.render(
                "${:,}".format(LivingIDCost[self.HouseID]), True,
                Font_InActiveTextColor)
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and isClicked == False:
                # code here
                isClicked = True
                if LivingID < self.HouseID and PlayerCharacter.cash >= LivingIDCost[
                    self.HouseID]:
                    LivingID = self.HouseID
                    CurrentLiving = LivingIDList[LivingID]
                    LivingBools[LivingID] = True
                    LivingBools[LivingID - 1] = False
                    PlayerCharacter.cash -= LivingIDCost[LivingID]
                    Sleep_tick *= self.SleepTickMod
                    HP_tick *= self.HPTickMod
                    Food_tick *= self.FoodTickMod
                    PlayerCharacter.max_hp += 10
                    PlayerCharacter.max_food += 10
                    PlayerCharacter.max_exhaustion += 15
                else:
                    fly_text = FlyText(150, 15, str("Need More Cash"),
                                       pygame.Color('black'))
                    fly_text_group.add(fly_text)
                    isClicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            isClicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
        text_rect = text.get_rect(center=(self.x + self.size_x / 2,
                                          self.y + 15))
        subText_rect = subText.get_rect(center=(self.x + self.size_x / 2,
                                                self.y + 35))
        self.surface.blit(text, text_rect)
        self.surface.blit(subText, subText_rect)


class Job:

    def __init__(self, surface, x, y, image, size_x, size_y, JobIDNumber):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # self.rect.center = (x + size_x/2, y + size_y/2)
        self.clicked = False
        self.surface = surface
        # self.buttonText = ButtonText
        self.size_x = size_x
        self.size_y = size_y
        self.x = x
        self.y = y
        self.CashIncome = JobListIncome[JobIDNumber]
        self.JobIDNumber = JobIDNumber

    def draw(self):
        # get mouse position
        pos = pygame.mouse.get_pos()
        global isClicked
        global CurrentJob
        global HasJob
        global JobID
        global JobList
        global JobListButtonIMG
        global PlayerCharacter
        global LivingID
        global JobListBools

        font = pygame.font.SysFont(
            'Times New Roman',
            fit_text_to_width(JobList[self.JobIDNumber], pygame.Color('black'),
                              105))
        subFont = pygame.font.SysFont(
            'Times New Roman',
            fit_text_to_width(
                str(JobListIncome[self.JobIDNumber]) + "/day",
                pygame.Color('black'), 45))

        if JobListBools[self.JobIDNumber]:
            text = font.render(JobList[self.JobIDNumber], True,
                               Font_ActiveTextColor)
            subText = subFont.render(
                str("${:,}".format(JobListIncome[self.JobIDNumber]) + "/day"),
                True, Font_ActiveTextColor)
        else:
            text = font.render(JobList[self.JobIDNumber], True,
                               Font_InActiveTextColor)
            subText = subFont.render(
                str("${:,}".format(JobListIncome[self.JobIDNumber]) + "/day"),
                True, Font_InActiveTextColor)

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and isClicked == False:
                # code here
                if HasJob == False and JobListBools[self.JobIDNumber] == False:
                    HasJob = True
                    JobID = self.JobIDNumber
                    CurrentJob = str(JobList[JobID])
                    JobListBools[self.JobIDNumber] = True
                elif HasJob and JobListBools[self.JobIDNumber] == False:
                    fly_text = FlyText(GameWindowWidth / 2,
                                       GameWindowHeight / 2,
                                       str("Please Leave Current Job"),
                                       pygame.Color('black'))
                    fly_text_group.add(fly_text)
                else:
                    HasJob = False
                    CurrentJob = "Jobless"
                    JobID = 0
                    JobListBools[self.JobIDNumber] = False

                isClicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            isClicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
        # text = font.render(LivingIDList[self.HouseID], True, Font_InActiveTextColor)
        text_rect = text.get_rect(center=(self.x + self.size_x / 2,
                                          self.y + 15))
        subText_rect = subText.get_rect(center=(self.x + self.size_x / 2,
                                                self.y + 35))
        self.surface.blit(text, text_rect)
        self.surface.blit(subText, subText_rect)

    def update(self):
        PlayerCharacter.cash += self.CashIncome


class Work:

    def __init__(self, surface, x, y, image, size_x, size_y):
        global JobID
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface
        self.size_x = size_x
        self.size_y = size_y
        self.x = x
        self.y = y
        self.CashIncome = JobListIncome[JobID] * .10
        self.JobIDNumber = JobID

    def draw(self):
        # get mouse position
        pos = pygame.mouse.get_pos()
        global isClicked
        global CurrentJob
        global HasJob
        global JobID
        global JobList
        global JobListButtonIMG
        global PlayerCharacter
        global LivingID
        global JobListBools

        font = pygame.font.SysFont(
            'Times New Roman',
            fit_text_to_width(
                "Work For: " + str("${:,}".format(self.CashIncome)),
                pygame.Color('black'), 105))

        if JobID > 0:
            text = font.render(
                "Work For: " + "${:,}".format(JobListIncome[JobID] * .10),
                True, Font_ActiveTextColor)
        else:
            text = font.render("Beg for $5", True, Font_ActiveTextColor)

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and isClicked == False:
                # code here
                if JobID == 0:
                    # Adds $5 to Player
                    PlayerCharacter.cash += 5
                    # Adjusts Food
                    if PlayerCharacter.food >= Food_Work_Decrease:
                        PlayerCharacter.food -= Food_Work_Decrease
                    else:
                        PlayerCharacter.food = 0
                    # Decrease Exhaustion
                    if PlayerCharacter.exhaustion >= Sleep_Work_Decrease:
                        PlayerCharacter.exhaustion -= Sleep_Work_Decrease
                    else:
                        PlayerCharacter.exhaustion = 0
                elif JobListBools[JobID]:
                    PlayerCharacter.cash += (JobListIncome[JobID] * .10)
                    # Adjusts Food
                    if PlayerCharacter.food >= Food_Work_Decrease:
                        PlayerCharacter.food -= Food_Work_Decrease
                    else:
                        PlayerCharacter.food = 0
                    # Decrease Exhaustion
                    if PlayerCharacter.exhaustion >= Sleep_Work_Decrease:
                        PlayerCharacter.exhaustion -= Sleep_Work_Decrease
                    else:
                        PlayerCharacter.exhaustion = 0

                isClicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            isClicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
        text_rect = text.get_rect(center=(self.x + self.size_x / 2,
                                          self.y + self.size_y / 2))
        self.surface.blit(text, text_rect)


class Food:
    def __init__(self, surface, x, y, image, size_x, size_y, ID, foodIncrease, HPIncrease, sleepDecrease):
        global ShopID
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface
        self.size_x = size_x
        self.size_y = size_y
        self.x = x
        self.y = y
        self.ID = ID
        self.foodIncrease = foodIncrease
        self.HPIncrease = HPIncrease
        self.sleepDecrease = sleepDecrease

    def draw(self):
        # get mouse position
        pos = pygame.mouse.get_pos()
        global isClicked
        global ShopList
        global ShopID

        font = pygame.font.SysFont('Times New Roman',
                                   fit_text_to_width("Eat " + ShopList[ShopID], pygame.Color('black'), 105))
        subfont = pygame.font.SysFont('Times New Roman',
                                      fit_text_to_width("${:,}".format(ShopListCost[ShopID]), pygame.Color('black'),
                                                        30))

        if ShopID > 0:
            text = font.render("Eat " + ShopList[ShopID], True, Font_ActiveTextColor)
            subtext = subfont.render("${:,}".format(ShopListCost[ShopID]), True, Font_ActiveTextColor)
        else:
            text = font.render("Beg for Food", True, Font_ActiveTextColor)
            subtext = subfont.render("${:,}".format(ShopListCost[ShopID]), True, Font_ActiveTextColor)

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and isClicked == False:
                # code here
                if PlayerCharacter.cash >= ShopListCost[ShopID]:
                    # Adjusts Food
                    if PlayerCharacter.max_food - PlayerCharacter.food < self.foodIncrease:
                        PlayerCharacter.food = PlayerCharacter.max_food
                    else:
                        PlayerCharacter.food += self.foodIncrease

                    # Adjusts Health
                    if PlayerCharacter.max_hp - PlayerCharacter.hp < self.HPIncrease:
                        PlayerCharacter.hp = PlayerCharacter.max_hp
                    else:
                        PlayerCharacter.hp += self.HPIncrease

                    # Decrease Exhaustion
                    if PlayerCharacter.exhaustion > self.sleepDecrease:
                        PlayerCharacter.exhaustion -= self.sleepDecrease
                    else:
                        PlayerCharacter.exhaustion = 0

                    PlayerCharacter.cash -= ShopListCost[ShopID]
                    isClicked = True
                else:
                    fly_text = FlyText(150, 15, str("Need More Cash"), pygame.Color('black'))
                    fly_text_group.add(fly_text)
                    isClicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            isClicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
        # text = font.render(LivingIDList[self.HouseID], True, Font_InActiveTextColor)
        text_rect = text.get_rect(center=(self.x + self.size_x / 2, self.y + 15))
        subText_rect = subtext.get_rect(center=(self.x + self.size_x / 2, self.y + 35))
        self.surface.blit(text, text_rect)
        self.surface.blit(subtext, subText_rect)


class Sleep:
    def __init__(self, surface, x, y, image, size_x, size_y):
        global ShopID
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface
        self.size_x = size_x
        self.size_y = size_y
        self.x = x
        self.y = y

    def draw(self):
        # get mouse position
        pos = pygame.mouse.get_pos()
        global isClicked
        global Sleep_Increase_HP
        global Sleep_Increase
        global Sleep_Decrease_Food

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and isClicked == False:
                # code here
                # Adjusts Exhaustion
                print(Sleep_Increase)
                if PlayerCharacter.max_exhaustion - PlayerCharacter.exhaustion < Sleep_Increase:
                    PlayerCharacter.exhaustion = PlayerCharacter.max_exhaustion
                else:
                    PlayerCharacter.exhaustion += Sleep_Increase

                # Adjusts Health
                if PlayerCharacter.max_hp - PlayerCharacter.hp < Sleep_Increase_HP:
                    PlayerCharacter.hp = PlayerCharacter.max_hp
                else:
                    PlayerCharacter.hp += Sleep_Increase_HP

                # Decrease Food
                if PlayerCharacter.food > Sleep_Decrease_Food:
                    PlayerCharacter.food -= Sleep_Decrease_Food
                else:
                    PlayerCharacter.food = 0

                isClicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            isClicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
        font = pygame.font.SysFont('Times New Roman', fit_text_to_width("Sleep", pygame.Color('black'), 105))
        text = font.render("Sleep", True, Font_ActiveTextColor)
        text_rect = text.get_rect(center=(self.x + self.size_x / 2, self.y + 15))
        self.surface.blit(text, text_rect)


class ShopFood:
    def __init__(self, surface, x, y, image, size_x, size_y, FoodID):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface
        self.size_x = size_x
        self.size_y = size_y
        self.x = x
        self.y = y
        self.FoodID = FoodID

    def draw(self):
        # get mouse position
        pos = pygame.mouse.get_pos()
        global isClicked
        global PlayerCharacter
        global ShopID
        global ShopList
        global ShopListCost
        global ShopFoodListUnlockCost
        global ShopFoodListUnlockBools
        global HasFood

        font = pygame.font.SysFont('Times New Roman', 18)
        subFont = pygame.font.SysFont('Times New Roman', 15)

        if PlayerCharacter.cash >= ShopFoodListUnlockCost[self.FoodID] or ShopFoodListUnlockBools[self.FoodID]:
            if ShopID == 0 or ShopID == self.FoodID:
                text = font.render(ShopList[self.FoodID], True, Font_ActiveTextColor)
                if ShopFoodListUnlockBools[self.FoodID]:
                    subText = subFont.render("Unlocked", True, Font_ActiveTextColor)
                else:
                    subText = subFont.render("${:,}".format(ShopFoodListUnlockCost[self.FoodID]), True, Font_ActiveTextColor)
            else:
                text = font.render(ShopList[self.FoodID], True, Font_InActiveTextColor)
                if ShopFoodListUnlockBools[self.FoodID]:
                    subText = subFont.render("Unlocked", True, Font_InActiveTextColor)
                else:
                    subText = subFont.render("${:,}".format(ShopFoodListUnlockCost[self.FoodID]), True, Font_InActiveTextColor)
        else:
            text = font.render(ShopList[self.FoodID], True, Font_InActiveTextColor)
            if ShopFoodListUnlockBools[self.FoodID]:
                subText = subFont.render("Unlocked", True, Font_InActiveTextColor)
            else:
                subText = subFont.render("${:,}".format(ShopFoodListUnlockCost[self.FoodID]), True, Font_InActiveTextColor)
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and isClicked == False:
                # code here
                isClicked = True

                if not HasFood and ShopID == 0 or not HasFood and ShopFoodListUnlockBools[self.FoodID]:
                    if PlayerCharacter.cash >= ShopFoodListUnlockCost[self.FoodID] or ShopFoodListUnlockBools[self.FoodID]:
                        HasFood = True
                        ShopID = self.FoodID
                        if not ShopFoodListUnlockBools[self.FoodID]:
                            ShopFoodListUnlockBools[self.FoodID] = True
                            PlayerCharacter.cash -= ShopFoodListUnlockCost[self.FoodID]
                    else:
                        fly_text = FlyText(165, 20, str("Not Enough Cash"), pygame.Color('black'))
                        fly_text_group.add(fly_text)
                elif HasFood and ShopID != self.FoodID:
                    fly_text = FlyText(GameWindowWidth / 2, 100, str("Please uncheck your current food"), pygame.Color('black'))
                    fly_text_group.add(fly_text)
                else:
                    HasFood = False
                    ShopID = 0

        if pygame.mouse.get_pressed()[0] == 0:
            isClicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
        text_rect = text.get_rect(center=(self.x + self.size_x / 2, self.y + 15))
        subText_rect = subText.get_rect(center=(self.x + self.size_x / 2, self.y + 35))
        self.surface.blit(text, text_rect)
        self.surface.blit(subText, subText_rect)


"""        
GUI Classes
"""


class Button_Options:

    def __init__(self, surface, x, y, image, size_x, size_y):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface

    def draw(self):
        # get mouse position
        pos = pygame.mouse.get_pos()
        global MenuState
        global isClicked

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and isClicked == False:
                if not MenuState == "options":
                    MenuState = "options"
                else:
                    MenuState = "main"
                isClicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            isClicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))


class Button_Shop:

    def __init__(self, surface, x, y, image, size_x, size_y):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface

    def draw(self):
        # get mouse position
        pos = pygame.mouse.get_pos()
        global MenuState
        global isClicked
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and isClicked == False:
                if not MenuState == "shop":
                    MenuState = "shop"
                else:
                    MenuState = "main"
                isClicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            isClicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))


class Button_Jobs:

    def __init__(self, surface, x, y, image, size_x, size_y):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface

    def draw(self):
        # get mouse position
        pos = pygame.mouse.get_pos()
        global MenuState
        global isClicked
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and isClicked == False:
                if not MenuState == "jobs":
                    MenuState = "jobs"
                else:
                    MenuState = "main"
                isClicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            isClicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))


class Button_Housing:

    def __init__(self, surface, x, y, image, size_x, size_y):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface

    def draw(self):
        # get mouse position
        pos = pygame.mouse.get_pos()
        global MenuState
        global isClicked
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and isClicked == False:
                if not MenuState == "housing":
                    MenuState = "housing"
                else:
                    MenuState = "main"
                isClicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            isClicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))


class Button_Home:

    def __init__(self, surface, x, y, image, size_x, size_y):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface

    def draw(self):
        # get mouse position
        pos = pygame.mouse.get_pos()
        global MenuState
        global isClicked
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and isClicked == False:
                if not MenuState == "main":
                    MenuState = "main"
                isClicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            isClicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))


class FlyText(pygame.sprite.Sprite):

    def __init__(self, x, y, text, colour):
        # def __init__(self, x, y, text, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(text, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # move damage text up
        # self.rect.y -= .5
        # delete the text after a few seconds

        self.counter += 1
        if self.counter > 60:
            self.kill()


def draw_BG():
    screen.fill(light_gray)
    # screen.blit(background_img,(0, 0))
    # GameWindow.fill(light_gray)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_text_centered(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    text_rect = img.get_rect(center=(x, y))
    screen.blit(img, text_rect)


def fit_text_to_width(text, color, pixels, font_face=None):
    font = pygame.font.SysFont(font_face, pixels * 3 // len(text))
    text_surface = font.render(text, True, color)
    size = text_surface.get_size()
    size = (pixels, int(size[1] * pixels / size[0]))
    # return pygame.transform.scale(text_surface, size)
    return size[1]


def CreateCharacter():
    global PlayerCharacter
    PlayerCharacter = Person(100, 100, 0, 100, 100, 0, 100, 100, 0, 0)
    return PlayerCharacter


def LoadGame():
    global PlayerCharacter
    global CurrentLiving
    global GameWindowWidth
    global GameWindowHeight
    global screen
    global HP_tick
    global Food_tick
    global Sleep_tick
    global HP_Increase
    global Sleep_Increase
    global Food_Increase
    global DayCount
    global DayLength
    global HasJob
    global JobListBools
    global JobID
    global CurrentJob
    global LivingID
    global LivingBools
    global ShopID
    global Sleep_Increase_HP
    global Sleep_Decrease_Food
    global HasFood
    global ShopFoodListUnlockBools

    PlayerCharacter = CreateCharacter()

    try:
        with open('GameSaveFile.json') as data_file:
            data = json.load(data_file)
        CurrentLiving = data["currentLivingSpace"]
        GameWindowHeight = data["resolution_y"]
        GameWindowWidth = data["resolution_x"]
        HP_tick = data["HP_tick"]
        Food_tick = data["Food_tick"]
        Sleep_tick = data["Sleep_tick"]
        HP_Increase = data["HP_Increase"]
        Food_Increase = data["Food_Increase"]
        Sleep_Increase = data["Sleep_Increase"]
        DayCount = data["Day_Count"]
        DayLength = data["Day_Length"]
        HasJob = data["HasJob"]
        JobID = data["JobID"]
        JobListBools = data["JobListBools"]
        CurrentJob = data["CurrentJob"]
        LivingID = data["LivingID"]
        LivingBools = data["LivingBools"]
        ShopID = data["ShopID"]
        HasFood = data["HasFood"]
        Sleep_Increase_HP = data["Sleep_Increase_HP"]
        Sleep_Decrease_Food = data["Sleep_Decrease_Food"]
        ShopFoodListUnlockBools = data["ShopFoodListUnlockBools"]

        # screen = pygame.display.set_mode((GameWindowWidth, GameWindowHeight))
        print("Loaded Variables")
    except:
        print("Failed to Load Variables")

    try:
        LivingBools = {int(k): v for k, v in LivingBools.items()}
        JobListBools = {int(k): v for k, v in JobListBools.items()}
        ShopFoodListUnlockBools = {int(k): v for k, v in ShopFoodListUnlockBools.items()}
        print("Loaded Dictionary Variables")
    except:
        print("Failed to change dictionary")


def SaveGame():
    print("Creating Save File Now")
    data = {
        "resolution_x": GameWindowWidth,
        "resolution_y": GameWindowHeight,
        "currentLivingSpace": CurrentLiving,
        "HP_tick": HP_tick,
        "Food_tick": Food_tick,
        "Sleep_tick": Sleep_tick,
        "HP_Increase": HP_Increase,
        "Food_Increase": Food_Increase,
        "Sleep_Increase": Sleep_Increase,
        "Sleep_Decrease_Food": Sleep_Decrease_Food,
        "Sleep_Increase_HP": Sleep_Increase_HP,
        "Day_Count": DayCount,
        "Day_Length": DayLength,
        "HasJob": HasJob,
        "JobListBools": JobListBools,
        "JobID": JobID,
        "CurrentJob": CurrentJob,
        "LivingID": LivingID,
        "LivingBools": LivingBools,
        "ShopID": ShopID,
        "HasFood": HasFood,
        "ShopFoodListUnlockBools": ShopFoodListUnlockBools

    }
    with io.open('GameSaveFile.json', 'w', encoding='utf8') as outfile:
        str_ = json.dumps(data,
                          indent=4,
                          separators=(',', ': '),
                          ensure_ascii=False)
        outfile.write(to_unicode(str_))

    with io.open('PlayerSaveFile.json', 'w', encoding='utf8') as outfile:
        PlayerSaveStr_ = json.dumps(PlayerCharacter.__dict__,
                                    indent=4,
                                    separators=(',', ': '),
                                    ensure_ascii=False)
        outfile.write(to_unicode(PlayerSaveStr_))


def ResetStats():
    global DayCount
    global LivingID
    global LivingBools
    global JobID
    global JobListBools
    global ShopID
    global CurrentJob
    global CurrentLiving
    PlayerCharacter.hp = 100
    PlayerCharacter.max_hp = 100
    PlayerCharacter.food = 100
    PlayerCharacter.max_food = 100
    PlayerCharacter.exhaustion = 100
    PlayerCharacter.max_exhaustion = 100
    PlayerCharacter.cash = 0
    DayCount = 0
    CurrentLiving = "Homeless"
    CurrentJob = "Jobless"
    LivingID = 0
    LivingBools = {
        int(0): True,
        int(1): False,
        int(2): False,
        int(3): False,
        int(4): False,
        int(5): False,
        int(6): False,
        int(7): False,
        int(8): False
    }
    JobID = 0
    JobListBools = {
        0: True,
        1: False,
        2: False,
        3: False,
        4: False,
        5: False,
        6: False,
        7: False,
        8: False
    }
    ShopID = 0


LoadGame()

fly_text_group = pygame.sprite.Group()

# Creates Progress Bars
player_health_bar = HealthBar(GameWindowWidth / 6 - 50,
                              GameWindowHeight - GameWindowHeight + 75,
                              PlayerCharacter.hp, PlayerCharacter.max_hp)
player_food_bar = FoodBar(GameWindowWidth / 2 - 50,
                          GameWindowHeight - GameWindowHeight + 75,
                          PlayerCharacter.food, PlayerCharacter.max_food)
player_exhaustion_bar = ExhaustionBar(GameWindowWidth / 6 * 5 - 75,
                                      GameWindowHeight - GameWindowHeight + 75,
                                      PlayerCharacter.exhaustion,
                                      PlayerCharacter.max_exhaustion)
DayProgressBar = DayBar(GameWindowWidth - 155, 5, DayCount, DayLength)

# Creates Sleep Buttons
BTN_Sleep = Sleep(screen, player_exhaustion_bar.x, player_exhaustion_bar.y + 50, BTN_Empty_IMG, 150, 50)

# Creates Cash buttons
Work_button = Work(screen, player_health_bar.x, player_health_bar.y + 60,
                   BTN_Empty_IMG, 150, 50)

# Creates the Food Buttons
BTN_Food_Beg = Food(screen, player_food_bar.x, player_food_bar.y + 60, BTN_Empty_IMG, 150, 50, 0,
                    ShopListFoodIncrease[ShopID], ShopListHPIncrease[ShopID], ShopListSleepDecrease[ShopID])
BTN_Food_Corndog = ShopFood(screen, 50, 100, BTN_Empty_IMG, 150, 50, 1)
BTN_Food_Burger = ShopFood(screen, 50, 160, BTN_Empty_IMG, 150, 50, 2)
BTN_Food_Fried_Chicken = ShopFood(screen, 50, 220, BTN_Empty_IMG, 150, 50, 3)
BTN_Food_Spaghetti = ShopFood(screen, 50, 280, BTN_Empty_IMG, 150, 50, 4)
BTN_Food_Lasagna = ShopFood(screen, 50, 340, BTN_Empty_IMG, 150, 50, 5)
BTN_Food_Steak = ShopFood(screen, 50, 400, BTN_Empty_IMG, 150, 50, 6)

# Creates House buttons
BTN_apartment_starter = House(screen, player_health_bar.x,
                              player_health_bar.y + 25, BTN_Empty_IMG, 150, 50,
                              1, .95, .95, .75)
BTN_apartment_advanced = House(screen, player_health_bar.x,
                               player_health_bar.y + 25, BTN_Empty_IMG, 150,
                               50, 2, .95, .95, .75)
BTN_Housing_Condo_Basic = House(screen, player_health_bar.x,
                                player_health_bar.y + 25, BTN_Empty_IMG, 150,
                                50, 3, .95, .95, .75)
BTN_Housing_Condo_Fancy = House(screen, player_health_bar.x,
                                player_health_bar.y + 25, BTN_Empty_IMG, 150,
                                50, 4, .95, .95, .75)
BTN_Housing_House_Basic = House(screen, player_health_bar.x,
                                player_health_bar.y + 25, BTN_Empty_IMG, 150,
                                50, 5, .95, .95, .75)
BTN_Housing_House_Fancy = House(screen, player_health_bar.x,
                                player_health_bar.y + 25, BTN_Empty_IMG, 150,
                                50, 6, .95, .95, .75)
BTN_Housing_Mansion_Small = House(screen, player_health_bar.x,
                                  player_health_bar.y + 25, BTN_Empty_IMG, 150,
                                  50, 7, .95, .95, .75)
BTN_Housing_Mansion_Large = House(screen, player_health_bar.x,
                                  player_health_bar.y + 25, BTN_Empty_IMG, 150,
                                  50, 8, .95, .95, .75)

# Creates Job Buttons
BTN_Fast_Food_Job = Job(screen, 100, 40, BTN_Empty_IMG, 150, 50, 1)
BTN_Job_Sales_Associate = Job(screen, 100, 100, BTN_Empty_IMG, 150, 50, 2)
BTN_Job_Mechanic = Job(screen, 100, 160, BTN_Empty_IMG, 150, 50, 3)
BTN_Job_Police_Officer = Job(screen, 100, 220, BTN_Empty_IMG, 150, 50, 4)
BTN_Job_Teacher = Job(screen, 100, 280, BTN_Empty_IMG, 150, 50, 5)
BTN_Job_Accountant = Job(screen, 100, 340, BTN_Empty_IMG, 150, 50, 6)
BTN_Job_Lawyer = Job(screen, 100, 400, BTN_Empty_IMG, 150, 50, 7)
BTN_Job_Doctor = Job(screen, 100, 460, BTN_Empty_IMG, 150, 50, 8)

# Creates UI Buttons
BTN_Options = Button_Options(screen, GameWindowWidth - 55,
                             GameWindowHeight - 55, Options_img, 50, 50)
BTN_Shop = Button_Shop(screen, player_food_bar.x, player_food_bar.y + 275,
                       Shop_img, 150, 50)
BTN_Jobs = Button_Jobs(screen, player_health_bar.x, player_health_bar.y + 275,
                       Jobs_img, 150, 50)
BTN_Housing = Button_Housing(screen, player_exhaustion_bar.x,
                             player_health_bar.y + 275, Housing_img, 150, 50)
BTN_Home = Button_Home(screen, 5, 5, Home_button_img, 50, 50)

while GameRunning:

    clock.tick(fps)
    draw_BG()

    if not MenuState == "GAME OVER":
        BTN_Options.draw()
    else:
        draw_text_centered("GAME OVER",
                           pygame.font.SysFont('Times New Roman', 50),
                           pygame.Color('black'), GameWindowWidth / 2, 35)

    ### Displays Main Screen ###

    # Menustates
    if MenuState == "main":
        if PlayerCharacter.hp > 0:
            if not PauseTicking:
                PlayerCharacter.hp -= HP_tick
        else:
            MenuState = "GAME OVER"
            ResetStats()

        if not PauseTicking:
            if PlayerCharacter.exhaustion > 0:
                PlayerCharacter.exhaustion -= Sleep_tick
            else:
                PlayerCharacter.hp -= HP_Decrease

            if PlayerCharacter.food > 0:
                PlayerCharacter.food -= Food_tick
            else:
                PlayerCharacter.hp -= HP_Decrease

        if NewDay:
            if JobListBools[1]:
                BTN_Fast_Food_Job.update()
            elif JobListBools[2]:
                BTN_Job_Sales_Associate.update()
            elif JobListBools[3]:
                BTN_Job_Mechanic.update()
            elif JobListBools[4]:
                BTN_Job_Police_Officer.update()
            elif JobListBools[5]:
                BTN_Job_Teacher.update()
            elif JobListBools[6]:
                BTN_Job_Accountant.update()
            elif JobListBools[7]:
                BTN_Job_Lawyer.update()
            elif JobListBools[8]:
                BTN_Job_Doctor.update()

        seconds = (pygame.time.get_ticks() -
                   GameStartTicks) / 1000  # calculate how many seconds
        if HP_Token:
            if seconds > PlayerHealthCD:  # if more than 10 seconds close the game
                if PlayerCharacter.max_hp - PlayerCharacter.hp > PlayerCharacter.hp_auto_regen:
                    PlayerCharacter.hp += PlayerCharacter.hp_auto_regen
                else:
                    PlayerCharacter.hp = PlayerCharacter.max_hp
                GameStartTicks = pygame.time.get_ticks()

        draw_text("Current Living Arrangements: " + CurrentLiving, font,
                  pygame.Color('black'), 15, 400)
        draw_text("Current Job: " + CurrentJob, font, pygame.Color('black'),
                  15, 425)
        # Draw Bars
        player_health_bar.draw(PlayerCharacter.hp)
        player_food_bar.draw(PlayerCharacter.food)
        player_exhaustion_bar.draw(PlayerCharacter.exhaustion)
        DayProgressBar.draw()
        BTN_Sleep.draw()
        # food_hotdog_button.draw()
        Work_button.draw()
        BTN_Food_Beg.draw()
        # food_hamburger_button.draw()
        BTN_Shop.draw()
        BTN_Jobs.draw()
        BTN_Housing.draw()
        draw_text_centered("Cash: " + "${:,}".format(PlayerCharacter.cash),
                           font, pygame.Color('black'), GameWindowWidth / 2,
                           15)
    elif MenuState == "shop":
        BTN_Home.draw()
        draw_text_centered("SHOP", pygame.font.SysFont('Times New Roman', 25),
                           pygame.Color('black'), GameWindowWidth / 2, 35)
        draw_text_centered("Cash: " + "${:,}".format(PlayerCharacter.cash),
                           font, pygame.Color('black'), GameWindowWidth / 2,
                           15)
        draw_text("Current Food: " + ShopList[ShopID], pygame.font.SysFont('Times New Roman', 20),
                           pygame.Color('black'), 100, 35)
        BTN_Food_Corndog.draw()
        BTN_Food_Burger.draw()
        BTN_Food_Fried_Chicken.draw()
        BTN_Food_Spaghetti.draw()
        BTN_Food_Lasagna.draw()
        BTN_Food_Steak.draw()

        draw_text_centered("Coming Soon",
                           pygame.font.SysFont('Times New Roman', 25),
                           pygame.Color('black'), GameWindowWidth / 2,
                           GameWindowHeight / 2)

    elif MenuState == "housing":
        BTN_Home.draw()

        draw_text_centered("Cash: " + "${:,}".format(PlayerCharacter.cash),
                           font, pygame.Color('black'), GameWindowWidth / 2,
                           15)
        draw_text("Housing", pygame.font.SysFont('Times New Roman', 25),
                  pygame.Color('black'), player_health_bar.x + 30,
                  player_health_bar.y - 10)
        pygame.draw.rect(screen, pygame.Color('black'),
                         pygame.Rect(GameWindowWidth / 2, 75, 350, 400), 4)
        pygame.draw.line(screen, pygame.Color('black'), (550, 125), (700, 125),
                         5)
        draw_text_centered("Current Stats",
                           pygame.font.SysFont('Times New Roman', 25),
                           pygame.Color('black'), 623, 100)
        draw_text("HP Decrease Rate: " + str(round(HP_tick * -1 * 60, 1)),
                  pygame.font.SysFont('Times New Roman', 20),
                  pygame.Color('black'), 475, 150)
        draw_text("Food Decrease Rate: " + str(round(Food_tick * -1 * 60, 1)),
                  pygame.font.SysFont('Times New Roman', 20),
                  pygame.Color('black'), 475, 175)
        draw_text("Sleep Decrease Rate: " + str(round(Sleep_tick * -1 * 60, 1)),
                  pygame.font.SysFont('Times New Roman', 20),
                  pygame.Color('black'), 475, 200)

        # Draws the next housing option available
        if LivingBools[0]:
            BTN_apartment_starter.draw()
        elif LivingBools[1]:
            BTN_apartment_advanced.draw()
        elif LivingBools[2]:
            BTN_Housing_Condo_Basic.draw()
        elif LivingBools[3]:
            BTN_Housing_Condo_Fancy.draw()
        elif LivingBools[4]:
            BTN_Housing_House_Basic.draw()
        elif LivingBools[5]:
            BTN_Housing_House_Fancy.draw()
        elif LivingBools[6]:
            BTN_Housing_Mansion_Small.draw()
        elif LivingBools[7]:
            BTN_Housing_Mansion_Large.draw()
        else:
            draw_text("No New Housing",
                      pygame.font.SysFont('Times New Roman', 25),
                      pygame.Color('black'), player_health_bar.x - 35,
                      player_health_bar.y + 25)

    elif MenuState == "jobs":
        BTN_Home.draw()
        draw_text("Current Job: " + CurrentJob, font, pygame.Color('black'),
                  200, 10)
        if LivingID == 0:
            draw_text_centered("You Need a place to live first!",
                               pygame.font.SysFont('Times New Roman', 25),
                               pygame.Color('black'), GameWindowWidth / 2,
                               GameWindowHeight / 2)
        if LivingID >= 1:
            BTN_Fast_Food_Job.draw()
        if LivingID >= 2:
            BTN_Job_Sales_Associate.draw()
        if LivingID >= 3:
            BTN_Job_Mechanic.draw()
        if LivingID >= 4:
            BTN_Job_Police_Officer.draw()
        if LivingID >= 5:
            BTN_Job_Teacher.draw()
        if LivingID >= 6:
            BTN_Job_Accountant.draw()
        if LivingID >= 7:
            BTN_Job_Lawyer.draw()
        if LivingID >= 8:
            BTN_Job_Doctor.draw()

    elif MenuState == "options":
        BTN_Home.draw()

    # Cautionary Text draw
    fly_text_group.update()
    fly_text_group.draw(screen)

    # Cheat Codes
    if Cheat1 and Cheat2:
        PlayerCharacter.cash += 100000
        Cheat1, Cheat2 = False, False
    elif Cheat1:
        PlayerCharacter.cash += 100
        Cheat1, Cheat2 = False, False

    # Key Events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                SaveGame()
            if event.key == pygame.K_h:
                PlayerCharacter.hp_auto_regen += 10
            if event.key == pygame.K_p:
                if not PauseTicking:
                    PauseTicking = True
                else:
                    PauseTicking = False
            if event.key == pygame.K_m:
                if not MenuState == "GAME OVER":
                    if MenuState == "shop":
                        MenuState = "main"
                    else:
                        MenuState = "shop"
            if event.key == pygame.K_t:
                if HP_Token:
                    HP_Token = False
                else:
                    HP_Token = True
            if event.key == pygame.K_c:
                # PlayerCharacter.cash += 100
                Cheat1 = True

            if event.key == pygame.K_LSHIFT:
                Cheat2 = True
            '''       
            if event.key == pygame.K_ESCAPE:
                gameRunning = False
                SaveGame()
                pygame.quit()
                sys.exit()
            '''
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                if Cheat2:
                    Cheat2 = False
            if event.key == pygame.K_c:
                if Cheat1:
                    Cheat1 = False

        if event.type == QUIT:
            gameRunning = False
            SaveGame()
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False
    pygame.display.update()
pygame.quit()
