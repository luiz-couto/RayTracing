### Luiz Felipe Couto Gontijo - Computação Gráfica - Universidade Federal de Minas Gerais
# RayTracing
## Overview
Esse projeto tem como objetivo a implementção de um RayTracing que produz uma imagem do tipo ppm como saída. O programa aqui apresentado foi feito em python, e tem como principal referência  o livro *Ray Tracing in One Weekend* do Peter Shirley, que pode ser encontrado nesse link:
>  https://github.com/petershirley/raytracinginoneweekend
Já que esse projeto foi inspirado no livro acima, este documento não está tão detalhado no que diz respeito ao funcionamento das diversas classes e funções, focando mais na implementação relacionada ao ambiente python e em algumas mudanças em particular.

## Para Compilar
Antes de compilar o código, é necessário a instalação de algumas bibliotecas essenciais:
* pyglm (para a manipulação de vetores)
* math (para operações matemáticas)
* random (necessária para gerar números aleatórios)

Além de, é claro, o python 3.x. Caso você não possua alguma das bibliotecas acima, basta rodar:
```
pip install *nome_da_biblioteca*

```
Para compilar o programa, simplesmente entre na pasta onde está o arquivo *.py* e rode a partir do terminal:
```
python3 ppm_test.py

```
## Implementação
De forma diferente ao que é feito no livro do Peter Shirley, ao invés de criar uma própria classe declarando o tipo vetor - vec3 -(o que gastaria bastante espaço e demandaria bastante tempo) foi utilizado o tipo *vec3* da biblioteca *pyglm*. Ele já possui todas as operações essenciais relacionadas à vetores que precisaremos ao longo do programa. 
Para a implementação foram criadas algumas classes, que serão brevemente explicadas nesse arquivo(para explicações mais profundas, veja o livro do Peter Shirley).

### Classe Ray
Pense em um raio como uma função **p (t) = A + t * B**. Onde *p* é uma posição 3D ao longo de uma linha em 3D. *A* é a origem do raio e *B* é a direção do raio. O parâmetro *t* é um número real. Um diferente *t* faz com que *p* (t) mova-se ao longo do raio.
### Classe Sphere
A classe sphere foi projetada a partir da equação de uma esfera. Ela define uma esfera a partir de seu raio, centro e material. Além disso, verifica se um raio atinge sua superfície a partir da função *hit*, que recebe como parâmetro um raio *r*.
### Classe Camera
A classe camera tem a função de simular uma câmera, definindo sua origem, posição e direção(para onde ela aponta). Nela, chamamos a posição em que colocamos a câmera de *lookfrom*, e o ponto que olhamos de *lookat*.
### Classe Camera_blur
Essa classe possui tudo que uma camêra igual à citada anteriormente possui, porém aborda um aspecto a mais: o foco. Ela possui duas váriaveis a mais(aperture e focus_dist) que juntas são responsáveis por mudar a "abertura da lente" e a distância focal. Assim, é criado o efeito de *motion_blur* , que dá a sensação de movimento focando ou não em certos objetos.
### Classes de Material
Nesse projeto possuimos três classes de material.Cada uma delas define um comportamento diferente para os raios que interceptam sua superfície:
* Lambertian: Material difuso, que quando um raio atinge sua superfície, emite esses raios em várias direções. Ou seja, a luz que reflete em uma superfície difusa tem sua direção randomizada.
* Metal: Faz com que a superfície do objeto seja similar ao comportamento de um metal.
* Dielectric: Objeto se comporta como uma superfície espelhada. Um caso interessante é quando temos duas esferas desse material combinadas, o que dá um aspecto de vidro 100% transparente. 

## Funções
Além das classes descritas anteriormente, temos(é claro) as funções que interagem com as classes. São elas:
### Reflect
Calcula a direção do raio refletido a partir de uma dado raio e da direção que ele atinge a superfície do objeto.
### Refract
Calcula a direção do raio refratado com os mesmos parâmetros descritos acima.
### Color
Calcula a cor final de cada pixel.
### Ran()
Função que calcula um número aleatório entre 0 e 1(nunca igual a um). Essa função utiliza da biblioteca *random* para gerar os números.

### RandomScene
Gera uma cena com 3 bolas maiores de diferentes materias que são fixas e bolas menores variadas, na qual o material e posição de cada uma é definida aleatoriamente.



