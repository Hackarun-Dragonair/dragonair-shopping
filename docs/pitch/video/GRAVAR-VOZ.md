# Como gravar a voz do vídeo no celular (5 minutos)

O vídeo já está pronto, com imagens e legendas. Falta só a sua voz.
Você grava o texto inteiro de uma vez no celular, manda o arquivo para o computador
e roda **um comando**. O resto é automático.

## 1. Prepare (1 min)
- **Lugar silencioso e "macio"**: quarto com cama, sofá ou roupas no armário aberto. Evite banheiro,
  cozinha e sala vazia (tem eco). Feche a janela, desligue ventilador e ar-condicionado.
- **Celular em modo avião** (nada de notificação no meio da gravação).
- Abra o **gravador de voz** do celular (Gravador, Gravador de Voz, Memorandos de Voz...).
  Se tiver a opção, escolha a **melhor qualidade**.
- Deixe o texto aberto em outra tela (computador ou papel): [`texto-locucao.md`](texto-locucao.md).

## 2. Posição (30 s)
- Celular a **um palmo (uns 20 cm)** da boca, com o microfone (embaixo do aparelho) virado para você.
- Um pouco **de lado**, não na frente da boca: assim o "p" e o "b" não estouram.
- Sentado com a coluna reta, ou em pé. Beba um gole de água antes.

## 3. Grave (3 min)
- Assista uma vez o `pitch-90s-voz-guia.mp4` para pegar o ritmo (não precisa imitar a voz).
- Toque em gravar, espere **2 segundos em silêncio** e comece.
- Leia o texto **inteiro de uma vez**, no seu jeito de falar, com calma.
  - `/` = respira curto. `//` = pausa de 1 a 2 segundos entre as partes. **Faça as pausas `//`**:
    é por elas que o computador acha onde começa cada parte do vídeo.
  - Errou uma palavra? Pare, respire e **comece de novo a frase** (ou a gravação toda). Não corte no celular.
- No fim, fique **2 segundos em silêncio** e pare.
- **Faça 3 tentativas** (cada uma em um arquivo). A terceira costuma ser a melhor.

**Meta de tempo:** a fala inteira com cerca de **80 a 88 segundos**.
Se ficar um pouco mais longa, o script acelera até 6% sem cortar nada; se ficar curta, a cena final fica mais tempo.
Se passar muito de 95 s, fale um pouco mais rápido nas partes do meio (não no slogan do final).

## 4. Escolha a melhor (30 s)
Ouça as 3 com fone. Escolha a que tem: nenhuma palavra engolida, sem barulho alto no fundo,
e a voz mais "sorrindo". Mande para o computador (WhatsApp para você mesmo como **documento**,
Google Drive ou cabo USB). Qualquer formato serve: m4a, mp3, ogg, opus, wav.

## 5. Gere o vídeo final (1 comando)
Na pasta do projeto, no terminal:

```bash
bash docs/pitch/video/montar_com_voz.sh ~/Downloads/NOME-DO-ARQUIVO.m4a
```

Em uns 3 minutos aparece `~/Vídeos/ronda-viva-pitch/pitch-90s-final.mp4`.
O script limpa o ruído, equilibra o volume, encaixa a voz e acerta as legendas pelas suas pausas.

## 6. Confira antes de enviar
- Assista **inteiro, com som**. As legendas acompanham a fala? (Uma diferença de meio segundo é normal.)
- O volume está bom no celular e no notebook?
- Se uma legenda ficar muito fora do lugar, grave de novo fazendo as pausas `//` mais claras.
- Se a voz ficar ruim, o **plano B** está pronto: `pitch-90s-voz-guia.mp4` (voz sintética) ou
  `pitch-90s-sem-voz.mp4` (só legendas).
