DOMAIN=$1

cp src/context/prod.js src/context/prod.js.bak

if [ $DOMAIN ]; then
  echo -e "\033[36mDomain is $DOMAIN\033[0m"
  sed -i '' 's/wiki.incv.net/'"${DOMAIN}"'/g' src/context/prod.js
else
  echo -e "\033[36mDomain is wiki.incv.net\033[0m"
fi

yarn && yarn build

mv src/context/prod.js.bak src/context/prod.js
