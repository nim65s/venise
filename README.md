# transHumUs

## Install requirements

```
pip install -U -r requirements.txt
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

### Prod

serve the `web/build` folder (eg. `cd web/build; python2 -m SimpleHTTPServer`, org Apache / Nginx)

Go to http://localhost:8000/ (or whatever port you want to use)

for each new modification: `cd web; npm install; npm run build`

### Dev

```
cd web; npm install; npm start
```

Go to http://localhost:3000/
