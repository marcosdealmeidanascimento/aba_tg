from django.core.management.base import BaseCommand
from core.models import Modulo, Nivel, Atividade

class Command(BaseCommand):
    help = 'Gera um currículo completo de atividades ABA para todos os níveis'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando geração massiva de atividades...")

        # Estrutura de currículo detalhada
        curriculo = {
            'M1': { # COMUNICAÇÃO
                'N1': [
                    ("Contato Visual", "Manter contato visual por 3 segundos ao ser chamado."),
                    ("Mando por Item", "Apontar ou vocalizar para pedir um item desejado (água, brinquedo)."),
                    ("Imitação Motora Grossa", "Imitar movimentos como bater palmas ou levantar braços."),
                    ("Resposta ao Nome", "Olhar para o instrutor quando o nome é pronunciado."),
                    ("Ecoico Simples", "Repetir sons vocais simples (ex: 'aaa', 'muuu').")
                ],
                'N2': [
                    ("Tato (Nomeação)", "Nomear 50 itens comuns em imagens."),
                    ("Mando com Frases", "Pedir itens usando 'Eu quero [item]'.", "MANDO"),
                    ("Seguimento de Instruções", "Seguir comandos de dois passos (ex: Pegue a bola e coloque na caixa)."),
                    ("Intraverbal Inicial", "Completar músicas ou frases familiares (ex: 'Brilha brilha estrelinha, quero ver você...').")
                ],
                'N3': [
                    ("Conversação", "Responder perguntas sobre o dia a dia."),
                    ("Relato", "Descrever uma cena ou imagem com 3 frases."),
                    ("Mando por Informação", "Perguntar 'Onde está?' ou 'Quem é?'."),
                    ("Abstração", "Identificar itens por características (ex: Qual voa? Qual é redondo?).")
                ]
            },
            'M2': { # SOCIAL
                'N1': [
                    ("Brincar Paralelo", "Permanecer próximo a outra criança por 2 minutos."),
                    ("Troca de Turno (Simples)", "Esperar a vez em um jogo de encaixe."),
                    ("Atenção Compartilhada", "Seguir o olhar do instrutor para um objeto.")
                ],
                'N2': [
                    ("Brincadeira Cooperativa", "Participar de um jogo de esconder ou pega-pega."),
                    ("Cumprimentos", "Dizer 'Oi' ou 'Tchau' espontaneamente para colegas."),
                    ("Compartilhar", "Oferecer um brinquedo a um colega.")
                ],
                'N3': [
                    ("Resolução de Conflitos", "Usar palavras para resolver uma disputa por brinquedo."),
                    ("Empatia", "Identificar se um colega está triste ou feliz por imagens."),
                    ("Regras de Jogos", "Seguir regras complexas de jogos de tabuleiro.")
                ]
            },
            'M3': { # COGNITIVO
                'N1': [
                    ("Pareamento Identidade", "Colocar objetos iguais juntos."),
                    ("Encaixe de Formas", "Completar quebra-cabeça de 3 peças."),
                    ("Cores Primárias", "Separar itens vermelhos e azuis.")
                ],
                'N2': [
                    ("Contagem", "Contar até 10 com correspondência um-para-um."),
                    ("Sequenciação", "Ordenar 3 imagens de uma história (início, meio, fim)."),
                    ("Categorização", "Separar animais de veículos.")
                ],
                'N3': [
                    ("Leitura Funcional", "Ler placas de sinalização (Pare, Saída)."),
                    ("Somas Simples", "Resolver adições usando objetos físicos."),
                    ("Escrita", "Escrever o próprio nome sem apoio.")
                ]
            },
            'M4': { # MOTOR
                'N1': [("Pinça", "Pegar pequenos itens usando o polegar e indicador."), ("Pular", "Pular com os dois pés juntos.")],
                'N2': [("Recorte", "Cortar uma folha seguindo uma linha reta."), ("Arremesso", "Jogar uma bola em um alvo a 1 metro.")],
                'N3': [("Escrita Cursiva", "Praticar traçados complexos."), ("Equilíbrio", "Andar sobre uma linha no chão por 2 metros.")]
            },
            'M5': { # AUTONOMIA
                'N1': [("Lavar Mãos", "Abrir torneira e usar sabão com ajuda."), ("Comer", "Usar a colher para levar comida à boca.")],
                'N2': [("Vestir", "Colocar a camiseta sozinho."), ("Higiene Bucal", "Colocar pasta na escova.")],
                'N3': [("Preparar Lanche", "Passar geleia no pão."), ("Arrumar Mochila", "Guardar itens específicos solicitados.")]
            }
        }

        # Execução
        for cod_mod, niveis in curriculo.items():
            try:
                modulo = Modulo.objects.get(codigo=cod_mod)
                for cod_niv, atividades in niveis.items():
                    nivel = Nivel.objects.get(modulo=modulo, codigo=cod_niv)
                    
                    for nome, desc in atividades:
                        Atividade.objects.get_or_create(
                            nome=nome,
                            defaults={
                                'descricao': desc,
                                'categoria': modulo.nome,
                                'nivel': nivel
                            }
                        )
                    self.stdout.write(f"✓ {len(atividades)} atividades inseridas no {modulo.codigo} - {cod_niv}")
            except Modulo.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Módulo {cod_mod} não encontrado. Rode o seed_aba primeiro!"))

        self.stdout.write(self.style.SUCCESS("\nSeeder de atividades concluído com sucesso!"))