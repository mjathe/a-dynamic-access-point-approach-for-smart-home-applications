# Ein dynamischer Access-Point-Ansatz für Smart-Home-Anwendungen

Der Smart Home Sektor befindet sich seit Jahren in
einem stetigen Wachstum. Die Zahl der Hersteller von
Smart Home Produkten nimmt zu und die Automatisierung
und Überwachung breitet sich auf alle Bereiche
im Haus aus.

Wichtige Aspekte des Smart Homes sind die Kommunikation
zwischen den Sensoren/Aktoren, die Anbindung an das
Internet und die Steuerung per Smartphone.

# Konzept

Es soll ein System entwickelt werden, in dem jeder Knoten, das heißt Sensor, Aktor oder Bedienelement, auch die Funktion des Access Point übernehmen kann. Für die Kommunikation wird MQTT(Message Queuing Telemetry Transport) eingesetzt. MQTT ist ein offenes Netzwerkprotokoll für Machine-to-Machine-Kommunikation (M2M), das die Übertragung von Telemetriedaten in Form von Nachrichten zwischen Geräten ermöglicht.
MQTT beruht auf dem Client-Server-Modell. Der Server, auch Broker genannt, stellt den Clients Kanäle zur Kommunikation zur Verfügung. Die Clients können diese Kanäle anlegen, auf Ihnen Nachrichten veröffentlichen und sie abonnieren, um Nachrichten von anderen Clients zu empfangen.

Bei der Konfiguration des ersten Knoten/Clients wird dieser als Broker festgelegt. Alle weiteren Clients melden sich bei dem Broker an. Der Broker legt eine Tabelle mit allen Clients und deren IP-Adressen an. Sobald sich ein neuer Client anmeldet, wird die aktualisierte IP-Tabelle an alle Clients gesendet. Das geschieht über einen MQTT-Kanal dem alle Clients folgen.

![Der erste Client wird Broker und erstellt die IP-Tabelle](https://github.com/mjathe/a-dynamic-access-point-approach-for-smart-home-applications/blob/master/Porposal/Bilder/bild1.jpg?raw=true)

Der zweite und alle weiteren Clients melden sich beim Broker an und bekommen die aktualisierte IP-Tabelle gesendet. Sollte der Broker die Verbindung verlieren, übernimmt der Client mit der niedrigsten IP-Adresse die Rolle des Brokers. Da alle Clients immer die aktuelle IP-Tabelle haben, weiß jeder Client unter welcher IP der neue Broker erreicht werden kann. Zusätzlich wird die IP-Tabelle noch auf dem Cloudspeicher abgelegt, damit sich der alte Broker mit dem neuen verbinden kann. Sollte durch den Absturz die IP-Tabelle verloren gegangen sein, muss das Gerät neu konfiguriert werden.

![Der zweite Client meldet sich beim Broker an und bekommt die aktuelle IP-Tabelle.](https://github.com/mjathe/a-dynamic-access-point-approach-for-smart-home-applications/blob/master/Porposal/Bilder/bild2.jpg?raw=true)

Der Broker hat außerdem die Aufgabe, alle Daten der Clients zu sammeln und diese kurzen Abständen in einem Cloudspeicher zu hinterlegen. 

![Der dritte Client meldet sich beim Broker an und bekommt die aktuelle IP-Tabelle.](https://github.com/mjathe/a-dynamic-access-point-approach-for-smart-home-applications/blob/master/Porposal/Bilder/Bild3.jpg?raw=true)

![Der Broker verliert die Verbindung und ein neuer Broker wird bestimmt.](https://github.com/mjathe/a-dynamic-access-point-approach-for-smart-home-applications/blob/master/Porposal/Bilder/Bild4.jpg?raw=true)

Sobald der abgestürzte Client/Broker die Verbindung wieder aufbauen konnte, erhält er die aktuelle IP-Tabelle aus dem Cloudspeicher und verbindet sich mit dem neuen Broker.

![Der ehemalige Broker ist jetzt Client](https://github.com/mjathe/a-dynamic-access-point-approach-for-smart-home-applications/blob/master/Porposal/Bilder/Bild5.jpg?raw=true)
