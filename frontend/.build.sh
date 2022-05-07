cp src/context/prod.js src/context/prod.js.bak

if [ $traceID ];then
  echo $traceID
  sed -i '' 's/traceIDStr/'"${traceID}"'/g' src/context/prod.js
fi

if [ $DOMAIN0 ]; then
  echo $DOMAIN0
  sed -i '' 's/wiki.incv.net/'"${DOMAIN0}"'/g' src/context/prod.js
fi

yarn build

mv src/context/prod.js.bak src/context/prod.js
