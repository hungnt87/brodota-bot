import os
import threading
import time

import pyautogui
import pydirectinput

import controller.global_variables as cgv
from controller.button import Button
from controller.filelog import logger
from controller.global_variables import global_event

path = cgv.PathManager()
REGION_HERO = (537, 125, 1158, 406)

REGION_SELL_HERO: tuple[int, int, int, int] = (662, 791, 704, 358)
CONFIDENCE = 0.8
GRAYSCALE: bool = True
number_winter_wyvern: int = 0
number_hood_wink: int = 1
number_dazzale: int = 0
need_WinterWyvern: int = 1
need_Hoodwink: int = 1
need_Dazzale: int = 1
need_Luna = 1
need_Windranger = 1
need_Oracle = 1
need_TrollWarlord = 1
need_Morphling = 1
need_WitchDoctor = 1
need_DarkWillow = 1
need_Clinkz = 1
need_Sniper = 5
need_Snapfire = 5
need_DrowRanger = 5
need_TemplarAssassin = 5
need_Zet = 5

previous_hero = dict()


class Hero:
    img = None
    img_lv1 = None

    def __init__(self, name: str, number: int = 0, need_buy: int = 0):
        self.name = name
        self.img = self._get_hero_img(name)
        self.img_lv1 = self._get_hero_img_lv1(name)
        self.number = number
        self.need_buy = need_buy
        self.region = REGION_HERO
        self.region_sell = REGION_SELL_HERO
        self.confidence = CONFIDENCE
        self.grayscale = GRAYSCALE

    def _get_hero_img(self, para_name):
        # global HERO_IMG
        if self.img is None:
            file_name = para_name + ".png"
            self.img = path.get_absolute_path(
                os.path.join("assets", "img", "hero", file_name)
            )
        return self.img

    def _get_hero_img_lv1(self, para_name):
        # global HERO_IMG
        if self.img_lv1 is None:
            file_name = para_name + "_lv1.png"
            self.img_lv1 = path.get_absolute_path(
                os.path.join("assets", "img", "hero", file_name)
            )
        return self.img_lv1

    def reset_hero_number(self):
        self.number = 0

    def buy(self):
        if global_event.check_event():
            return False
        # logger.debug("Bat dau tim hero {}".format(self.name))
        try:
            res_center = pyautogui.locateCenterOnScreen(
                self.img, minSearchTime=1, confidence=self.confidence, region=self.region, grayscale=self.grayscale, )
            # res_center = pyautogui.center(res)
            # pydirectinput.moveTo(res_center.x, res_center.y)
            # pydirectinput.click(res_center[0], res_center[1])
            # pydirectinput.moveTo(201, 213)
            # logger.debug("Tim thay hinh anh {}".format(self.img))
            return res_center
        except pyautogui.ImageNotFoundException:
            # logger.debug("Khong tim thay hinh anh {}".format(self.img))
            return False
        except Exception as e:
            logger.error(e)
            return None

    def buy_hero(self):
        if global_event.check_event():
            return False
        logger.debug("Bat dau tim hero {}".format(self.name))
        count_buy = self.need_buy - self.number

        if count_buy > 0:
            # logger.debug(f"Con {count_buy} {self.name} can mua")
            try:
                res_center = pyautogui.locateCenterOnScreen(
                    self.img, minSearchTime=1.5, confidence=self.confidence, region=self.region,
                    grayscale=self.grayscale, )
                previous_hero[res_center] = self
                return True
            except pyautogui.ImageNotFoundException:
                # logger.debug("Khong tim thay hinh anh {}".format(self.img))
                return False
            except Exception as e:
                logger.error(e)
                return None

    def check_hero(self):
        if global_event.check_event():
            return False
        try:
            if global_event.check_event():
                return False
            pyautogui.locateCenterOnScreen(
                self.img, confidence=self.confidence, region=REGION_HERO, grayscale=self.grayscale, )
            return True
        except pyautogui.ImageNotFoundException:
            return False
        except Exception as e:
            logger.error(e)
            return False

    def sell_hero(self):
        if global_event.check_event():
            return False
        global REGION_SELL_HERO
        try:
            res_center = pyautogui.locateCenterOnScreen(
                self.img_lv1, confidence=self.confidence, region=self.region_sell, grayscale=self.grayscale, )
            pydirectinput.rightClick(res_center.x, res_center.y)
            time.sleep(0.5)
            pydirectinput.click(res_center.x + 20, res_center.y)
            pydirectinput.moveTo(213, 201)
            logger.debug(f"Ban thanh cong hero {self.name}")
            time.sleep(0.5)
            self.number = 10
            return True
        except pyautogui.ImageNotFoundException:
            logger.debug(f"Khong co hero  {self.name} de ban")
            return False
        except Exception as e:
            logger.error(e)
            return False


