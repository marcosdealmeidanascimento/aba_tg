from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Modulo, Nivel, Atividade

class Command(BaseCommand):
    help = 'Limpa e recria o currículo ABA completo baseado no protocolo VB-MAPP'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            Atividade.objects.all().delete()
            Nivel.objects.all().delete()
            Modulo.objects.all().delete()
        self.stdout.write("  Currículo ABA anterior removido")
        self.stdout.write("Gerando currículo ABA (VB-MAPP)...")

        curriculo = {
            # ─────────────────────────────────────────────────────────────────
            # M1 · COMUNICAÇÃO  (VB-MAPP: Mand, Tact, Echoic, Intraverbal,
            #                    Listener Responding, Visual Perceptual / Reading)
            # ─────────────────────────────────────────────────────────────────
            'M1': {
                'N1': [
                    ("Contato Visual", "Manter contato visual por 3 segundos ao ser chamado pelo nome."),
                    ("Mando por Item Desejado", "Apontar ou vocalizar para solicitar um item preferido (água, brinquedo)."),
                    ("Imitação Motora Grossa", "Imitar movimentos amplos como bater palmas ou levantar os braços."),
                    ("Resposta ao Nome", "Olhar para o instrutor dentro de 5 segundos após ouvir o próprio nome."),
                    ("Ecoico de Sons Simples", "Repetir sons vocálicos isolados: 'aaa', 'ooo', 'muuu'."),
                    ("Ecoico de CV Simples", "Repetir sílabas consoante+vogal: 'ma', 'pa', 'ba', 'da'."),
                    ("Mando com Gesto", "Usar gesto de alcançar ou apontar para pedir item que está fora do alcance."),
                    ("Seguimento de Instrução de 1 Passo", "Executar um comando simples como 'Sente' ou 'Venha'."),
                    ("Discriminação Ouvinte (2 itens)", "Selecionar o objeto correto entre dois quando nomeado pelo instrutor."),
                    ("Tato de Objetos Comuns (5 itens)", "Nomear 5 objetos do cotidiano apresentados ao vivo: copo, bola, sapato, carro, boneca."),
                ],
                'N2': [
                    ("Tato de 50 Itens em Imagens", "Nomear pelo menos 50 itens apresentados em cartões ou fotos."),
                    ("Mando com Frase de 2 Palavras", "Usar estrutura 'Quero [item]' ou '[item] por favor' para fazer pedidos."),
                    ("Mando por Informação (Onde?)", "Perguntar 'Onde está?' para localizar um item escondido."),
                    ("Seguimento de Instrução de 2 Passos", "Executar comandos encadeados: 'Pegue o lápis e coloque na mesa'."),
                    ("Intraverbal: Completar Frases Familiares", "Completar canções ou frases conhecidas: 'Parabéns pra você...'"),
                    ("Ecoico de Palavras Dissílabas", "Repetir palavras com duas sílabas: 'cama', 'bola', 'sapo'."),
                    ("Discriminação Ouvinte (campo de 6 itens)", "Selecionar objeto correto entre seis quando nomeado."),
                    ("Tato de Ações em Imagens (10 ações)", "Nomear ações em figuras: correndo, dormindo, comendo, pulando."),
                    ("Tato de Atributos: Cores (4 cores)", "Identificar e nomear vermelho, azul, verde e amarelo."),
                    ("Mando por Ação", "Solicitar que o instrutor realize uma ação: 'Cante', 'Pule'."),
                    ("Resposta de Ouvinte por Função", "Selecionar o item pela sua função: 'Qual você usa para tomar?'"),
                    ("Resposta de Ouvinte por Classe", "Selecionar o item pela sua categoria: 'Me dê um animal'."),
                ],
                'N3': [
                    ("Conversação Espontânea", "Iniciar e manter uma conversa sobre um tema por pelo menos 3 trocas de turno."),
                    ("Relato de Evento Passado", "Descrever com 3 ou mais frases algo que aconteceu no mesmo dia."),
                    ("Intraverbal: Perguntas de 'O quê?' e 'Quem?'", "Responder perguntas sobre personagens e objetos de histórias."),
                    ("Mando por Informação (Como? Por quê?)", "Fazer perguntas de 'Como se faz?' ou 'Por que?' para obter informação."),
                    ("Tato de Emoções", "Nomear emoções em imagens de rostos: feliz, triste, com raiva, com medo."),
                    ("Abstração por Característica", "Identificar itens por características: 'Qual tem penas?', 'Qual é doce?'"),
                    ("Intraverbal: Categorias", "Listar 5 ou mais itens de uma categoria dada: 'Fale frutas'."),
                    ("Tato de Atributos: Tamanho e Forma", "Nomear atributos como grande/pequeno, quadrado/redondo."),
                    ("Ecoico de Sentenças Curtas", "Repetir frases de até 5 palavras sem omissões."),
                    ("Leitura Funcional de Palavras", "Ler em voz alta palavras de alta frequência do cotidiano: nome, banheiro, saída."),
                    ("Resposta de Ouvinte: Preposições", "Colocar objeto 'em cima de', 'embaixo de' e 'dentro de' conforme instrução."),
                    ("Narrativa Sequencial", "Organizar e contar 3 cartões de história na ordem correta."),
                ],
            },

            # ─────────────────────────────────────────────────────────────────
            # M2 · SOCIAL  (VB-MAPP: Social / Play Skills)
            # ─────────────────────────────────────────────────────────────────
            'M2': {
                'N1': [
                    ("Brincar Paralelo", "Permanecer próximo a outra criança por 2 minutos sem interação negativa."),
                    ("Troca de Turno Simples", "Esperar a vez em jogo de encaixe ou passa-e-pega."),
                    ("Atenção Compartilhada: Seguir Olhar", "Seguir o olhar ou o ponto do instrutor para um objeto."),
                    ("Atenção Compartilhada: Mostrar Objeto", "Pegar um objeto e mostrá-lo ao parceiro espontaneamente."),
                    ("Imitar Pares", "Copiar uma ação simples realizada por outra criança."),
                    ("Aproximação Social", "Se aproximar de um colega e iniciar contato físico suave (tocar no ombro)."),
                    ("Responder a Cumprimentos", "Dizer 'Oi' em resposta quando um colega cumprimenta."),
                    ("Brincadeira Funcional com Brinquedos", "Usar brinquedo de forma convencional: empurrar carrinho, alimentar boneca."),
                ],
                'N2': [
                    ("Brincadeira Cooperativa", "Participar de jogo de esconder, pega-pega ou jogo de tabuleiro simples."),
                    ("Cumprimentos Espontâneos", "Dizer 'Oi' ou 'Tchau' sem prompt ao encontrar ou se despedir de colegas."),
                    ("Compartilhar Materiais", "Oferecer um brinquedo ou item a um colega quando solicitado."),
                    ("Solicitar Atenção do Par", "Chamar o nome do colega para iniciar interação."),
                    ("Comentário Social", "Fazer um comentário sobre a atividade de um colega: 'Legal isso!'."),
                    ("Esperar em Fila", "Aguardar na fila por até 2 minutos sem sair ou empurrar."),
                    ("Pedir Ajuda", "Usar palavras para solicitar assistência de um adulto ou colega."),
                    ("Reconhecer Colegas pelo Nome", "Nomear corretamente pelo menos 3 colegas da turma."),
                    ("Brincadeira de Faz de Conta Simples", "Participar de brincadeira simbólica com 2 ou mais papéis (médico/paciente)."),
                ],
                'N3': [
                    ("Resolução de Conflitos Verbais", "Usar palavras para resolver disputa por brinquedo sem agressão."),
                    ("Empatia: Identificar Emoções em Colegas", "Nomear o estado emocional de um colega com base no comportamento observado."),
                    ("Empatia: Oferecer Conforto", "Oferecer ajuda ou conforto verbal a colega que demonstra tristeza."),
                    ("Seguir Regras de Jogos Complexos", "Seguir as regras de jogos de tabuleiro com 3 ou mais etapas."),
                    ("Negociação", "Propor troca ou acordo verbal para obter item ou participar de atividade."),
                    ("Iniciar Convite", "Convidar um colega para brincar usando frase completa."),
                    ("Manter Tópico de Conversa", "Permanecer no mesmo assunto por 4 ou mais trocas de turno com par."),
                    ("Reconhecer e Expressar Emoções Próprias", "Nomear sua própria emoção e a razão: 'Estou com raiva porque...'."),
                    ("Respeitar Espaço Pessoal", "Manter distância adequada durante conversas sem ser solicitado."),
                    ("Elogiar um Par", "Dar feedback positivo espontâneo ao colega: 'Você foi bem!'."),
                ],
            },

            # ─────────────────────────────────────────────────────────────────
            # M3 · COGNITIVO  (VB-MAPP: Visual Perceptual / Matching-to-Sample,
            #                   Math, Early Academics)
            # ─────────────────────────────────────────────────────────────────
            'M3': {
                'N1': [
                    ("Pareamento por Identidade: Objetos", "Colocar objetos iguais juntos (campo de 3 pares)."),
                    ("Pareamento por Identidade: Imagens", "Combinar imagem idêntica sobre campo de 3 cartões."),
                    ("Encaixe de Formas (3 peças)", "Completar quebra-cabeça de 3 peças de formas geométricas."),
                    ("Discriminação de Cores Primárias", "Separar itens vermelhos, azuis e amarelos em grupos corretos."),
                    ("Discriminação de Tamanho (grande/pequeno)", "Selecionar o objeto grande ou pequeno conforme instrução."),
                    ("Parear Objeto a Imagem", "Colocar objeto real sobre a imagem correspondente no cartão."),
                    ("Parear Cor a Cor", "Combinar cartões de mesma cor em campo de 4 cores."),
                    ("Construção com Blocos (3 blocos)", "Reproduzir uma estrutura de 3 blocos apresentada pelo instrutor."),
                ],
                'N2': [
                    ("Contagem com Correspondência (1 a 10)", "Contar objetos físicos de 1 a 10 tocando cada item uma vez."),
                    ("Sequenciação de História (3 cartões)", "Ordenar início, meio e fim de uma história com 3 imagens."),
                    ("Categorização: Animais vs. Veículos", "Separar figuras de animais e veículos em dois grupos."),
                    ("Categorização: Alimentos vs. Roupas", "Separar imagens de alimentos e roupas corretamente."),
                    ("Identificação de Formas Geométricas (6 formas)", "Nomear círculo, quadrado, triângulo, retângulo, oval e losango."),
                    ("Pareamento de Quantidade a Numeral", "Associar grupo de 1 a 5 objetos ao numeral correspondente."),
                    ("Parear por Função", "Agrupar itens que têm a mesma função: garfo+colher, tênis+sandália."),
                    ("Sequência de Padrões (ABAB)", "Completar e continuar padrão de cores ou formas ABAB."),
                    ("Completar Puzzle de 6 Peças", "Montar quebra-cabeça de 6 peças sem apoio físico."),
                    ("Identificar Letras do Próprio Nome", "Apontar as letras do próprio nome em campo de letras variadas."),
                ],
                'N3': [
                    ("Leitura Funcional de Sinalização", "Ler e identificar sinais: Pare, Saída, Banheiro, Perigo."),
                    ("Soma com Objetos Físicos (até 10)", "Resolver adições usando objetos concretos como fichas ou blocos."),
                    ("Subtração com Objetos Físicos (até 5)", "Resolver subtrações simples com apoio de material concreto."),
                    ("Escrita do Próprio Nome", "Escrever o próprio nome sem modelo visual presente."),
                    ("Reconhecimento de Numerais (1 a 20)", "Identificar e nomear numerais de 1 a 20 apresentados aleatoriamente."),
                    ("Sequenciação Numérica", "Preencher o número que falta em sequência: 3, 4, __, 6."),
                    ("Leitura de Palavras de Alta Frequência (10 palavras)", "Ler corretamente pelo menos 10 palavras de uso cotidiano."),
                    ("Classificação por 2 Atributos", "Separar itens por cor E tamanho simultaneamente."),
                    ("Medida Não Convencional", "Medir objetos usando palmos ou passos e comparar resultados."),
                    ("Conceitos de Dinheiro (moedas)", "Identificar cédula de R$ 1, R$ 2, R$ 5 e R$ 10."),
                    ("Noção de Tempo: Ontem/Hoje/Amanhã", "Responder corretamente perguntas sobre ontem, hoje e amanhã."),
                ],
            },

            # ─────────────────────────────────────────────────────────────────
            # M4 · MOTOR  (Fine Motor, Gross Motor — áreas de suporte do VB-MAPP)
            # ─────────────────────────────────────────────────────────────────
            'M4': {
                'N1': [
                    ("Pinça Digital", "Pegar pequenos objetos (feijão, botão) usando polegar e indicador."),
                    ("Pular com Dois Pés", "Pular no lugar com os dois pés juntos 3 vezes seguidas."),
                    ("Rolar Bola", "Rolar uma bola de volta para o instrutor sentado a 1 metro."),
                    ("Empilhar Blocos (4 blocos)", "Empilhar 4 blocos sem derrubar a torre."),
                    ("Rasgar Papel", "Rasgar uma folha de papel ao meio com as duas mãos."),
                    ("Desembrulhar Item", "Retirar o papel ou embrulho de um objeto pequeno."),
                    ("Subir Degraus Alternando Pés (com apoio)", "Subir 3 degraus alternando os pés com auxílio de corrimão."),
                ],
                'N2': [
                    ("Recorte em Linha Reta", "Recortar uma folha seguindo uma linha reta tracejada."),
                    ("Arremesso em Alvo", "Jogar uma bola de tênis em direção a alvo a 1,5 metros, acertando 3 de 5 tentativas."),
                    ("Traçado de Formas Geométricas", "Traçar círculo, quadrado e triângulo sobre pontilhado."),
                    ("Abotoar e Desabotoar", "Abotoar e desabotoar 3 botões grandes em peça de roupa."),
                    ("Pedalar Triciclo", "Pedalar um triciclo por 3 metros em linha reta."),
                    ("Chutar Bola Parada", "Chutar bola parada no chão em direção a um alvo simples."),
                    ("Segurar Lápis Corretamente", "Segurar lápis com pegada trípode para colorir dentro de um contorno."),
                    ("Dobrar Papel ao Meio", "Dobrar uma folha A4 ao meio alinhando as bordas."),
                ],
                'N3': [
                    ("Escrita Cursiva Básica", "Praticar traçados cursivos das vogais sem perder a linha."),
                    ("Equilíbrio em Linha", "Andar sobre uma faixa de 2 metros no chão sem sair da linha."),
                    ("Corte Curvilíneo", "Recortar ao redor de uma figura simples (círculo) com tesoura."),
                    ("Pular Corda (2 saltos seguidos)", "Pular corda girada pelo instrutor por pelo menos 2 saltos consecutivos."),
                    ("Desenho de Pessoa (6 partes)", "Desenhar figura humana com cabeça, tronco, dois braços e duas pernas."),
                    ("Lançar e Receber Bola", "Arremessar e receber bola com as duas mãos a 2 metros, 4 de 5 tentativas."),
                    ("Usar Tesoura com Controle", "Recortar uma tira de papel ondulado sem sair dos limites."),
                    ("Saltar Obstáculo", "Saltar sobre um obstáculo baixo (10 cm) sem derrubá-lo."),
                ],
            },

            # ─────────────────────────────────────────────────────────────────
            # M5 · AUTONOMIA  (Self-Help / Adaptive Behavior — suporte VB-MAPP)
            # ─────────────────────────────────────────────────────────────────
            'M5': {
                'N1': [
                    ("Lavar Mãos com Assistência", "Abrir a torneira, aplicar sabão e enxaguar as mãos com assistência física parcial."),
                    ("Comer com Colher", "Levar colher com alimento à boca sem derramar por 5 colheradas consecutivas."),
                    ("Beber em Copo", "Beber líquido em copo aberto sem derramar."),
                    ("Indicar Necessidade de Banheiro", "Sinalizar (verbalmente ou por gesto) a necessidade de ir ao banheiro."),
                    ("Tirar Sapatos com Velcro", "Abrir e retirar os próprios sapatos de velcro."),
                    ("Empurrar Braço na Manga", "Introduzir o braço na manga da camiseta com prompt mínimo."),
                    ("Jogar Lixo na Lixeira", "Depositar papel ou embrulho na lixeira sem prompt após uso."),
                ],
                'N2': [
                    ("Vestir Camiseta Sozinho", "Colocar camiseta, incluindo passar a cabeça e os dois braços, sem assistência."),
                    ("Higiene Bucal: Colocar Pasta", "Colocar quantidade adequada de pasta de dente na escova sem derramar."),
                    ("Lavar Mãos Independentemente", "Completar toda a rotina de lavar mãos (água, sabão, enxágue, secar) sem prompts."),
                    ("Usar Garfo", "Espetar pedaços de alimento com garfo e levar à boca de forma independente."),
                    ("Amarrar Velcro / Fechar Zíper", "Fechar zíper ou fixar velcro em jaqueta ou mochila."),
                    ("Guardar Brinquedos no Local Correto", "Guardar 3 brinquedos diferentes em seus devidos lugares após instrução."),
                    ("Usar Lenço para Limpar o Nariz", "Pegar lenço, limpar o nariz e descartar no lixo de forma independente."),
                    ("Servir-se de Água", "Pegar uma garrafa ou jarra leve e servir água no copo sem derramar."),
                ],
                'N3': [
                    ("Preparar Lanche Simples", "Passar geleia ou manteiga no pão usando faca de manteiga."),
                    ("Arrumar Mochila", "Guardar estojo, lancheira e agenda na mochila conforme lista verbal."),
                    ("Amarrar Cadarço (nó simples)", "Realizar o primeiro laço no cadarço do tênis com assistência mínima."),
                    ("Usar Banheiro de Forma Independente", "Completar toda a rotina do banheiro (entrar, usar, limpar, dar descarga, lavar mãos) sem prompt."),
                    ("Fazer Pedido em Restaurante", "Verbalizar o pedido de um item do cardápio para um atendente."),
                    ("Cuidar de Pertences", "Guardar mochila e lancheira no local correto ao chegar à escola."),
                    ("Seguir Rotina Matinal (5 passos)", "Executar de forma independente: levantar, escovar dentes, tomar café, vestir-se e separar material."),
                    ("Identificar Situação de Perigo", "Nomear e recusar situações de risco: fogo, estrada, estranho, tomada."),
                ],
            },

            # ─────────────────────────────────────────────────────────────────
            # M6 · CONTROLE DE GRUPO  (Group / Classroom Skills — VB-MAPP)
            # ─────────────────────────────────────────────────────────────────
            'M6': {
                'N1': [
                    ("Sentar em Roda por 2 Minutos", "Permanecer sentado em roda de atividade por 2 minutos sem se levantar."),
                    ("Olhar para o Instrutor em Grupo", "Orientar o olhar para o instrutor quando chamado dentro de um grupo de 3."),
                    ("Levantar a Mão para Falar", "Levantar a mão e aguardar a permissão antes de falar em grupo."),
                    ("Seguir Instrução de Grupo", "Atender a instrução dada ao grupo sem precisar de prompt individual."),
                    ("Transição Entre Atividades", "Mudar de uma atividade para outra em até 1 minuto com prompt verbal."),
                ],
                'N2': [
                    ("Participar de Roda de Conversa", "Fazer um comentário ou responder a pergunta em roda de conversa grupal."),
                    ("Copiar da Lousa", "Copiar 3 palavras escritas na lousa no próprio caderno."),
                    ("Seguir Rotina de Sala de Aula", "Completar a sequência de atividades da rotina visual sem prompt."),
                    ("Trabalhar em Tarefa Independente por 5 Minutos", "Realizar atividade individual por 5 minutos sem precisar de atenção do instrutor."),
                    ("Esperar a Vez de Responder", "Aguardar outro colega terminar a resposta antes de falar."),
                    ("Transição sem Prompt", "Mudar de atividade de forma independente ao sinal sonoro ou verbal ao grupo."),
                ],
                'N3': [
                    ("Trabalho em Dupla", "Realizar tarefa colaborativa com um colega até o final."),
                    ("Apresentação Oral Breve", "Falar sobre um tema por 1 minuto diante de um pequeno grupo."),
                    ("Seguir Múltiplas Regras de Sala", "Seguir 3 ou mais regras simultaneamente durante aula de 15 minutos."),
                    ("Autorregulação em Grupo", "Identificar que está agitado e usar estratégia de regulação (respirar, pedir pausa)."),
                    ("Pedir Ajuda ao Professor em Grupo", "Levantar a mão ou usar o combinado da turma para sinalizar dúvida."),
                    ("Organizar Material Escolar", "Organizar mesa de trabalho antes e após a atividade conforme modelo."),
                ],
            },
        }

        DESCRICOES_MODULOS = {
            'M1': 'COMUNICAÇÃO',
            'M2': 'SOCIAL',
            'M3': 'COGNITIVO',
            'M4': 'MOTOR',
            'M5': 'AUTONOMIA',
            'M6': 'CONTROLE DE GRUPO',
        }
        DESCRICOES_NIVEIS = {
            'N1': 'Nível Iniciante',
            'N2': 'Nível Intermediário',
            'N3': 'Nível Avançado',
        }

        with transaction.atomic():
            for cod_mod, niveis in curriculo.items():
                modulo = Modulo.objects.create(
                    nome=cod_mod,
                    descricao=DESCRICOES_MODULOS[cod_mod],
                )
                for cod_niv, atividades in niveis.items():
                    nivel = Nivel.objects.create(
                        modulo=modulo,
                        nome=cod_niv,
                        descricao=DESCRICOES_NIVEIS[cod_niv],
                    )
                    for nome, desc in atividades:
                        Atividade.objects.create(
                            nome=nome,
                            nivel=nivel,
                            descricao=desc,
                            categoria=cod_mod,
                        )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  {modulo.nome} ({DESCRICOES_MODULOS[cod_mod]}) - {cod_niv}: {len(atividades)} atividades"
                        )
                    )

        self.stdout.write(self.style.SUCCESS("\nCurrículo ABA (VB-MAPP) gerado com sucesso!"))