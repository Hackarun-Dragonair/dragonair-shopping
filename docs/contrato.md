# 📜 Contrato da equipe (versão Flask)

São os nomes que **todos** usam. Mudar algo daqui? **Combine no grupo antes** e atualize este arquivo no mesmo PR.

## 1. Valores permitidos

| Campo | Valores (minúsculo, sem acento) | Onde está no código |
|---|---|---|
| `categoria` | `hidraulica` · `eletrica` · `climatizacao` · `limpeza` · `seguranca` · `estrutura` | `app/dominio.py` (CATEGORIAS) |
| `prioridade` | `P1` (risco a pessoas) · `P2` (grave) · `P3` (incomoda) · `P4` (detalhe) | `app/dominio.py` (PRIORIDADES) |
| equipe | `manutencao` · `limpeza` · `seguranca` · `climatizacao` | `app/seed.py` |
| resultado da conferência | `ok` · `atencao` · `problema` | rota `/z/<codigo>/conferir` |
| estado da zona (cor do mapa) | `ok` (verde) · `atencao` (amarelo) · `problema` (vermelho) · `cinza` (ninguém conferiu no prazo) | `app/dominio.py` (estado_da_zona) |
| status do problema | `aberto` · `em_atendimento` · `resolvido` | `app/consultas.py` |
| tipo de zona | `sanitario` · `praca_alimentacao` · `corredor` · `escada` · `area_tecnica` · `doca` · `entrada` · `estacionamento` | `app/seed.py` |

Código de zona: minúsculo com hífen. Ex.: `sanitario-piso1`.

## 2. Planilhas da IA (pasta `data/`)

**`treino.csv`** e **`teste_cego.csv`**: `frase,categoria,prioridade`
- Frases como alguém da ronda escreveria no celular. **Fictícias, sem nome de pessoa nem de loja.**
- `teste_cego.csv` é só para medir: **nunca** copiar frases de lá para o treino.
- Guia passo a passo: [`missao-2/guia-dados.md`](missao-2/guia-dados.md).

## 3. Regras que não mudam
- Fumaça, fogo, choque ou pessoa presa → **P1** e **"Avise a brigada pelo rádio"**. Ninguém rebaixa (`garantir_prioridade`). O sistema não aciona ninguém sozinho.
- A IA só **sugere**. O supervisor confirma.
- A **linha do tempo** (tabela `eventos`) só recebe novos registros. Nunca altera nem apaga.
- Indicadores por **zona e equipe**, nunca por pessoa. Usuários da demo são fictícios.
- **Planta do shopping é dado sensível.** O mapa é desenho nosso em blocos.

## 4. Funções que ligam as partes
```python
# app/modelo.py (IA)
obter_modelo().prever(texto) -> Previsao      # categoria + prioridade + confiança
# app/dominio.py (regras)
triar(texto, previsao) -> Sugestao            # junta IA + regra de risco
garantir_prioridade(texto, prioridade) -> (prioridade, risco)
estado_da_zona(...) -> "ok" | "atencao" | "problema" | "cinza"
```

## 5. Endereços

**Telas (HTML, para pessoas):**

| Rota | Tela | Arquivos |
|---|---|---|
| `GET /` | Mapa das zonas | `templates/inicio.html` |
| `GET /z/<codigo>` | Tela do QR (OK / Atenção / Problema) | `templates/zona.html`, `static/js/zona.js` |
| `GET /telas/fila` | Fila de problemas | `templates/fila.html` |
| `GET /telas/problemas/<id>` | Problema + linha do tempo | `templates/problema.html`, `static/js/problema.js` |
| `GET /telas/painel` | Painel | `templates/painel.html` |
| `GET /telas/sobre-a-ia` | Sobre a IA | `templates/sobre_ia.html` |

**API (JSON, usada pelas telas):** lista completa no README, seção "Como executar".
