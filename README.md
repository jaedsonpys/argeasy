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