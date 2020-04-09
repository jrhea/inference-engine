# Inference Engine

## Model Info

***Fire Model***

inputs: 224x224 PNG images

***Wind Model***

inputs: 224x224 PNG images

## Client Instructions

***Usage: run.sh***

```bash
$ ./run.png [fire|wind] [path/to/image.png]
```

***Example: fire***

```bash
$ ./run.sh fire examples/fire/fire1.png
[{'confidence': '0.999692', 'label': 'Heavy DAMAGE fire'}, {'confidence': '0.000308329', 'label': 'No DAMAGE fire'}]  
```

***Example: wind***

```bash
$ ./run.sh wind examples/wind/partial_damage2.png
[{'confidence': '0.938072', 'label': 'PARTIAL DAMAGE'}, {'confidence': '0.0614239', 'label': 'HEAVY DAMAGE TL'}]  
```

## Server Instructions
