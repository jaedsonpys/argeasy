# ArgEasy

O Argeasy é um analisador de argumentos de linha de comando simples e intuitivo para qualquer usuário, facilitando a construção de aplicações **CLI**. Com ele, você pode:

- Obter argumentos;
- Obter flags;
- Definir a ação a ser tomada quando um argumento ou flag for chamado;

Além de possuir mensagens de ajudas ao usuário bem estruturadas e com todas as informações necessárias.

## Exemplo de uso

Aqui vai um exemplo simples de uso:

```python
import argeasy

parser = argeasy.ArgEasy()
parser.add_argument('foo', 'print foo', action='store_true')

args = parser.get_args()
if args.foo:
    print('foo')
```

Neste código, adicionamos um argumento chamado `foo` e definimos a ação (action) como `store_true`, ou seja, quando esse argumento for chamado, o valor dele será `True`. Caso contrário, o valor será `None`

### Actions

Action é a ação que o `argeasy` deve tomar ao perceber um argumento. Veja as ações disponíveis:

- `default`: obtém o próximo argumento como resposta. Por exemplo, se o argumento `add` estiver definido como `default` e digitarmos o comando `add README.md`, o conteúdo da variável `args.add` será `README.md`;
- `store_true`: se o argumento for detectado, o valor dele será `True`;
- `store_false`: se o argumento for detectado, o valor dele será `False`;
- `append`: se o argumento for detectado, ele irá obter todos os outros argumentos presentes a frente dele. Por exemplo, no argumento `add`, podemos obter vários arquivos de uma vez com o comando `add README.md app.py test.txt` utilizando a ação `append`. Também é possível definir o limite de argumentos;

## Licença

GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.