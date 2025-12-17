import json
import statistics
from collections import Counter

# Nomes dos arquivos
FILE_QUESTOES = 'questoes.jsonl'
FILE_CHUNKS = 'chunks_pesquisa.jsonl'

def print_text_histogram(data_list):
    """Gera um histograma de texto formatado no terminal."""
    if not data_list:
        print("Sem dados para gerar histograma.")
        return

    counts = Counter(data_list)
    sorted_keys = sorted(counts.keys())
    
    # Configurações para normalização visual (escala)
    max_freq = max(counts.values())
    max_bar_width = 50  # Largura máxima da barra em caracteres
    
    print("\n   [Tamanho] | [Frequência Visual] (Qtd Real)")
    print("   " + "-" * 45)

    for size in sorted_keys:
        freq = counts[size]
        
        # Calcula tamanho da barra proporcional
        if max_freq > 0:
            bar_len = int((freq / max_freq) * max_bar_width)
        else:
            bar_len = 0
            
        # Caractere de bloco para o gráfico (pode trocar por '#' se preferir)
        bar = '█' * bar_len 
        
        # Se a barra for 0 mas tiver frequência, coloca um pontinho para indicar que existe
        if bar_len == 0 and freq > 0:
            bar = '·'

        print(f"   {size:6d}    | {bar} ({freq})")

def main():
    print("--- Iniciando processamento com Histograma ---")
    
    # 1. Carregar os URNs dos chunks
    print(f"1. Mapeando {FILE_CHUNKS}...")
    valid_urns = set()
    try:
        with open(FILE_CHUNKS, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                try:
                    data = json.loads(line)
                    if 'URN' in data:
                        valid_urns.add(data['URN'])
                except json.JSONDecodeError:
                    pass
    except FileNotFoundError:
        print(f"Erro: {FILE_CHUNKS} não encontrado.")
        return

    print(f"   -> {len(valid_urns)} chunks únicos carregados.")

    # 2. Processar questões
    print(f"2. Analisando {FILE_QUESTOES}...")
    
    urn_list_lengths = []
    missing_urns_count = 0
    total_urns_checked = 0
    
    try:
        with open(FILE_QUESTOES, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                try:
                    data = json.loads(line)
                    urn_refs = data.get('URN_FUNDAMENTACAO', [])
                    
                    # Guarda o tamanho para o histograma
                    urn_list_lengths.append(len(urn_refs))
                    if (len(urn_refs) == 0):
                        print(data['QUESTAO_COM_RESPOSTA_COMENTADA_E_FORMATADA'])
                    
                    # Validação de existência
                    for urn in urn_refs:
                        total_urns_checked += 1
                        if urn not in valid_urns:
                            missing_urns_count += 1
                            
                except json.JSONDecodeError:
                    pass
    except FileNotFoundError:
        print(f"Erro: {FILE_QUESTOES} não encontrado.")
        return

    # 3. Estatísticas e Histograma
    print("\n" + "="*50)
    print("RESULTADOS DA ANÁLISE")
    print("="*50)

    # Integridade
    print(f"\n>>> INTEGRIDADE DOS DADOS")
    print(f"Total de referências verificadas: {total_urns_checked}")
    print(f"Referências QUEBRADAS (não achadas): {missing_urns_count}")
    if total_urns_checked > 0:
        pct = (missing_urns_count / total_urns_checked) * 100
        print(f"Porcentagem de erro: {pct:.2f}%")

    # Estatísticas Básicas
    if urn_list_lengths:
        print(f"\n>>> ESTATÍSTICAS DE TAMANHO DA LISTA (URN_FUNDAMENTACAO)")
        print(f"Mínimo: {min(urn_list_lengths)}")
        print(f"Média:  {statistics.mean(urn_list_lengths):.2f}")
        print(f"Máximo: {max(urn_list_lengths)}")
        
        # Histograma
        print(f"\n>>> HISTOGRAMA DE DISTRIBUIÇÃO")
        print_text_histogram(urn_list_lengths)
    else:
        print("\nNenhuma questão processada.")
        
    print("\n" + "="*50)

if __name__ == "__main__":
    main()