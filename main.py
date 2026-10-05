

import csv
from abc import ABC, abstractmethod


# ==============================================================================
# CLASSES DE IMÓVEIS (HIERARQUIA E POLIMORFISMO)
# ==============================================================================

class Imovel(ABC):
    """
    Classe base abstrata para todos os imóveis.
    Garante que sub-classes implementem o método calcular_aluguel().
    """
    def __init__(self, aluguel_base: float):
        self.aluguel_base = aluguel_base

    @abstractmethod
    def calcular_aluguel(self) -> float:
        """Método abstrato que deve ser sobrescrito pelas subclasses."""
        pass

    @abstractmethod
    def obter_detalhes(self) -> str:
        """Retorna uma descrição detalhada das opções do imóvel."""
        pass


class Apartamento(Imovel):
    def __init__(self, qtd_quartos: int, tem_garagem: bool, tem_criancas: bool):
        super().__init__(aluguel_base=700.0)
        self.qtd_quartos = qtd_quartos
        self.tem_garagem = tem_garagem
        self.tem_criancas = tem_criancas

    def calcular_aluguel(self) -> float:
        aluguel = self.aluguel_base
        
        # Adicional de 2 quartos
        if self.qtd_quartos == 2:
            aluguel += 200.0
            
        # Adicional de garagem
        if self.tem_garagem:
            aluguel += 300.0
            
        # Desconto de 5% se não possuir crianças (aplicado após adicionais)
        if not self.tem_criancas:
            aluguel *= 0.95
            
        return aluguel

    def obter_detalhes(self) -> str:
        detalhes = [
            f"- Tipo: Apartamento (Base: R$ {self.aluguel_base:.2f})",
            f"- Quantidade de Quartos: {self.qtd_quartos} (+R$ 200,00)" if self.qtd_quartos == 2 else f"- Quantidade de Quartos: {self.qtd_quartos}",
            f"- Garagem: {'Sim (+R$ 300,00)' if self.tem_garagem else 'Não'}",
            f"- Possui Crianças: {'Sim' if self.tem_criancas else 'Não (Desconto de 5% aplicado)'}"
        ]
        return "\n".join(detalhes)


class Casa(Imovel):
    def __init__(self, qtd_quartos: int, tem_garagem: bool):
        super().__init__(aluguel_base=900.0)
        self.qtd_quartos = qtd_quartos
        self.tem_garagem = tem_garagem

    def calcular_aluguel(self) -> float:
        aluguel = self.aluguel_base
        
        # Adicional de 2 quartos
        if self.qtd_quartos == 2:
            aluguel += 250.0
            
        # Adicional de garagem
        if self.tem_garagem:
            aluguel += 300.0
            
        return aluguel

    def obter_detalhes(self) -> str:
        detalhes = [
            f"- Tipo: Casa (Base: R$ {self.aluguel_base:.2f})",
            f"- Quantidade de Quartos: {self.qtd_quartos} (+R$ 250,00)" if self.qtd_quartos == 2 else f"- Quantidade de Quartos: {self.qtd_quartos}",
            f"- Garagem: {'Sim (+R$ 300,00)' if self.tem_garagem else 'Não'}"
        ]
        return "\n".join(detalhes)


class Estudio(Imovel):
    def __init__(self, qtd_vagas: int):
        super().__init__(aluguel_base=1200.0)
        self.qtd_vagas = qtd_vagas

    def calcular_aluguel(self) -> float:
        aluguel = self.aluguel_base
        
        # Regra de estacionamento do estúdio
        if self.qtd_vagas > 0:
            aluguel += 250.0  # Pacote inicial até 2 vagas
            if self.qtd_vagas > 2:
                vagas_extras = self.qtd_vagas - 2
                aluguel += vagas_extras * 60.0  # R$ 60 por vaga adicional
                
        return aluguel

    def obter_detalhes(self) -> str:
        if self.qtd_vagas == 0:
            garagem_str = "Sem vagas"
        elif self.qtd_vagas <= 2:
            garagem_str = f"{self.qtd_vagas} vaga(s) - Pacote inicial (+R$ 250,00)"
        else:
            vagas_extras = self.qtd_vagas - 2
            garagem_str = f"{self.qtd_vagas} vagas - Pacote inicial (+R$ 250,00) + {vagas_extras} extra(s) (+R$ {vagas_extras * 60:.2f})"

        detalhes = [
            f"- Tipo: Estúdio (Base: R$ {self.aluguel_base:.2f})",
            f"- Estacionamento: {garagem_str}"
        ]
        return "\n".join(detalhes)


# ==============================================================================
# CLASSE DE GERENCIAMENTO DE ORÇAMENTO E EXPORTAÇÃO
# ==============================================================================

