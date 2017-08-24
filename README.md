# transHumUs

## Install requirements

```
pip install -U -r requirements.txt
cd web; npm install
```

## Start

To be run in different shells or proccesses:

```
python -m transhumus.trajectories.mona
python -m transhumus.outputs.websockets
python -m transhumus.processors.granier -H ame
```

## Simulation

```
python -m transhumus.inputs.granier_random -H ame
python -m transhumus.processors.simulator -H ame
```

## Observe

```
python -m transhumus.outputs.print
```

## Web

```
cd web; npm start
```
