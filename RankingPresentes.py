class RankingPresentes:
    def __init__(self, presentes_multiplos):
        self.presentes_multiplos = presentes_multiplos

    def criar_ranking(self):
        # Verifique se presentes_multiplos não está vazia e tem pelo menos 3 entradas
        if len(self.presentes_multiplos) >= 3:
            # Dicionário para armazenar nome de usuário, foto e número de presentes
            usuarios_presentes = {}

            # Preencha o dicionário com dados de presentes_multiplos
            for entrada in self.presentes_multiplos:
                usuario = entrada.get("user")
                foto = entrada.get("img")
                presentes = entrada.get("presentes")

                # Verifique se todos os dados necessários estão presentes
                if usuario and foto and presentes is not None:
                    # Adicione os dados ao dicionário
                    usuarios_presentes[usuario] = {
                        "foto": foto,
                        "presentes": presentes
                    }
                else:
                    print(f"Dados inválidos para entrada: {entrada}")  # Debug para dados inválidos

            # Obtenha os top 3 usuários com base na contagem de presentes
            top_usuarios = sorted(usuarios_presentes.items(), key=lambda x: x[1]["presentes"], reverse=True)[:3]

            # Retorna o ranking dos usuários
            return top_usuarios
        else:
            return None
