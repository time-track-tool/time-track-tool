# Time Tracker REST-API frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development (be sure to start roundup-server beforehand in a seperate terminal)
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


### Deploy with roundup issue tracker (time-track-tool)
After npm run build:

```
cd ..
ln -sfn vue-frontend/dist/index.html daily_record.rest.html
ln -s vue-frontend/dist .
```

then you can use roundup-server like this:

```
cd ..
roundup-server T=time-track-tool
```

