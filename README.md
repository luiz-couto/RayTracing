### Luiz Felipe Couto Gontijo - Computação Gráfica - Universidade Federal de Minas Gerais
# RayTracing
## Overview
Esse projeto tem como objetivo a implementção de um RayTracing que produz uma imagem do tipo ppm como saída. O programa aqui apresentado foi feito em python, e tem como principal referência  o livro *Ray Tracing in One Weekend* do Peter Shirley, que pode ser encontrado nesse link:
>  https://github.com/petershirley/raytracinginoneweekend

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
### Sphere





