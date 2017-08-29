# transHumUs

## Install requirements

```
pip install -U -r requirements.txt
cd web; npm install
```

## Start

To be run in different shells / proccesses:

```
python -m transhumus.trajectories.mona
python -m transhumus.processors.websockets
python -m transhumus.processors.granier
```

## Simulation

```
python -m transhumus.inputs.granier_random
python -m transhumus.processors.simulator
```

## Observe

```
python -m transhumus.outputs.print
```

## Web

### Dev

```
cd web; npm start
```

Go to http://localhost:3000/

### Prod

for each new modification: `cd web; npm run build`

serve the `web/build` folder (eg. `cd web/build; python2 -m SimpleHTTPServer`, org Apache / Nginx)

Go to http://localhost:8000/
