import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1250, 650

delta = {  # キー：移動量／値：（横方向移動量，縦方向移動量）
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0)}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面外or画面外を判定し、真理値タプルを返す関数
    引数 rct:こうかとんor爆弾Surfaceのrect
    戻り値:横方向、縦方向はみだし判定結果（画面内:Ture/画面外:False）、
    """
    yoko,tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向はみ出し判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向はみ出し判定
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img1 = pg.transform.flip(kk_img, True, False)
    kk_hen = {kk_img:(-5, 0),
              pg.transform.rotozoom(kk_img, -45, 2.0):(-5, -5),
              pg.transform.rotozoom(kk_img1, -90, 2.0):(0, -5),
              pg.transform.rotozoom(kk_img1, -45, 2.0):(+5, -5),
              kk_img1:(+5, 0),
              pg.transform.rotozoom(kk_img1, +45, 2.0):(+5, +5),
              pg.transform.rotozoom(kk_img1, +90, 2.0):(0, +5),
              pg.transform.rotozoom(kk_img, 45, 2.0):(-5, +5)}
    kk_rct = kk_img.get_rect()  # こうかとんSurfaceのRectを抽出
    kk_rct.center = 900, 400  # こうかとんの初期座標
    bb_img = pg.Surface((20, 20))  # 透明のSurfaceを作る
    accs = [a for a in range(1, 11)]  # 加速度のリスト
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い半径10の円を描く
    bb_img.set_colorkey((0, 0, 0))  # 黒い部分を透明
    bb_rct = bb_img.get_rect()  # 爆弾SurfaceのRectを抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = 5, 5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bb_rct):
            kk_img = pg.image.load("ex02/fig/8.png")  # 切り替え画像
            kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
            screen.blit(bg_img, [0, 0])  # 背景貼り付け
            screen.blit(kk_img, kk_rct)  # 画像貼り付け
            pg.display.update()  # 画面更新
            print("Game Over")
            return
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]: 
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)   # こうかとんを移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]  # 加速度のリスト抽出
        bb_rct.move_ip(avx, avy)   # 爆弾を移動
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()