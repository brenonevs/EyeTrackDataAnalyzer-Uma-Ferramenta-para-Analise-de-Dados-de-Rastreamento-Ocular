O repositório "EyeTrackDataAnalyzer" é um projeto especializado na análise de dados obtidos através de experimentos realizados com Eye Trackers. Este repositório contém um conjunto de scripts e ferramentas em Python destinados a processar, analisar e visualizar dados de rastreamento ocular.

# Explicação passo a passo

No repositório há 6 pastas: "Background Images", "Codes to Split Data", "Experiments", "Experiments Codes", "Heatmap" e "Itrace XML's"

1) Na pasta "Background Images" coloque imagens dos trechos de códigos analisados durantes os experimentos
2) Ao fazer o experimento com o Eye Tracker você recebe 2 outputs em XML, um do itrace-core e outro do itrace-eclipse, ambos os arquivos juntam todas as informações de todos os códigos analisados no mesmo XML, ou seja, para um mesmo XML existem as informações de todos os códigos analisados. Por conta disso, dentro da pasta "Codes to Split Data" existem 3 códigos: "SplitDataXMLCore.py", "SplitDataXMLEclipse.py" e "FilterXML.py".

SplitDataXMLCore.py: Separa os arquivos XML do itrace-core a partir dos códigos analisados
SplitDataXMLEclipse.py: Separa os arquivos XML do itrace-eclipse a partir dos códigos analisados
FilterXML.py: Filtra o arquivo itrace-eclipse para retirar as mudanças de códigos acidentais durante o experimento

3) Na pasta "Experiments", você deverá colocar os arquivos do itrace-eclipse separados
4) Na pasta "Experiments Codes" coloque os códigos que foram analisados durante o experimento
5) Na pasta "Heatmap" estão os códigos para gerar o heatmap
6) Na pasta "Itrace XML's" estão os arquivos XML's (Output do Eye Tracker)
    
# Como utilizar?

1) Primeiramente coloque na pasta "Itrace XML's" os arquivos XML's (itrace-core e itrace-eclipse) obtidos do experimento.
2) Coloque na pasta "Background Images" as imagens dos trechos analisados durante o experimento.
3) A partir do terminal entre na pasta "Experiments".
4) Na pasta "Codes to Split Data", rode o código "FilterXML.py" e selecione o arquivo XML itrace-eclipse que você colocou dentro de "Itrace XML's".
5) Note que dentro de "Experiments" um novo arquivo chamado "output_cleaned.xml" foi criado.
6) Agora, na pasta "Code to Split Data", rode o código "SplitDataXMLEclipse.py" e selecione o arquivo "output_cleaned.xml". Note que o arquivo itrace-eclipse foi divido em diversos outros arquivos XML a partir dos códigos que foram analisados.
7) A partir do terminal entre na pasta "Heatmap".
8) Na pasta "Heatmap", rode o código "XMLReaderMatriz.py" e selecione um dos arquivos XML que foram criados a partir do passo 6, o heatmap será gerado a partir do arquivo XML selecionado, ou seja, caso você queira fazer o heatmap da análise do código 1, por exemplo, selecione o XML do código 1 (Esse código é responsável por fazer uma transformação do arquivo XML em uma matriz para que o código do heatmap consiga transformar essa leitura em um mapa de calor).
9) Note que, no terminal aparecerá um input para você digitar a quantidade de linhas e colunas da matriz, isto é, você consegue selecionar o tamanho da matriz de interesse, quanto menor for a matriz, maior o interesse em uma determinada área, portanto, para um estudo mais geral, matrizes maiores são mais interessantes (No caso do experimento que foi realizado, utilizamos uma matriz 3x21).
10) Também aparecerá um input para você selecionar o tempo de mínimo de duração, isto é, se você selecionar um tempo de 1000 ms, o heatmap será feito para áreas (Matrizes) analisadas para um tempo maior ou igual que 1000 ms.
11) Por fim, rode o código "heatmap.py". Abrirá uma janela para você selecionar a imagem do trecho de código analisado e depois aparecerá uma janela para você selecionar o código que foi analisado (Essa janela de selecionar o código aparecerá 3 vezes, basta selecionar o mesmo arquivo código nessas 3 vezes), lembre-se que os códigos foram colocados dentro de "Experiments Codes".
12) Feito isso, o heatmap será gerado.

# Observações

1) Note que o experimento foi feito usando o eclipse, por isso o arquivo é itrace-eclipse, no entanto, dependendo da IDE utilizada, o nome do arquivo pode mudar, mas os procedimentos são os mesmos
2) Note que o código "SplitDataXMLCore.py" não utilizado. O motivo disso é que a criação desse código foi feita para utilizar uma ferramenta adicional chamada "Itrace Toolkit", no entanto, para a necessidade de fazer um heatmap esse código não é necessário
3) Deixei alguns arquivos dentro de "Background Images", "Experiments" e "Itrace XML's" para vocês conseguirem realizar alguns testes. Note que dentro de "Experiments" existem as pastas "With DejaVu" e "Without DejaVu", essas pastas foram criadas para realizar a análise de um experimento que depois foi utilizada a ferramenta DejaVu que serve para recuperar dados perdidos. Vocês podem utilizar a pasta "Testes" para realizar alguns testes.
