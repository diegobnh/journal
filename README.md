# Get Memory Footprint

* A primeira tarefa é descobrir o memory footprint de cada aplicação. Para isso nós rodamos cada aplicação normalmente. Ver o memory footprint no folder plots.

* Depois de executar cada aplicação, nós executamos o seguinte script:

```console
[dmoura@collect_trace]$ ./get_memfootprint.sh 
```

Esse script irá gerar a quantidade de memória que deve ser disponibilizada a depender da pressão que será dada a aplicação. Nós estamos usando três níveis: 30%, 50% e 70%. Aplicar 30% significa dizer nós configuraremos a memória de modo a não disponibilizar 30% do footprint da aplicação, ou seja, nessa configuração 30% dos dados deverão estar no PMEM. O resultado em algo parecido com oque segue abaixo:

```console
MEM_PRESSURE_30=("5" "6" "4" "5" "5" "5" "3" "4" "5" "5" "3" "4" "5" "5" "3" "4" )
MEM_PRESSURE_50=("9" "10" "6" "8" "8" "9" "6" "7" "8" "8" "6" "7" "9" "9" "6" "7" )
MEM_PRESSURE_70=("13" "14" "9" "11" "12" "12" "8" "11" "12" "12" "8" "10" "12" "12" "8" "11" )

TYPES_OF_MEM_PRESSURE=("30" "50" "70")
```

Além disso, existe um plot (**plot_mem_footprint.py**) que usa uma das saidas desse script (**mem_footprint.csv**) para gerar um gráfico de barras com o Resident Set Size obtido a partir do numastat. 
* Tempo de duração dessa fase 84 minutos.

# Running with Memory Constraint

* Para configurar a dram com diferentes níveis de pressão, nós criamos um programa (lock_memory.c) que recebe como parâmetro a quantidade a ser bloqueada de modo a forçar a aplicação a usar o PMEM.
* Basta executarmos o seguinte comando para iniciar a coleta dos dados com diferentes níveis de pressão de memória:

```console
[dmoura@collect_trace]$ sudo ./start_run.sh
```
Ao final da execução podemos coletar o tempo de execução para cada tipo de pressão de memória:

```console
[dmoura@collect_trace]$ ./get_exec_times.sh
```

Esse script irá gerar um arquivo chamado *exec_times.csv* . Ele serve de entrada para um plot dentro do folder plots.

```console
[dmoura@plots]$ python3 plot_exec_times_autonuma.py
```

* Tempo de duração dessa fase 375 minutos.

# Post Processing

* Nessa etapa nós iremos processar os dados do perf bem como das alocações interceptadas. Um ponto a destacar nessa fase é a necessidade de alterar o arquivo com as informações de alocação, de modo a quebrar alocações acima de um threshold (hoje configurado em 500MB). Para isso nós criamos um programa (mmap_break_to_chunks.py) que faz o calculo dos intervalos de endereço para cada chunk gerado.

Para executar essa fase, nós executamos o seguinte comando:

```console
[dmoura@collect_trace]$ sudo ./start_post_process.sh
```
* Tempo de duração dessa fase 336 minutos.

# Mapping

* Nessa etapa nós iremos mapear os samples para as alocações. Vale ressaltar que como objetos superiores a 500GB goram divididos em chunks, após o mapemaneto já será possível saber quais chunks tiveram mais acessos.

* Tempo de duração dessa fase 502 minutos.
