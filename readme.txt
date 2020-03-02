
Welche Services müssen laufen:
Frontend
DataImportService
ClusteringService
SchedulerService

Starten über run_linux.sh / run_osx.sh, beziehungsweise über pycharm die Services einzeln starten.

Bei der Evaluation werden Zufallsdaten generiert. Die hierbei erzeugten Votes sind immer richtig.
Aktuell wird die Anzahl der Cluster (auch für den ClusteringTask) aus der config gelesen.

Todo:
Beim Koordinatengraphen gibt es bei 2 Achsen keine Legende
Refactoring
datenbank aufräumen
Benennung der Achsen aus der Datenbank lesen