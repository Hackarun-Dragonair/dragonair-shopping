# 📜 Contrato da equipe

São os nomes que **todos** usam. Mudar algo daqui? **Combine no grupo antes** e atualize este arquivo no mesmo PR.

## 1. Valores permitidos

| Campo | Valores (sempre minúsculo, sem acento) |
|---|---|
| `tipo` de zona | `sanitario` · `praca` · `corredor` · `area_tecnica` · `doca` · `entrada` · `estacionamento` |
| `status` da ronda | `ok` · `atencao` · `problema` |
| `categoria` | `limpeza` · `hidraulica` · `eletrica` · `climatizacao` · `estrutura` · `seguranca` · `outros` |
| `prioridade` | `baixa` · `media` · `alta` · `urgente` |
| `equipe` | `limpeza` · `manutencao` · `seguranca` |
| `estado` da ocorrência | `aberto` · `em_atendimento` · `resolvido` |
| cor da zona no mapa | `verde` (ok) · `amarelo` (atenção) · `vermelho` (problema) · `cinza` (ninguém conferiu no prazo) |

`id` de zona: minúsculo com hífen. Ex.: `sanitario-fem-p1`.

## 2. Planilhas (pasta `dados/`)

**`zonas.csv`**: `id,nome,tipo,piso,x,y,largura,altura,prazo_min`
- `x,y,largura,altura`: posição do bloco no mapa (desenho de 1000 × 700).
- `prazo_min`: depois de quantos minutos sem conferência a zona fica cinza.
- Só **áreas comuns**. Nada de loja.

**`frases.csv`**: `texto,categoria,prioridade,equipe`
- Frases como alguém da ronda escreveria. **Sem nome de pessoas.**

O teste `tests/test_dados.py` confere tudo isso sozinho.

## 3. Banco (SQLite, recriado toda vez que o servidor liga)

| Tabela | Colunas |
|---|---|
| `zonas` | as mesmas do `zonas.csv` |
| `registros` | `id, zona_id, status, texto, criado_em` |
| `ocorrencias` | `id, registro_id, zona_id, texto, categoria, prioridade, equipe, estado, risco, criado_em` |
| `eventos` | `id, ocorrencia_id, tipo, detalhe, criado_em`. **Só insere, nunca altera nem apaga** (o banco bloqueia). |

Datas: texto ISO, ex. `2026-11-13T19:30:00`.

## 4. Funções que ligam as partes

```python
# ia/modelo.py  (IA)
sugerir(texto: str) -> dict
# {"categoria": str, "prioridade": str, "equipe": str,
#  "confianca": float (0 a 1), "risco": bool, "aviso": str | None}

# ia/risco.py  (IA)
detectar_risco(texto: str) -> bool

# app/status.py  (dados + telas)
cor_da_zona(ultimo_status: str | None, ultimo_em: str | None,
            prazo_min: int, agora: datetime) -> str
```

## 5. Endereços (rotas)

| Rota | O que mostra | Tarefa |
|---|---|---|
| `GET /` | Mapa das zonas | #10 |
| `GET /z/{id}` | Tela dos 3 botões (abre pelo QR) | #3 |
| `POST /z/{id}` | Salva a conferência | #3 |
| `GET /fila` | Fila de ocorrências | #11 |
| `POST /ocorrencias/{id}/estado` | Muda o estado | #11 |
| `GET /ocorrencias/{id}` | Linha do tempo + dossiê | #12 |
| `GET /painel` | Indicadores por zona e equipe | #4 |
| `GET /sobre-modelo` | Como a IA funciona | #6 |
| `GET /api/sugestao?texto=` | Sugestão da IA em JSON | #6 |
| `GET /api/zonas` | Zonas + cor em JSON (para o mapa) | #10 |
