# **Biometric_System**
En nuestro proyecto desarrollamos un sistema de seguridad biométrica que integró verificación de parpadeo con reconocimiento facial, esto es para evitar fraudes por parte de usuarios desconocidos con la fotografía de algún usuario registrado. Utilizamos la librería **face_recognition** junto con OpenCV para capturar y procesar imágenes en tiempo real, comparando los rasgos faciales con una base de datos local. Mediante **Tkinter** implementamos una interfaz gráfica que permitía iniciar la verificación y gestionar la detección de parpadeo, utilizando *mediapipe* para analizar la malla facial. Además, establecimos comunicación con un ESP32 a través del **protocolo Modbus TCP**, enviando señales que activaban un relé para el control del acceso.

---

## **Flujo Operativo**

A continuación, se describe un flujo de trabajo más cercano a la realidad, donde la cámara permanece activa de manera continua y el dispositivo **ESP32** se encuentra siempre conectado a la red WiFi:

1. **Inicialización del Sistema**  
   - El **código Python** inicia y permanece ejecutándose en un computador o servidor.  
   - La **cámara** se enciende y mantiene una captura de video en **tiempo real**, lista para procesar cada cuadro (frame).

2. **Monitoreo de Rostros**  
   - El software de **Reconocimiento Facial** (Python + OpenCV + face_recognition) analiza cada frame.  
   - Si no detecta ningún rostro, sigue esperando hasta que alguien aparezca frente a la cámara.  
   - Cuando detecta un rostro, compara la imagen con la **base de datos local** (imágenes registradas).

3. **Verificación de Identidad**  
   - Si la similitud es **mayor al umbral** (ej. 65%), el sistema reconoce al usuario como **"Autorizado"**.  
   - Si no cumple el umbral, se marca como **"Desconocido"** y el sistema no envía señal de apertura.

4. **Detección de Parpadeo**  
   - Para confirmar que no se trate de una fotografía o imagen falsa, se activa la **detección de parpadeo** con **Mediapipe** (análisis de la malla facial).  
   - Si el parpadeo se verifica con éxito, se considera que el usuario está presente en tiempo real.

5. **Comunicación con el ESP32**  
   - El **ESP32** está siempre conectado a la red WiFi y ejecuta un **servidor Modbus TCP** o un protocolo similar.  
   - El código Python, tras validar la identidad y el parpadeo, **envía una señal digital** (por ejemplo, `1` si es autorizado, `0` si es fallido).  

6. **Accionamiento de la Puerta**  
   - Al recibir la señal `1`, el **ESP32** **activa el relé** durante unos segundos (ej. 3 s) para **desbloquear la chapa**.  
   - En caso de señal `0`, el ESP32 no activa la chapa y permanece a la espera de la próxima instrucción.

7. **Estado de Espera y Repetición**  
   - El sistema continúa **monitoreando la cámara** en busca de nuevos rostros, y el ESP32 permanece **escuchando** en la misma conexión WiFi.  
   - Este ciclo se repite indefinidamente mientras el sistema esté encendido.

---

## **Interacción entre el ESP32 y el Código en Python**

1. **Conexión WiFi Permanente**  
   - El ESP32 se conecta a la red WiFi al iniciar y configura el servidor Modbus TCP (o el protocolo elegido).  
   - El código Python mantiene la dirección IP y el puerto del ESP32 para enviar las señales.

2. **Recepción de Señales**  
   - Cuando el software de reconocimiento facial identifica y verifica a un usuario, llama a una función que envía una petición al ESP32.  
   - El ESP32 interpreta la señal (`1` o `0`) y actúa en consecuencia (activar o no el relé).

3. **Retroalimentación y Logs**  
   - Opcionalmente, el Python puede registrar en un **log** cada evento de apertura de puerta, junto con fecha y hora.  
   - El ESP32 podría enviar una respuesta de confirmación, si se requiere.

Con este flujo, la **cámara permanece activa** y el **ESP32** **conectado**, de modo que el sistema está preparado en todo momento para reconocer rostros y gestionar el acceso de forma automática.

---

## **Diagrama de flujo**
![Diagrama de flujo](https://github.com/user-attachments/assets/2004ea87-ef57-44e2-bc39-ff3b09fbf9d9)


## **Diagrama de Secuencia**
![Diagrama de Secuencia](https://github.com/user-attachments/assets/ddafeebf-22c8-4e19-9824-7b3be404b974)
Con **EL**: Electric Lock (chapa  eléctrica) 

---

## Integrantes

[Miguel Chacca](https://www.linkedin.com/in/miguel-chacca-tolentino-6b9561121/)
[Adrian Vela](https://www.linkedin.com/in/adrianvelad/)
Patricia Meza
[Magarita Segovia](https://www.linkedin.com/in/botones/)









