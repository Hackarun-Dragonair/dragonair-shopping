# 📒 Guia da parte de DADOS, passo a passo

Tudo aqui dá para fazer **pelo site do GitHub**, sem instalar nada. Leva cerca de 1h30.

**Por que importa:** a IA aprende com estas frases. Mais frases variadas = IA acertando mais = nota em "Inovação e IA" (20%).

---

## Tarefa 1: mais frases de treino (meta: +70 frases, chegar a ~150)

### Onde
Arquivo `data/treino.csv` → clique no **lápis ✏️** (Edit) → vá até a **última linha** → cole as frases novas → **Commit changes** → escolha **"Create a new branch"** → **Propose changes** → **Create pull request**.

### Formato (uma frase por linha, sem espaço depois da vírgula)
```
frase,categoria,prioridade
```

### Valores permitidos (escreva igualzinho, sem acento)
| categoria | quando usar |
|---|---|
| `hidraulica` | água, vazamento, entupimento, torneira, descarga |
| `eletrica` | luz, lâmpada, tomada, energia, escada rolante, elevador |
| `climatizacao` | ar-condicionado, calor, frio, ventilação, exaustor |
| `limpeza` | sujeira, lixo, piso molhado, falta de papel ou sabonete, cheiro |
| `seguranca` | extintor, porta de emergência, alarme, pessoa suspeita, criança perdida |
| `estrutura` | coisa quebrada: cadeira, porta, vidro, piso, forro, corrimão |

| prioridade | quando usar |
|---|---|
| `P1` | risco para pessoas: fumaça, fogo, choque, pessoa presa, fio exposto |
| `P2` | atrapalha muito ou pode machucar: vazamento, piso molhado, escada parada |
| `P3` | incomoda mas dá para esperar: lâmpada queimada, ar fraco |
| `P4` | detalhe: sabonete acabando, mesa bamba |

### Como escrever boas frases (o segredo)
Escreva **como um funcionário digitaria no celular, com pressa**:
- curtas: `vaso entupido`
- com gíria: `ta pingando do teto`
- sem acento: `agua no chao perto da pia`
- com erro de digitação: `torneira vazndo`
- de jeitos diferentes para a mesma coisa: `privada entupida`, `descarga n funciona`, `banheiro alagado`

⚠️ **Hoje faltam frases de `P4` (só 5) e de `P3` (19).** Priorize essas.

### Exemplo do que colar
```
sabonete acabando no banheiro feminino,limpeza,P4
mesa bamba na praca,estrutura,P4
papel toalha no fim,limpeza,P4
ar fraco no corredor,climatizacao,P3
lampada piscando perto da escada,eletrica,P3
torneira vazndo devagar,hidraulica,P3
```

🚫 **Não pode:** nome de pessoa, nome de loja real, nada copiado da planta do shopping.

### Se usar IA (Gemini, ChatGPT) para ajudar
Pode. Cole este pedido:
> "Crie 30 frases curtas, como um funcionário de shopping digitaria no celular com pressa (gírias, sem acento, alguns erros de digitação), relatando problemas. Formato CSV: `frase,categoria,prioridade`. Categorias: hidraulica, eletrica, climatizacao, limpeza, seguranca, estrutura. Prioridades: P1 (risco a pessoas), P2 (grave), P3 (incomoda), P4 (detalhe). Pelo menos 10 de P4 e 10 de P3. Sem nomes de pessoas ou lojas."

Depois **leia uma por uma** e corrija o que estiver errado. E registre em `docs/IA.md`:
`| 13/11 | Pedro | Gemini | Gerar frases de treino da IA | Revisei uma por uma e corrigi categorias |`

---

## Tarefa 2: conferir as zonas do mapa (15 min)
Abra o app (`/`) e veja as zonas. Elas fazem sentido para um shopping? Falta alguma área comum importante (estacionamento, entrada principal, praça de alimentação)?
Anote as sugestões e mande no grupo. **Não copie nada da planta do shopping.**

---

## Tarefa 3: organizar o teste com 3 pessoas (19h–21h)
Siga `docs/missao-2/teste-usabilidade.md`: tem o que falar, as 4 tarefas e a folha para anotar.
Só vale teste **de verdade**, com prints reais (regulamento 6.5).

---

## Travou?
Mande print no grupo. Ninguém fica preso mais de 30 minutos. 💪
