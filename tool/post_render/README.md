# Post configurations
E' possibile generare in modo automatizzato immagini, con set di colori e configurazioni diverse.
Funziona sia con testo che con immagini.

Il programma genera immagini ottimizzate per i social impostati.
Restituendo un immagine che rispetta formati, dimensioni e compressione ottimale per garantire la miglior qualità dell'immagine possibile.

## I colori
I colori devono essere dichiarati come array di tuple di 3 elementi.

Il programma sceglierà automaticamente un elemento dall'array in modo random.
```
# (BACKGROUND, COLORE_PRIMARIO, COLORE_TESO)

[
    (RED_200, RED_800, BLACK),
    (BLUE_200, BLUE_200, BLACK),
]
```
I colori sono tutti quelli disponibili nelle palette di [google material design](https://material.io/resources/color/#!/?view.left=0&view.right=0).
Seguire i consigli del tool per ottimizzare la scelta colori.

Piu informazioni sul [sitema colori di google](https://material.io/design/color/the-color-system.html#tools-for-picking-colors)

## Dimensione del testo
Il testo viene formattato automaticamente con una dimensione corretta.
Dato che ogni testo ha il suo space schema, non è possibile configurare il font dinamicamente.
Il font è quello che è e non può essere cambiato.

## Posizione del testo
Il testo può essere genarato i 3 modi
- Centrato nell'immagine
- Allineato a Destra
- Allineato a Sinistra

## Logo
Il logo può essere settato in 2 modi:
- come sfondo
- in uno dei due angoli destri (superiore, inferiore).

## Colorazione del logo
Il logo viene automaticamente settato dello stesso colore del testo (colorization disattivata).
Oppure del colore del colore secondario (colorization attiva).

### Requisiti file.png del logo:
- Deve avere una **dimensione di 1024x1024** in formato png con sfondo trasparente.
- Il logo deve essere **bianco #FFFFFF (255, 255, 255)** per poter usare la colorization 
(le parti non bianche non sono soggette a colorization, usare questo a propio vantaggio).
La colorization evita la necessità di avere 2 versioni di logo, una chiara (per gli sfondi scuri) ed una scura (per gli sfondi chiari)

Il sigolo file:
- logo-name.png

Idealmente nel caso di due file devono essere:
- logo-name-light.png
- logo-name-dark.png 

## Extra
Su richiesta possiamo implementare altre cose più specifiche.