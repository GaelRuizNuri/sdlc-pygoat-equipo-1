# Matriz de riesgos

Una fila por riesgo. La columna «Caso de abuso» cita los issues con #n. El checkpoint lee solo esta tabla: no agregue otras tablas a este archivo.

| ID | Amenaza | STRIDE | Caso de abuso | Probabilidad | Impacto | Riesgo | Tratamiento |
|:---|:---|:---|:---|:---|:---|:---|:---|
| R-01 | Un usuario puede borrar labs personalizados sin que quede registro de quién lo hizo | R | #3 | 2 | 2 | 4 | Corregir |
| R-02 | Un visitante inyecta SQL en el registro y extrae datos de las cuentas | I | #4 | 1 | 3 | 3 | Corregir |
| R-03 | Un visitante cambia el rol en un campo oculto y obtiene privilegios que no le corresponden | T | #5 | 2 | 3 | 6 | Corregir |
| R-04 | Un atacante abusa del login para actuar con más privilegios de los que debería tener | E | #6 | 1 | 3 | 3 | Mitigar |
| R-05 | Una sesión abierta no expira y otra persona con acceso al dispositivo la usa | S | #7 | 2 | 2 | 4 | Mitigar |
| R-06 | Las sesiones no se pueden invalidar, por lo que una cuenta capturada sigue siendo controloada por el atacante indefinidamente | S | #8 | 1 | 2 | 2 | Aceptar |


## Escala

Probabilidad (P):

- **1, baja.** Requiere acceso privilegiado, conocimiento interno o una cadena de varios pasos.
- **2, media.** Un usuario registrado lo logra con herramientas comunes.
- **3, alta.** Cualquier visitante anónimo lo logra desde el navegador.

Impacto (I):

- **1, bajo.** Afecta a un usuario y se revierte sin pérdida.
- **2, medio.** Expone o altera datos de varios usuarios, o detiene una función.
- **3, alto.** Expone datos sensibles en masa, da control de administración o detiene la app.

Riesgo = P × I. De 1 a 2 es bajo, de 3 a 4 es medio y de 6 a 9 es alto.

Tratamiento: **mitigar** (con el requerimiento #n que lo cubre), **aceptar** (con justificación), **transferir** o **evitar**.

## Mapa de calor

Escriba los ID de riesgo en la celda que les corresponde.

```
            Impacto 1          Impacto 2            Impacto 3
P 3      |             |                      |                 |
P 2      |             |       R-01 R-05      |       R-03      |
P 1      |             |         R-06         |    R-02 R-04    |
```
