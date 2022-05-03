from pydoc import describe
import pygame as pg
import os
import random

# Definindo tamnho da tela
larguta_tel = 500
altura_tel = 800

# Carregndo imagens
IMAGEM_CANO = pg.transform.scale2x(
    pg.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pg.transform.scale2x(
    pg.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pg.transform.scale2x(
    pg.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSAROS = [
    pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'bird1.png'))),
    pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'bird2.png'))),
    pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'bird3.png')))
]


pg.font.init()
FONT_PONTOS = pg.font.SysFont('arial', 50)


# Definindo as class

class Passaro:
    IMGS = IMAGENS_PASSAROS
    # animações da rotação
    ROTACAO_MAX = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    # Definindo caracteristicas do passaro

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y

        # paramentros auxiliares
        self.tempo = 0
        self.contagem_da_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

        # Restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16

        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # O angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAX:
                self.angulo = self.ROTACAO_MAX
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # Definir a imagem que vai ser usada do passaro
        self.contagem_da_imagem += 1

        if self.contagem_da_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]

        elif self.contagem_da_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]

        elif self.contagem_da_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]

        elif self.contagem_da_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]

        elif self.contagem_da_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_da_imagem = 0

        # Se o passaro estiver caindo, não vai bater a asa

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_da_imagem = self.TEMPO_ANIMACAO*2

        # Desenhar a imagem
        imagem_rotacionada = pg.transform.rotate(self.imagem, self.angulo)
        pos_centro_img = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_img)

        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        # Mascara para ajudar a indentificar a colisão do passaro com o cano
        return pg.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self. altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pg.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        # Gerando a altura com um intervalo
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pg.mask.from_surface(self.CANO_TOPO)
        base_mask = pg.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if topo_ponto or base_ponto:
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA

        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))

    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = FONT_PONTOS.render(f"Pontuação:{pontos}", 1, (255, 255, 255))
    tela.blit(texto, (larguta_tel - 10 - texto.get_width(), 10))

    chao.desenhar(tela)

    pg.display.update()


def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pg.display.set_mode((larguta_tel, altura_tel))
    pontos = 0
    relogio = pg.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        # interação com o usuário
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                rodando = False
                pg.quit()
                quit()
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        # mover as coisas
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)


if __name__ == '__main__':
    main()