class Orcamento:
    VALOR_TAXA_CONTRATUAL = 2000.0

    def __init__(self, imovel: Imovel, num_parcelas_taxa: int):
        self.imovel = imovel
        self.num_parcelas_taxa = num_parcelas_taxa

    def calcular_valor_parcela_taxa(self) -> float:
        return self.VALOR_TAXA_CONTRATUAL / self.num_parcelas_taxa

    def exibir_resumo(self):
        aluguel_mensal = self.imovel.calcular_aluguel()
        parcela_taxa = self.calcular_valor_parcela_taxa()

        print("\n" + "=" * 55)
        print("          RENTSMART - RESUMO DO ORÇAMENTO          ")
        print("=" * 55)
        print("CARACTERÍSTICAS DA LOCAÇÃO:")
        print(self.imovel.obter_detalhes())
        print("-" * 55)
        print(f"VALOR DO ALUGUEL MENSAL: R$ {aluguel_mensal:.2f}")
        print("-" * 55)
        print("CONDIÇÕES DA TAXA CONTRATUAL:")
        print(f"- Valor Total da Taxa: R$ {self.VALOR_TAXA_CONTRATUAL:.2f}")
        print(f"- Condição Escolhida: {self.num_parcelas_taxa}x de R$ {parcela_taxa:.2f}")
        print("=" * 55 + "\n")

    def gerar_csv_projecao(self, nome_arquivo: str = "projecao_aluguel.csv"):
        aluguel_mensal = self.imovel.calcular_aluguel()
        valor_parcela_taxa = self.calcular_valor_parcela_taxa()

        try:
            with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                
                # Cabeçalho
                writer.writerow(["Mes", "Valor Aluguel (R$)", "Parcela Taxa Contratual (R$)", "Total do Mes (R$)"])

                # Projeção de 12 meses
                for mes in range(1, 13):
                    if mes <= self.num_parcelas_taxa:
                        taxa_mes = valor_parcela_taxa
                    else:
                        taxa_mes = 0.0

                    total_mes = aluguel_mensal + taxa_mes
                    
                    writer.writerow([
                        mes,
                        f"{aluguel_mensal:.2f}",
                        f"{taxa_mes:.2f}",
                        f"{total_mes:.2f}"
                    ])

            print(f"✔️  Projeção de 12 meses gerada com sucesso no arquivo '{nome_arquivo}'!")
        except Exception as e:
            print(f"❌  Erro ao gerar o arquivo CSV: {e}")


# ==============================================================================
# FUNÇÕES AUXILIARES DE VALIDAÇÃO DE ENTRADAS
# ==============================================================================

def solicitar_opcao_validada(mensagem: str, opcoes_validas: list) -> str:
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in opcoes_validas:
            return resposta
        print(f"⚠️ Opção inválida! Escolha entre: {', '.join(opcoes_validas)}")


def solicitar_inteiro_validado(mensagem: str, minimo: int, maximo: int) -> int:
    while True:
        try:
            valor = int(input(mensagem).strip())
            if minimo <= valor <= maximo:
                return valor
            print(f"⚠️ Por favor, digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("⚠️ Entrada inválida! Por favor, digite um número inteiro.")


# ==============================================================================
# FLUXO PRINCIPAL DO SISTEMA (MENU INTERATIVO)
# ==============================================================================

def main():
    print("=======================================================")
    print("      BEM-VINDO AO RENTSMART - R.M IMÓVEIS           ")
    print("=======================================================")

    # 1. Seleção do Tipo de Imóvel
    print("\nEscolha a categoria do imóvel:")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")
    
    tipo_imovel_op = solicitar_opcao_validada(
        "Digite a opção desejada (1, 2 ou 3): ", 
        ["1", "2", "3"]
    )

    imovel_selecionado = None

    # 2. Coleta de dados específica por imóvel
    if tipo_imovel_op == "1":
        # APARTAMENTO
        quartos = solicitar_inteiro_validado("Quantidade de quartos (1 ou 2): ", 1, 2)
        
        garagem_ans = solicitar_opcao_validada("Deseja vaga de garagem? (s/n): ", ["s", "n"])
        tem_garagem = (garagem_ans == "s")
        
        criancas_ans = solicitar_opcao_validada("Possui crianças no imóvel? (s/n): ", ["s", "n"])
        tem_criancas = (criancas_ans == "s")
        
        imovel_selecionado = Apartamento(
            qtd_quartos=quartos, 
            tem_garagem=tem_garagem, 
            tem_criancas=tem_criancas
        )

    elif tipo_imovel_op == "2":
        # CASA
        quartos = solicitar_inteiro_validado("Quantidade de quartos (1 ou 2): ", 1, 2)
        
        garagem_ans = solicitar_opcao_validada("Deseja vaga de garagem? (s/n): ", ["s", "n"])
        tem_garagem = (garagem_ans == "s")
        
        imovel_selecionado = Casa(
            qtd_quartos=quartos, 
            tem_garagem=tem_garagem
        )

    elif tipo_imovel_op == "3":
        # ESTÚDIO
        vagas = solicitar_inteiro_validado("Quantidade total de vagas de garagem desejadas (0 a 10): ", 0, 10)
        imovel_selecionado = Estudio(qtd_vagas=vagas)

    # 3. Taxa Contratual e Parcelamento
    print("\nA taxa contratual padrão é de R$ 2.000,00.")
    parcelas_taxa = solicitar_inteiro_validado("Em quantas parcelas deseja pagar a taxa contratual (1 a 5x)? ", 1, 5)

    # 4. Processamento e Saídas
    orcamento = Orcamento(imovel=imovel_selecionado, num_parcelas_taxa=parcelas_taxa)
    
    # Exibe orçamento no terminal
    orcamento.exibir_resumo()
    
    # Gera o arquivo CSV
    orcamento.gerar_csv_projecao()

    print("\nObrigado por utilizar o RentSmart!")


if __name__ == "__main__":
    main()