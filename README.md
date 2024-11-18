## Py - UI

O Py - UI é uma aplicação web de controle de maquetes de ferreomodelismo. Ele possui uma interface que
se comunica via wifi (protocolo MQTT) com placas eletrônicas que controlarão locomotivas e desvios na maquete, e
receberão dados de sensores.
<br>
Pela interface web é possível controlar locomotivas, desvios e receber dados de sensores em maquetes. O funcionamento
envolve duas placas eletrônicas, uma que enviará comandos para as locomotivas, que trabalham em um protocolo próprio,
chamado DCC, e outra placa que lida com os sensores e com os desvios. Ambas comunicam-se via wifi com o servidor.
<br>
Para controlar as locomotivas, comandos DCC são enviados via trilhos e decodificados por um chip dentro da locomotiva
que é conhecido como decoder. A aplicação faz a conversão dos comandos enviados via web para o protocolo DCC. Essa parte
é feita pela placa H-888 que nada mais é que um arduino mais uma ESP8266.
<br>
Os desvios e os sensores são conectados a uma placa ESP32, e ela envia e recebe comandos via protocolo MQTT. Na
aplicação web é possível ver em tempo real os dados dos sensores, e comandar os desvios.
<br>
Os sensores utilizados são LEDs infravermelho, utilizados para saber se há algum trem passando na frente deles em determinado momento,
e local da maquete. O outro sensor é um RFID que vai ler tags RFID coladas nas locomotivas, desta forma é possível identificar qual
locomotiva passou por determinado ponto da maquete.
<br>

### Conteúdo
- Painel de controle de locomotivas
- Controle de desvios
- Monitoramento de sensores
- Modo administrador
- CRUDs:
    - Usuários
    - Sensores
    - Desvios
    - Locomotivas

    ![model_railroad_picture2](https://github.com/user-attachments/assets/2d227e9b-1094-40bf-ad2f-1b8b1e4c702f)

### Ferramentas
Flask, Javascript, HTML, CSS, C
Protocolo de comunicação MQTT

### Eletrônica
- Placa ESP32
- Placa H-888 (Arduino + ESP8266)
- Sensor RFID
- Tags RFID
- LEDs emissores e receptores de infravermelho.
- Decoder das locomotivas

![model_railroad_picture1](https://github.com/user-attachments/assets/c1e7cfae-d057-4f1f-8dd3-772c989b520c)


