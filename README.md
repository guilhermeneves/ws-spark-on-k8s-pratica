# Workshop Spark no Kubernetes

Saiba como criar o seu ambiente local para acompanhar o workshop!
<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

Os passos abaixos servem para você criar um ambiente para a realização do workshop e também um ambiente de estudo

Veja como criar as contas e configurar um cluster Kubernetes localmente, na sua máquina, independente do sistema operacional em uso, e quais serão os passos de todas as tecnologias que vamos utilizar.


O Nosso principal objetivo é que você se divirta enquanto aprende e possa ter uma experiência imersiva nesse conteúdo para aprimorar ainda mais as suas habilidades, apresentar alguma proposta para sua empresa etc


<p align="center">
  <a href="" rel="noopener">
    <img src="https://github.com/owshq-academy/ws-spark-on-k8s-pratica/blob/main/ppts/spok-roadmap.png" alt="Project logo">
 </a>
</p>


### Começando

Confira abaixo, os passos para criar o seu ambiente local para acompanhar o workshop:

#### Passo 1

Teremos uma introdução sobre a utilização de containers com Docker, no vídeo abaixo compartilhamos algumas dicas de como criar uma conta no DockerHub para hospedar imagens

* https://www.loom.com/share/2d70f9820a6740dcb9941106b000f45f

Link do DockerHub:
* https://hub.docker.com/


#### Passo 2

Agora, vamos instalar a engine do Docker que permitirá criar imagens. 
* https://www.loom.com/share/166cdb6c6b1b447eb0077c769a60c865

No link abaixo encontra-se instruções de instalação para o Linux Ubuntu
* https://docs.docker.com/engine/install/ubuntu/


#### Passo 3

A próxima etapa é instalar o Kind, que permitirá criar um ambiente Kubernetes local


* https://www.loom.com/share/7d22f8b0c79a44d98492f4ba72d764ad

Link de instalação do Kind
* https://kind.sigs.k8s.io/docs/user/quick-start/#installation
  * Sinta-se livre para utilizar outra ferramenta, como o Minikube ou k3s
  * https://minikube.sigs.k8s.io/docs/start/ - Link do Minikube
  * https://k3s.io/ - Link do k3s
  
Para instalação de ferramentas no cluster kubernetes, utilizaremos também o Helm. Você pode fazer o download no link abaixo
* https://helm.sh/docs/intro/install/

#### [Dica Bônus]
Plugins que facilitam a interação com Kubernetes
* https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/kubectl
* https://github.com/ahmetb/kubectx
* https://k8slens.dev/

#### Passo 4

AWS Free Tier: Veja dicas de como criar uma conta na AWS e utilizar alguns serviços gratuítos por 12 meses

Como criar uma conta grátis na AWS:
* https://www.loom.com/share/c88110f4ee3b49c1999d11aa7d9fdb7a

Link da página
* https://aws.amazon.com/free/

Além disso, instale as seguintes ferramentas para interação com a AWS
* https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
* https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html


É isso, as demais dicas e instruções serão apresentadas no dia do Workshop. ;D

___

## Anotações 25.02.2023:

- DataMechanics criadores do spark on Kubernets, fundaram empresa spotnetapp

- Virtualização (Server -> OS -> Hypervisor -> VM -> Guest OS ->App) x Conteinerização (Server -> OS -> Container Runtime -> App)
- Container: Isolamento, Efemero, Stateless, Inicialização rápida, Portateis
- Docker um dos produtos para rodar containers

- Imagem: é um Template com instruçoes, analogia ISO de uma imagem linux ou classe em POO. criada a partir de um dockerfile por exemplo. Numero de camadas N formando uma pilha read-only
- Container: Cria uma camada extra no topo da pilha Read/Write

Persistência Container:

- Bind Mount: Diretorio Host <-> Container (Problema vinculo maquina host, recomendado apenas para ambiente dev/local) vinculado ao host nao escala e pode perder info

- TMPFS: Utiliza memoria do container para armazenar estado, pode ser problema principalmente para spark, pois usa memoria e fica limitado a memoria, pode ser util por exemplo, cache muito rapido.

- Volumes: É uma forma que o docker fornece criar uma camada em cima do host para segregar um diretorio para o container. (Recomendado para escala, todos os container consegue acessar o mesmo volume)

## Kubernetes

- Opensource desenvolvido pela google em Go
  - Alta dispobinilidade
  - Escalabilidade
  - Disaster Recovery
  - Microservices
  - Instrucoes declarativas

### Ambiente
- kind
- minikube
- k3s (mais leve IoT Raspberry)
- EKS (gerenciados)
- AKS (gerenciados)
- GKE (gerenciados)

