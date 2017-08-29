# transHumUs

## Install requirements

```
pip install -U -r requirements.txt
```

## Start

To be run in different shells / proccesses:

```
python -m transhumus.trajectories.mona  # main process, chooses trajectories
python -m transhumus.processors.websockets  # sends data from main process to webbrowsers
python -m transhumus.processors.granier  # normalizes data from granier probes
```

## Simulation

```
python -m transhumus.inputs.granier_random  # generates data in place of granier probes
python -m transhumus.processors.simulator  # emulates motion of agv
```

## Observe

```
python -m transhumus.outputs.print  # prints data on the shell
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
