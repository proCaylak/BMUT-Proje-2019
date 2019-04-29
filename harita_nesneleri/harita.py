from random import randint

from harita_nesneleri.tile import Tile
from harita_nesneleri.dikdortgen import Dikdortgen


class Harita:

    def __init__(self, genislik, yukseklik):
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.yukseklik)] for x in range(self.genislik)]

        return tiles

    def make_harita(self, max_oda_sayisi, oda_min_boyut, oda_max_boyut, harita_genislik, harita_yukseklik, oyuncu):
        odalar = []
        oda_sayisi = 0

        for r in range(max_oda_sayisi):
            gen = randint(oda_min_boyut, oda_max_boyut)
            yuk = randint(oda_min_boyut, oda_max_boyut)

            x = randint(0, harita_genislik - gen - 1)
            y = randint(0, harita_yukseklik - yuk - 1)

            yeni_oda = Dikdortgen(x, y, gen, yuk)

            for diger_oda in odalar:
                if yeni_oda.cakisma(diger_oda):
                    break
            else:
                self.create_oda(yeni_oda)

                (yeni_x, yeni_y) = yeni_oda.merkez()

                if oda_sayisi == 0:
                    oyuncu.x = yeni_x
                    oyuncu.y = yeni_y
                else:
                    (onceki_x, onceki_y) = odalar[oda_sayisi - 1].merkez()

                    if randint(0, 1) == 1:
                        self.create_yatay_tunel(onceki_x, yeni_x, onceki_y)
                        self.create_dikey_tunel(onceki_y, yeni_y, onceki_x)
                    else:
                        self.create_dikey_tunel(onceki_y, yeni_y, onceki_x)
                        self.create_yatay_tunel(onceki_x, yeni_x, onceki_y)

                odalar.append(yeni_oda)
                oda_sayisi += 1

    def create_oda(self, oda):
        for x in range(oda.x1 + 1, oda.x2):
            for y in range(oda.y1 + 1, oda.y2):
                self.tiles[x][y].engel = False
                self.tiles[x][y].gorus_engel = False

    def create_yatay_tunel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].engel = False
            self.tiles[x][y].gorus_engel = False

    def create_dikey_tunel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].engel = False
            self.tiles[x][y].gorus_engel = False

    def is_engelli(self, x, y):
        if self.tiles[x][y].engel:
            return True

        return False