### Arquitetura e componenentes
- Control Plane: Gerencia cluster
- Node
- Kubeletet: Gerencia o nó
- Container (Docker, etc...)

### Interface Usuario
- kubectl
- lens
- k9s

### POD
menor unidade do kubernetes, ambiente para execução dos containers, podem conter varios containers

- ReplicaSet: Garante x replicas do POD rodando. se definir 3 e 1 cair sobe mais 1 auto.
- Deployments:
  - Blue-green: 1 pod por vez da v1 para v2, só apos todos os pods forem para v2 mata os da v1 
  - Canary: implementa v1 e v2, e direciona pelo load balancer uma % do load para cada ambiente

  ### Persistencia

  - emptydir similar com tmpfs (parecido docker)
  - hostpath similar com bindmount
  - Persistent Volumes (PV)
  - Persistent Volume Claine (PVC)

  ### Yaml
  em prod sempre usa deployment estrutura mais alto nivel
  - kind: estrutura hierarquica exemplo:
    - deployment
      - replicaset/daemonsets/statefulsets
        - pod
  - metadada: 

## Spark on Kubernetes

Cluster managers: Standalone, Mesos, Yarn, Kubernetes

Cluster Manager -> Driver (Context) -> Worker Node (Executor->task->cache)

Performance Yarn x Kubernetes 

Segundo TPC-DS a performance de ambos é semelhante não a perdas significativas. Alguns casos um pouco melhor e no outro pouco pior.

**Precisa instalar o Spark-Operator no Cluster Antes, tem no README especificando o namespace**

Spark-submit -> Kubernetes-core (scheduler-API SERVER) -> pods (exeuctor/driver)

- Pode ser feito via submit (nao recomendado)

  - spark-submit --master k8s... --conf spark.executor.instances=5 --conf spark.kubernetes.container.image=<spark-image>

- Recomendado Spark Operator

### Spark Operator

Custom Resrouce Definirion (CRDs) criado especifico para Spark criado pela google (spark-operator)

Temos o spark job (script pyspark) e o manifesto do job spark (onde será configurado os drivers/executors/etc..)

`kubectl apply -f meu-job.yaml`
```
kind: SparkApplication

metadata
 - name
 - namespace (pode organizar os jobs dentro de 1 namespace)

spec:
 - type: Scala
 - image: ˜teste/spark:3.1˜
 - imagePullPolicy: IfNotPresent
 - sparkVersion: """
driver:
 cores: 1
 coreLimit: ˜1200m˜
 labels:
  version:
executor:
 cores: 1
 instances: 2
 memory: "512m"
```

### Configuração Spot/on-demand

Cluster Spark (Node Affinity): Definir afinidades para os PODS, por exemplo, mandar drivers para on-demand e executors para spots.

### Jobs na mesma AZ

Drivers se for para Az1 e Executors para Az2 pode ser ruim shuffle custo transfer.
Driver e Executors na mesma Az1 melhor sem custo de transfer.

### Escalabilidade

Karpenter vs Cluster Autoscaler

Karpenter: (muito rapido, já atrela o pod ao node criado, nao precisa de intermedio do autoscaler para avaliar se tem node group)
- Provisiona nodes com base em pods pendentes
- Escala de acordo com o que foi solicitado
- Provisioner -> regras para controle de escala
- Vincula o pod diretamente
- Apenas AWS por enquanto

Cluster Autoscaler:
- Managed Node Groups (Auto Scaling Group) - Diferença entre o Karpenter que não precisa de um grupo especifico.
- Tenta manter balanceamento entre AZ **ponto atencao**

### S3 != HDFS

principalmente diferença rename, object storage utitiliza mimic rename (copy/delete) mais custoso.

- Magic Commiter: recomendado
 - dez - 2020 : AWS s3 se torna consistente
 - maior performance
 - necessario especificar na build da imagem spark (S3A Commiter)

 Cada tecnologia tem seu próprio commiter: EMRFS, Iceberg, DeltaLake, Hudi... caso use alguma dessas tecnologias use o da tecnologia e nao o magic commiter S3A.

 ### Alocacao Recursos Kubernetes

 **Cuidado**: Nem todo o espaço do K8s Node é alocavel, existe espaço revervado de sistema e K8s, por exemplo alocar 3400 mcores ao inves de 4000 mcores

 ## ConfigMaps

 - Desacoplar configurações
 - Informações não confidenciais

 ## Logs
- Dev logInfo
- Hom Warn
- Prod Error

### Mutation admission Webhook

se ele estiver habilitado consegue aplicar uma mutação em tempo de execução, boa partes dos componente utilizados precisa desse recurso habilitado, por exemplo node affinity para o executor subi spots.
