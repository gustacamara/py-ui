## Py - UI
O Py - UI será um aplicativo de controle de maquetes de ferreomodelismo que está sendo desenvolvido para a disciplina de Experiência Criativa, do terceiro período do curso de Ciência da Computação. Ele envolve a criação de uma interface que se comunicará via wifi (protocolo MQTT) com placas eletrônicas que controlarão locomotivas e desvios na maquete, e receberão dados de sensores.

Este é um projeto que se encontra ainda em fase de desenvolvimento, com previsão de entrega na primeira semana de novembro de 2024. Servirá como o protótipo de uma aplicação mais complexa que busca paridade com o [JMRI](https://github.com/JMRI/JMRI).

![home page](https://github.com/user-attachments/assets/fefc5004-329e-4b3c-8d27-efd039391b4b)

### Conteúdo
- Painel de controle de locomotivas
- Modo administrador
- CRUDs:
    - Usuários
    - Sensores
    - Desvios
    - Locomotivas

    ![IMG_0006](https://github.com/user-attachments/assets/a1ca7108-349e-41b4-8d47-f06eb72025d0)

### Especificação
Pela interface web será possível controlar locomotivas, desvios e receber dados de sensores em maquetes. O funcionamento envolve duas placas eletrônicas, uma que enviará comandos para as locomotivas, que trabalham em um protocolo próprio, chamado DCC, e outra placa que lidará com os sensores e com os desvios. Ambas comunicam-se via wifi com o servidor.

Para controlar as locomotivas, comandos DCC são enviados via trilhos e decodificados por um chip dentro da locomotiva que é conhecido como decoder. A aplicação faz a conversão dos comandos enviados via web para o protocolo DCC. Essa parte é feita pela placa H-888 que é um Arduino + uma ESP8266.

Os desvios e os sensores são conectados a uma placa ESP32, e ela envia e recebe comandos via protocolo MQTT. Na aplicação web é possível ver em tempo real os dados dos sensores, e comandar os desvios.

Os sensores utilizados são LEDs infra vermelho, para saber se há algo passando na frente deles em determinado momento, no caso, uma locomotiva.
O outro sensor é um RFID que vai ler tags RFID coladas nas locomotivas, que conterão dados sobre elas. E assim é possível saber qual locomotiva passou por determinado ponto da maquete.

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

![IMG_0039](https://github.com/user-attachments/assets/13d39d3b-cf3a-4fc5-8bb5-f4decfd4f4ec)

