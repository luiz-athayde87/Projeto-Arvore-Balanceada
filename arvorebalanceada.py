import math

# ==========================================
# 1. IMPLEMENTAÇÃO DA ÁRVORE AVL
# ==========================================

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        # Realiza rotação
        x.right = y
        y.left = T2

        # Atualiza alturas
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        # Realiza rotação
        y.left = x
        x.right = T2

        # Atualiza alturas
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, root, key):
        # 1. Inserção normal de BST
        if not root:
            return AVLNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # 2. Atualiza altura do nó ancestral
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # 3. Obtém o fator de balanceamento
        balance = self.get_balance(root)

        # Casos de desbalanceamento:
        # Caso Esquerda-Esquerda (LL)
        if balance > 1 and key < root.left.key:
            return self.rotate_right(root)

        # Caso Direita-Direita (RR)
        if balance < -1 and key > root.right.key:
            return self.rotate_left(root)

        # Caso Esquerda-Direita (LR)
        if balance > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Caso Direita-Esquerda (RL)
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def print_tree(self, root, val="key", left="left", right="right"):
        """Exibe a árvore no terminal de forma legível de lado."""
        def _print_tree(node, prefix="", is_left=True):
            if node is not None:
                _print_tree(getattr(node, right), prefix + ("│   " if is_left else "    "), False)
                print(prefix + ("└── " if is_left else "┌── ") + str(getattr(node, val)))
                _print_tree(getattr(node, left), prefix + ("    " if is_left else "│   "), True)
        _print_tree(root)


# ==========================================
# 2. IMPLEMENTAÇÃO DA ÁRVORE RUBRO-NEGRA
# ==========================================

class RedBlackNode:
    def __init__(self, key, color="RED"):
        self.key = key
        self.color = color  # "RED" ou "BLACK"
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.NIL = RedBlackNode(0, color="BLACK")
        self.root = self.NIL

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, key):
        node = RedBlackNode(key)
        node.left = self.NIL
        node.right = self.NIL

        y = None
        x = self.root

        while x != self.NIL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        node.color = "RED"
        self.fix_insert(node)

    def fix_insert(self, k):
        while k.parent and k.parent.color == "RED":
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.rotate_left(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.rotate_right(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.rotate_right(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.rotate_left(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "BLACK"

    def get_height(self, node):
        if node == self.NIL or node is None:
            return 0
        return 1 + max(self.get_height(node.left), self.get_height(node.right))

    def print_tree(self, node, prefix="", is_left=True):
        """Exibe a árvore no terminal mostrando o valor e a cor (R/B)."""
        if node != self.NIL and node is not None:
            self.print_tree(node.right, prefix + ("│   " if is_left else "    "), False)
            color_str = "R" if node.color == "RED" else "B"
            print(prefix + ("└── " if is_left else "┌── ") + f"{node.key}({color_str})")
            self.print_tree(node.left, prefix + ("    " if is_left else "│   "), True)


# ==========================================
# 3. SUÍTE DE TESTES PARA AS 6 QUESTÕES
# ==========================================

def executar_testes():
    questoes = [
        {
            "num": 1,
            "titulo": "Catálogo de produtos da loja",
            "estrutura": "AVL",
            "chaves": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
        },
        {
            "num": 2,
            "titulo": "Log de eventos do app Mumbuca",
            "estrutura": "Rubro-Negra",
            "chaves": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        },
        {
            "num": 3,
            "titulo": "Tabela de símbolos de um compilador",
            "estrutura": "AVL",
            "chaves": [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 55, 65]
        },
        {
            "num": 4,
            "titulo": "Índice de sessões ativas",
            "estrutura": "Rubro-Negra",
            "chaves": [42, 17, 63, 9, 28, 55, 74, 3, 21, 38, 50, 70]
        },
        {
            "num": 5,
            "titulo": "Importação de cadastro já ordenado",
            "estrutura": "AVL",
            "chaves": [1, 2, 3, 4, 5, 6, 7]
        },
        {
            "num": 6,
            "titulo": "Fila de processos do escalonador",
            "estrutura": "Rubro-Negra",
            "chaves": [40, 20, 60, 10, 30, 50, 70, 5, 15, 25, 35, 45]
        }
    ]

    for q in questoes:
        print("\n" + "=" * 65)
        print(f" QUESTÃO {q['num']}: {q['titulo']}")
        print(f" Estrutura Selecionada: {q['estrutura']}")
        print(f" Sequência de Inserção: {q['chaves']}")
        print("=" * 65)

        if q['estrutura'] == "AVL":
            avl = AVLTree()
            root = None
            for key in q['chaves']:
                root = avl.insert(root, key)
            
            print("\nRepresentação Gráfica da Árvore AVL Final:")
            avl.print_tree(root)
            
            h = avl.get_height(root) - 1  # Altura baseada em arestas (0-indexed)
            print(f"\n-> Altura final da árvore AVL: {h} (em termos de arestas/níveis)")

        else:
            rb = RedBlackTree()
            for key in q['chaves']:
                rb.insert(key)
            
            print("\nRepresentação Gráfica da Árvore Rubro-Negra Final [Valor(Cor)]:")
            rb.print_tree(rb.root)
            
            h = rb.get_height(rb.root) - 1  # Altura baseada em arestas
            print(f"\n-> Altura final da árvore Rubro-Negra: {h} (em termos de arestas/níveis)")

if __name__ == "__main__":
    executar_testes()