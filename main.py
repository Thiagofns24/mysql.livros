import mysql.connector

# Conexão com o banco de dados MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='***',
    database='***'
)
cursor = conn.cursor()

# Tabela Alunos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE
    )
''')

# Tabela Livros
cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INT AUTO_INCREMENT PRIMARY KEY,
        titulo VARCHAR(200) NOT NULL,
        autor VARCHAR(200) NOT NULL,
        disponivel BOOLEAN DEFAULT TRUE
    )
''')

# Tabela Reservas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservas (
        aluno_id INT,
        livro_id INT,
        FOREIGN KEY (aluno_id) REFERENCES alunos(id),
        FOREIGN KEY (livro_id) REFERENCES livros(id),
        UNIQUE (aluno_id, livro_id)
    )
''')

# CRUD Alunos
def criar_aluno(nome, email):
    cursor.execute('INSERT INTO alunos (nome, email) VALUES (%s, %s)', (nome, email))
    conn.commit()

def listar_alunos():
    cursor.execute('SELECT * FROM alunos')
    return cursor.fetchall()

# CRUD Livros
def criar_livro(titulo, autor):
    cursor.execute('INSERT INTO livros (titulo, autor) VALUES (%s, %s)', (titulo, autor))
    conn.commit()

def listar_livros():
    cursor.execute('SELECT * FROM livros')
    return cursor.fetchall()

# Reservar um livro para um aluno
def reservar_livro(aluno_id, livro_id):
    cursor.execute('INSERT IGNORE INTO reservas (aluno_id, livro_id) VALUES (%s, %s)', (aluno_id, livro_id))
    conn.commit()

# Listar livros reservados por um aluno específico usando JOIN
def livros_reservados_por_aluno(aluno_id):
    cursor.execute('''
        SELECT livros.titulo, livros.autor
        FROM reservas
        JOIN livros ON reservas.livro_id = livros.id
        WHERE reservas.aluno_id = %s
    ''', (aluno_id,))
    return cursor.fetchall()

# Exemplos de uso:
# Criar alguns alunos e livros
criar_aluno('Joao', 'joao@example.com')
criar_aluno('Maria', 'maria@example.com')

criar_livro('Dom Casmurro', 'Machado de Assis')
criar_livro('1984', 'George Orwell')

# Reservar livros para um aluno
reservar_livro(1, 1)  # Joao reserva Dom Casmurro
reservar_livro(2, 2)  # Maria reserva 1984

# Listar livros reservados por um aluno específico
id_aluno = 2
livros_reservados = livros_reservados_por_aluno(id_aluno)
print(f"Livros reservados pelo aluno {id_aluno}:")
for livro in livros_reservados:
    print(f"Título: {livro[0]}, Autor: {livro[1]}")

# Fechar a conexão com o banco de dados
conn.close()