def buy_all_previous_hero():
    if global_event.check_event():
        return False
    pydirectinput.moveTo(213, 201)
    global previous_hero
    if previous_hero:
        logger.debug("Ban dang mua hero ")
        for key, value in list(previous_hero.items()):
            check_sell_hero(value)
            pydirectinput.click(key[0], key[1])
            if Button.check_money() is True:
                logger.info(f"Ban da mua thanh cong 1 {value.name}")
                value.number = value.number + 1
                cgv.count_of_buy += 1
                del previous_hero[key]
            else:
                look_region = (key[0], key[1], 267, 312)
                cgv.set_money(False)
                if Button.click_lock(value.name, look_region) is True:
                    # del previous_item[key]
                    logger.debug("Khong du tien, Khoa hero")
                else:
                    del previous_hero[key]

    else:
        logger.debug("Khong co hero khoa o round truoc")
    pydirectinput.moveTo(213, 201)


WinterWyvern = Hero(name="WinterWyvern", number=number_winter_wyvern, need_buy=need_WinterWyvern)

HoodWink = Hero(name="Hoodwink", number=number_hood_wink, need_buy=need_Hoodwink)
Dazzale = Hero(name="Dazzale", number=number_dazzale, need_buy=need_Dazzale)
# hero lv2

Luna = Hero(name="Luna", need_buy=1)

Windranger = Hero(name="Windranger", need_buy=1)

Oracle = Hero(name="Oracle", need_buy=1)

TrollWarlord = Hero(name="TrollWarlord", need_buy=1)
Morphling = Hero(name="Morphling", need_buy=1)

# hero lv3
WitchDoctor = Hero(name="WitchDoctor", need_buy=1)
DarkWillow = Hero(name="DarkWillow", need_buy=1)
Mirana = Hero(name="Mirana", need_buy=1)
Clinkz = Hero(name="Clinkz", need_buy=1)

# hero lv4
Sniper = Hero(name="Sniper", need_buy=5)
Snapfire = Hero(name="Snapfire", need_buy=5)
# hero lv5
DrowRanger = Hero(name="DrowRanger", need_buy=5)
TemplarAssassin = Hero(name="TemplarAssassin", need_buy=5)
Zet = Hero(name="Zet", need_buy=5)
DragonKnight = Hero(name="DragonKnight", need_buy=5)


def check_sell_hero(hero: Hero):
    if global_event.check_event():
        return False
    # slot 1
    if hero.name == Mirana.name:
        Dazzale.sell_hero()
    elif hero.name == Sniper.name:
        Dazzale.sell_hero()
        Mirana.sell_hero()

    # slot 2
    elif hero.name == Morphling.name:
        Oracle.sell_hero()
    elif hero.name == Snapfire.name:
        Oracle.sell_hero()
        Morphling.sell_hero()

    # slot 3
    elif hero.name == DarkWillow.name:
        Windranger.sell_hero()
    elif hero.name == DragonKnight.name:
        DarkWillow.sell_hero()
        Windranger.sell_hero()

    # slot 4
    elif hero.name == Luna.name:
        HoodWink.sell_hero()
    elif hero.name == DrowRanger.name:
        HoodWink.sell_hero()
        Luna.sell_hero()


    # slot 5
    elif hero.name == WitchDoctor.name:
        WinterWyvern.sell_hero()
    elif hero.name == TemplarAssassin.name:
        WinterWyvern.sell_hero()
        WitchDoctor.sell_hero()

    # slot 6
    elif hero.name == Clinkz.name:
        # logger.debug("Ban Clinkz")
        TrollWarlord.sell_hero()
    elif hero.name == Zet.name:
        Clinkz.sell_hero()
        TrollWarlord.sell_hero()


