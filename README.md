## Py - UI
O Py - UI foi desenvolvido na disciplina de Experiência Criativa, do terceiro período de Ciência da Computação, da PUCPR. Neste trabalho foi desenvolvida tanto uma aplicação web de controle de maquetes de ferreomodelismo quanto uma maquete experimental. A aplicação web possui uma interface que se comunica via wifi (protocolo MQTT) com placas eletrônicas que controlam e recebem dados de locomotivas, desvios e sensores na maquete.
<br><br>
Pela interface web é possível controlar locomotivas, desvios e receber dados de sensores em uma determinada maquete. O funcionamento
envolve duas placas eletrônicas, uma que enviará comandos para as locomotivas, que trabalham em um protocolo próprio,
chamado DCC, e outra placa que lida com os sensores e com os desvios (que são automatizados com servomotores). Ambas comunicam-se via wifi com o servidor.
<br><br>
Para controlar as locomotivas, comandos DCC são enviados via trilhos e decodificados por um chip dentro da locomotiva
que é conhecido como decoder. A aplicação faz a conversão dos comandos enviados via web para o protocolo DCC. Essa parte
é feita pela placa H-888 que nada mais é que um arduino mais uma ESP8266.
<br><br>
Os desvios (servomotores) e os sensores são conectados a uma placa ESP32, que envia e recebe comandos via protocolo MQTT. Na
aplicação web é possível ver em tempo real os dados dos sensores, e comandar e ver o estado dos desvios.
<br><br>
Os sensores utilizados para a maquete experimental, desenvolvida para este trabalho são LEDs infravermelho, utilizados para
saber se há algum trem passando na frente deles em determinado momento, e local da maquete e um RFID que vai ler tags RFID coladas nas locomotivas, sendo possível, desta forma, identificar qual locomotiva passou por determinado ponto da maquete.
<br><br>
[Documentário do Py - UI no youtube](https://www.youtube.com/watch?v=oOwtDmphA4U)

### Conteúdo da aplicação web
- Painel de controle de locomotivas
- Controle de desvios
- Monitoramento de sensores
- Modo administrador (dono da maquete)
    Contém opção de adicionar, editar e deletar:
    - Usuários
    - Sensores
    - Desvios
    - Locomotivas

<br>
Pela página principal (homepage) da aplicação, é possível visualizar a maquete, ao centro, e, na barra lateral direita, os controles das locomotivas, e dados dos sensores. Para controlar uma locomotiva, basta inserir a id dela no input indicado. Para escolher o trajeto da locomotiva nos trilhos, basta clicar no desenho da maquete para que os desvios sejam movidos de acordo. Os dados dos sensores infravermelho e
RFID também estão localizados nesta parte da homepage, e tem os dados atualizados em tempo real. Para cadastrar e editar sensores, desvios, locomotivas e usuários, é necessário estar logado como administrador, e esses menus são acessados por um dropdown da navbar, ao se clicar em "Admin".<br><br>

Tela principal:<br>
<img width="700" src="https://github.com/gustacamara/py-ui/blob/main/to_readme/pyui3.png?raw=true"><br>

Tela de login:<br>
<img width="700" src="https://github.com/gustacamara/py-ui/blob/main/to_readme/pyui4.png?raw=true"><br>

Tela de cadastro de sensor:<br>
<img width="700" src="https://github.com/gustacamara/py-ui/blob/main/to_readme/pyui1.png?raw=true"><br>

Tela de lista de locomotivas cadastradas:<br>
<img width="700" src="https://github.com/gustacamara/py-ui/blob/main/to_readme/pyui2.png?raw=true"><br>

### Conteúdo da maquete
A maquete experimental é composta dos seguintes ítens:
- Placa ESP32
- Placa H-888 (Arduino + ESP8266)
- Sensor RFID
- Tags RFID
- Servomotores (desvios automatizados)
- LEDs emissores e receptores de infravermelho.
- Decoder das locomotivas

Foto da maquete experimental:<br>
<img width="1000" src="https://github.com/gustacamara/py-ui/blob/main/to_readme/maquete.jpg?raw=true"><br>

### Ferramentas
Flask, Javascript, HTML, CSS, C, SQLite, protocolo de comunicação MQTT.



