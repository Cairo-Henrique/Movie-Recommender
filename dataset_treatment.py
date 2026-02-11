# movies.py -- pré-processamento + leitura robusta
import csv
from pathlib import Path
import pandas as pd

p = Path(__file__).parent / 'movies.csv'
fixed = Path(__file__).parent / 'movies_fixed.csv'

print("Lendo e corrigindo:", p)

# 1) Ler com csv.reader usando TAB e quotechar padrão "
#    Vamos reconstituir linhas que têm mais colunas que o header juntando as "sobras"
with p.open('r', encoding='utf-8', errors='replace', newline='') as src, \
     fixed.open('w', encoding='utf-8', newline='') as dst:
    reader = csv.reader(src, delimiter='\t', quotechar='"')
    writer = csv.writer(dst, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    try:
        header = next(reader)
    except StopIteration:
        raise SystemExit("Arquivo vazio")

    expected = len(header)
    writer.writerow(header)  # escreve cabeçalho no fixed.csv

    total = 0
    fixed_count = 0
    short_count = 0
    long_count = 0

    for i, row in enumerate(reader, start=2):
        total += 1
        if len(row) == expected:
            writer.writerow(row)
        elif len(row) < expected:
            # linhas com menos campos: pad com strings vazias
            short_count += 1
            row = row + [''] * (expected - len(row))
            writer.writerow(row)
        else:
            # linhas com mais campos: juntar as colunas extras na última coluna
            long_count += 1
            merged = row[: expected - 1] + [ '\t'.join(row[expected - 1:]) ]
            writer.writerow(merged)
            fixed_count += 1

print(f"Total de linhas lidas (sem contar cabeçalho): {total}")
print(f"Linhas com colunas corretas: {total - short_count - long_count}")
print(f"Linhas curtas (pad com vazio): {short_count}")
print(f"Linhas longas (juntadas na última coluna): {long_count}  (recuperadas: {fixed_count})")
print("Arquivo corrigido gravado em:", fixed)

# 2) Ler com pandas o arquivo corrigido (CSV com vírgula como separador)
df = pd.read_csv(fixed, encoding='utf-8', dtype=str)  # carrega tudo como str inicialmente

# 3) Limpar nomes de colunas: remover aspas indesejadas e espaços
def clean_col_name(c):
    if isinstance(c, str):
        c = c.strip()
        if c.startswith('"') and c.endswith('"'):
            c = c[1:-1]
        return c.strip()
    return c

df.columns = [clean_col_name(c) for c in df.columns]

# 4) Limpar conteúdo textual: substituir dupla-aspas internas "" -> " e strip
def clean_cell(x):
    if not isinstance(x, str):
        return x
    s = x.strip()
    # substituir dupla aspas por aspas simples internas
    s = s.replace('""', '"')
    # remover aspas ao redor (caso sobre)
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        s = s[1:-1]
    return s

for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].map(clean_cell)

# 5) Mostrar resumo
print("\nDF lido: linhas=", len(df), " colunas=", len(df.columns))
print("Colunas:", df.columns.tolist())
print("\nExemplo (primeiras 3 linhas):\n")
print(df.head(3).to_string(index=False))

# 6) Converter todas as colunas de texto para minúsculas
def lower_columns(df):
    for col in df.columns:
        if df[col].dtype == object:  # só aplica em colunas de texto
            df[col] = df[col].str.lower()
    return df

df = lower_columns(df)

# salvar o CSV modificado (sobrescreve movies_fixed.csv)
df.to_csv(fixed, index=False, encoding='utf-8')
print("\nArquivo corrigido e convertido para minúsculas salvo em:", fixed)

# salvar versão final em parquet (opcional, leitura mais rápida depois)
try:
    out_parquet = Path(__file__).parent / 'movies_fixed.parquet'
    df.to_parquet(out_parquet)
    print("\nTambém salvei em:", out_parquet)
except Exception:
    pass