# **AMR Projekt: Blensor-Pipeline zur Generierung von Trainingsdaten für 6D-Pose-Estimation**

## **1. Info**

Dieses Repository enthält den Code für das AMR-Semesterprojekt `Aufbau einer Pipeline zur Generierung von synthetischen Trainingsdaten für 6D-Pose-Estimation`.
Das Ziel dieses Projektes ist es, das Erzeugen von Trainingsdaten für die 6D-Pose-Estimation zu automatisieren. 
Die Umsetzung erfolgte unter Verwendung von Blensor über die Python-API.

<hr>

## **2. Setup**

1\. Stellen Sie sicher, dass sich das modifizierte Blensor AppImage `Blender-x86_64.AppImage` in diesem Repository befindet.

2\. Geben Sie mit dem nachfolgendem Befehl die Erlaubnis das AppImage auszuführen:
```
chmod +x Blender-x86_64.AppImage
```
3\. Ersetzen Sie das Beispiel-Objekt im `scan_objects` Ordner durch ihr eigenes Objekt. Das Objekt muss dabei im .obj-Format vorliegen.

4\. Passen Sie die Einstellungen innerhalb der `config.yaml` gemäß der nachfolgenden Beschreibung an.

<hr>

## **3. Konfiguration**

Die Konfigurationsdatei `config.yaml` enthält alle Einstellungen zu den Scans.
Die Einstellungen müssen, wie unten beschrieben, an den realen Versuchsaufbau angepasst werden:

Zunächst muss dafür die Position und die Rotation des simulierten Azure Kinect Scanners im Abschnitt **scan_settings** konfiguriert werden.
Die Position stellt dabei den Abstand zum Ursprung der Blensor Szene dar. Die Rotation beschreibt, wie der Sensor ausgerichtet ist.
Das Objekt, welches gescannt werden soll, wird dann im Ursprung der Blensor Szene eingefügt und innerhalb einer definierten Fläche zufällig verschoben und rotiert. Der Bereich, in welchem das Objekt zufällig platziert werden kann, muss ebenfalls in diesem Abschnitt konfiguriert werden.
Weiterhin muss hier festgelegt werden, wieviele Scans durchgeführt werden.

Der Abschnitt **azure_kinect_settings** muss nicht geändert werden, liefert aber Informationen über die Konfiguration des Sensors, die für die Fehlersuche nützlich sein können.


**scan_settings**
- scanner_location: Liste mit den x, y und z-Positionen des Azure Kinect Scanners in Metern.
- scanner_rotation: Liste mit den x, y und z-Rotationen des Azure Kinect Scanners in Metern.
- object_location_area: Liste mit den maximalen Abweichungen vom Mittelpunkt der Fläche, auf welcher sich das Objekt befindet. (Default: +- 0,25m)
- num_scans: Anzahl der Scans, welche für das Objekt durchgeführt werden.

**azure_kinect_settings**
- x_res: Auflösung des Sensors in x-Richtung in Pixeln.
- y_res: Auflösung des Sensors in y-Richtung in Pixeln.
- focal_length: Brennweite in Millimetern.
- max_scan_dist: Maximale Distanz, in welcher Punkte erkannt werden können in Metern.
- min_scan_dist: Minimale Distanz, in welcher Punkte erkannt werden können in Metern.
- inlier_distance: 
- noise_center: Erwartungswert des Gauß'schen Rauschens.
- noise_sigma: Standardabweichung des Gauß'schen Rauschens.
- noise_scale: Stärke des Rauschens.
- noise_smoothness: Glättung des Rauschens.
- reflectivity_distance: Objekte, welche näher als die reflectivity_distance sind, sind unabhängig von ihrer Reflektivität.
- reflectivity_limit: Mindest-Reflektivität für Objekte, welche reflectivity_distance besitzen.
- reflectivity_slope: Steigung der reflectivity_limit Kurve.

<hr>

## **4. Anwendung**

Der folgende Befehl startet Blensor ohne GUI und führt das `main.py` Skript aus.
Zum Debugging kann das -b Flag entfernt werden, dieses verhindert dass das Blensor GUI geöffnet wird.

```
./Blender-x86_64.AppImage -b -P main.py
```

Dieses Script lädt das Objekt aus dem `scan_objects` Ordner und fügt es in der Blensor Szene ein. Das Objekt wird dann zufällig um alle drei Achsen rotiert und zufällig innerhalb des vorher definierten Bereichs verschoben. Nachdem das Objekt verschoben und rotiert wurde, wird der Scan durchgeführt.