def buy_all_hero(round_number):
    if global_event.check_event():
        return False
    logger.info(f"Bat dau mua hero in round: {round_number}")
    if cgv.check_money() is False:
        logger.debug("Khong du tien, next round")
        return None
    thread_buy_dazzale = threading.Thread(target=Dazzale.buy_hero, args=())
    thread_buy_oracle = threading.Thread(target=Oracle.buy_hero, args=())
    thread_buy_hoodwink = threading.Thread(target=HoodWink.buy_hero, args=())
    thread_buy_winter_wyvern = threading.Thread(target=WinterWyvern.buy_hero, args=())
    thread_buy_luna = threading.Thread(target=Luna.buy_hero, args=())
    thread_buy_troll_warlord = threading.Thread(target=TrollWarlord.buy_hero, args=())
    thread_buy_morphling = threading.Thread(target=Morphling.buy_hero, args=())
    thread_buy_windranger = threading.Thread(target=Windranger.buy_hero, args=())
    thread_buy_mirana = threading.Thread(target=Mirana.buy_hero, args=())
    thread_buy_dark_willow = threading.Thread(target=DarkWillow.buy_hero, args=())
    thread_buy_clinkz = threading.Thread(target=Clinkz.buy_hero, args=())
    thread_buy_witch_doctor = threading.Thread(target=WitchDoctor.buy_hero, args=())
    thread_buy_sniper = threading.Thread(target=Sniper.buy_hero, args=())
    thread_buy_snapfire = threading.Thread(target=Snapfire.buy_hero, args=())
    thread_buy_drow_ranger = threading.Thread(target=DrowRanger.buy_hero, args=())
    thread_buy_templar_assassin = threading.Thread(target=TemplarAssassin.buy_hero, args=())
    thread_buy_zet = threading.Thread(target=Zet.buy_hero, args=())
    thread_buy_dragon_knight = threading.Thread(target=DragonKnight.buy_hero, args=())

    if round_number <= 3:
        thread_buy_dazzale.start()
        thread_buy_oracle.start()
        thread_buy_hoodwink.start()
        thread_buy_winter_wyvern.start()
        thread_buy_luna.start()
        thread_buy_troll_warlord.start()
        thread_buy_morphling.start()
        thread_buy_windranger.start()
        thread_buy_dazzale.join()
        thread_buy_oracle.join()
        thread_buy_hoodwink.join()
        thread_buy_winter_wyvern.join()
        thread_buy_luna.join()
        thread_buy_troll_warlord.join()
        thread_buy_morphling.join()
        thread_buy_windranger.join()
    elif round_number < 10:
        # start
        thread_buy_dazzale.start()
        thread_buy_oracle.start()
        thread_buy_hoodwink.start()
        thread_buy_winter_wyvern.start()
        thread_buy_luna.start()
        thread_buy_troll_warlord.start()
        thread_buy_morphling.start()
        thread_buy_windranger.start()
        thread_buy_dark_willow.start()
        thread_buy_clinkz.start()
        thread_buy_witch_doctor.start()
        thread_buy_mirana.start()
        # join
        thread_buy_dazzale.join()
        thread_buy_oracle.join()
        thread_buy_hoodwink.join()
        thread_buy_winter_wyvern.join()
        thread_buy_luna.join()
        thread_buy_troll_warlord.join()
        thread_buy_morphling.join()
        thread_buy_windranger.join()
        thread_buy_dark_willow.join()
        thread_buy_clinkz.join()
        thread_buy_witch_doctor.join()
        thread_buy_mirana.join()
    else:
        # start

        thread_buy_dark_willow.start()
        thread_buy_clinkz.start()
        thread_buy_witch_doctor.start()
        thread_buy_mirana.start()
        thread_buy_sniper.start()
        thread_buy_snapfire.start()
        thread_buy_drow_ranger.start()
        thread_buy_templar_assassin.start()
        thread_buy_zet.start()
        thread_buy_dragon_knight.start()
        # join

        thread_buy_dark_willow.join()
        thread_buy_clinkz.join()
        thread_buy_witch_doctor.join()
        thread_buy_mirana.join()
        thread_buy_sniper.join()
        thread_buy_snapfire.join()
        thread_buy_drow_ranger.join()
        thread_buy_templar_assassin.join()
        thread_buy_zet.join()
        thread_buy_dragon_knight.join()  # buy_all_previous_hero()  # logger.info(f"Ket thuc mua hero in round: {round_number}")


def reset_hero():
    if global_event.check_event():
        return False
    # hero lv1
    WinterWyvern.number = number_winter_wyvern
    HoodWink.number = number_hood_wink
    Dazzale.number = number_dazzale
    # hero lv2
    Oracle.number = 0
    TrollWarlord.number = 0
    Luna.number = 0
    Windranger.number = 0
    Morphling.number = 0
    # hero lv3
    Mirana.number = 0
    DarkWillow.number = 0
    Clinkz.number = 0
    WitchDoctor.number = 0
    # hero lv4
    Sniper.number = 0
    Snapfire.number = 0
    # hero lv5
    DrowRanger.number = 0
    TemplarAssassin.number = 0
    Zet.number = 0
    DragonKnight.number = 0


def reset_previous_hero():
    global previous_hero
    previous_hero.clear()


if __name__ == "__main__":
    time.sleep(2)
    start = time.time()
    TrollWarlord.number = 1
    Oracle.number = 1
    WinterWyvern.number = 1
    HoodWink.number = 1
    Dazzale.number = 1
    Morphling.number = 1
    WitchDoctor.number = 1
    Mirana.number = 1
    Windranger.number = 1
    # Mirana.sell_hero()

    buy_all_hero(16)
    start = time.time() - start
    buy_all_previous_hero()
    print(f"thoi gian {start}")
    pass
