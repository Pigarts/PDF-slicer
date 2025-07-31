# CutPdf

Este aplicativo permite cortar arquivos PDF em faixas verticais e/ou horizontais, gerando novos PDFs com as partes selecionadas. É útil para dividir grandes folhas em pedaços menores, como para impressão ou manipulação de projetos técnicos.

## Funcionalidades
- **Selecionar PDF de entrada:** Escolha o arquivo PDF que deseja cortar.
- **Definir largura máxima da faixa (mm):** Informe o tamanho máximo de cada faixa vertical.
- **Cortar também na horizontal:** Se marcado, permite definir a altura máxima das faixas, cortando também horizontalmente.
- **Definir altura máxima da faixa (mm):** Só aparece se o corte horizontal estiver ativado.
- **Selecionar pasta de destino:** Escolha onde os arquivos cortados serão salvos.
- **Salvar todas as faixas em um único PDF:** Junta todas as faixas em um único arquivo PDF, se desejado.
- **Botão "Cortar PDF":** Executa o corte conforme as opções escolhidas.

## Como usar
1. Abra o aplicativo.
2. Escolha o PDF de entrada.
3. Defina a largura máxima da faixa.
4. (Opcional) Marque "Cortar também na horizontal" e defina a altura máxima.
5. Escolha a pasta de destino.
6. (Opcional) Marque "Salvar todas as faixas em um único PDF".
7. Clique em "Cortar PDF".

Os arquivos gerados serão salvos na pasta escolhida, com nomes indicando a página, coluna e linha de cada faixa.

## Requisitos
- Python 3
- PyMuPDF (fitz)
- ttkbootstrap

## Instalação dos pacotes
```bash
pip install pymupdf ttkbootstrap
```

## Observações
- O app não altera o PDF original.
- Ideal para dividir plantas, mapas, projetos técnicos ou qualquer PDF grande em partes menores.