Nach Abschluss des Scans wiederholt sich der Prozess von Rotation, Translation und Scan bis die spezifizierte Anzahl an Scans erreicht ist.

Die Scans der simulierten Azure Kinect werden im .pcd Format gespeichert, während die zugehörigen Ground Truth Labels in .txt Format gespeichert werden.
Mehr Informationen über die Dateiformate sind im nächsten Abschnitt zu finden.


<hr>

## **5. Datei Formate**

<p>Für jeden Scan werden im neu erzeugten `training_data/pointclouds` Ordner die folgenden beiden Dateien erzeugt:</p>

    1. OBJNAME_XXXX.pcd          Enthält den simulierten Azure Kinect Scan.

    2. OBJNAME_noisy_XXXX.pcd    Enthält den simulierten Azure Kinect Scan mit überlagertem Rauschen.

<p>Weiterhin wird für jeden Scan im neu erzeugten 'training_data/labels' Ordner das zugehörige Ground-Truth-Label erzeugt:</p>

    1. OBJNAME_XXXX.txt          Enthält die Position sowie die Rotation des Objektes.

Dabei steht OBJNAME für den Namen des Objektes und XXXX steht für die Nummer des Scans.

**Aufbau der Scan-Dateien**

Jede Scan-Datei besteht aus einem Integer(N) für die Anzahl der Laser-Echos und N*15 Tuples, welche die Daten der einzelnen Laserechos beinhalten.
Die Datei endet mit einer Integer Zahl mit dem Wert -1.

Jedes Tuple beinhaltet dabei die folgenden Daten:

- timestamp (double)
- yaw (double)
- pitch (double)
- distance (double)
- noisy distance (double)
- x (double)
- y (double)
- z (double)
- noisy x (double)
- noisy y (double)
- noisy z (double)
- red (double)
- green (double)
- blue (double)
- object id (double)

**Aufbau der Ground-Truth-Dateien**

Jede Ground-Truth-Datei besteht aus 6 Zeilen, welche die folgenden Daten beinhalten:

- x-position (float)
- y-position (float)
- z-position (float)
- x-rotation (int)
- y-rotation (int)
- z-rotation (int)

Die Positions- und Rotationsdaten beziehen sich dabei auf das Kamera-Koordinatensystem (x:rechts, y:vorne, z:oben).

<hr>

## **6. Nützliche Funktionen** 

### **6.1 Visualisierung der Punktewolke**

Um den Output des simulierten Azure Kinect Scanners zu visualisieren existieren verschiedene Tools, wie beispielsweise der [PCD-Online-Viewer](https://imagetostl.com/de/pcd-online-ansehen).

### **6.2 Modifikation des AppImages**

Das AppImage, welches in diesem Projekt benutzt wird, basiert auf dem [originalen Blensor Appimage](https://www.blensor.org/pages/downloads.html) und beinhaltet zusätzliche Python-Module. Für zukünftige Arbeiten an diesem Projekt kann es unter Umständen nötig sein, dem AppImage weitere Module hinzuzufügen. 
Dies kann mit nachfolgend beschriebenen Schritten durchgeführt werden:


**1. Entpacken des AppImages**

Zunächst muss das AppImage mit nachfolgendem Befehl entpackt werden.
Dieser Befehl erzeugt einen Ordner "squashfs-root" neben dem originalen AppImage.
Dieser Ordner enthält alle Daten des AppImages.

```
/PATH/TO/YOUR/Blender-x86_64.AppImage --appimage-extract
```

**2. Einfügen von Python Modulen**

Im nächsten Schritt müssen die benötigten Python-Module in das entpackte AppImage eingefügt werden.
Der Unterordner, welcher die Python Module enthält, ist dieser:

```
/PATH/TO/YOUR/squashfs-root/2.79/python/lib
```

**3. Zusammensetzen des AppImages**

Zuletzt muss das AppImage mit dem folgenden Befehl wieder zusammen gesetzt werden.
Um den Befehl ausführen zu können muss zunächst das kostenlose [appimagetool](https://github.com/AppImage/AppImageKit/releases) heruntergeladen werden.
Andere Tools sollten ebenfalls möglich sein, wurden allerdings nicht getestet.

```
./appimagetool-x86_64.AppImage -v /PATH/TO/YOUR/squashfs-root
```


