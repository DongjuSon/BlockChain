var CACHE_NAME = 'infra-wiki-v2';
var APP_FILES = [
  './',
  './index.html',
  './firebase-config.js',
  './wikidata.js',
  './manifest.webmanifest',
  './icon.svg',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', function(event){
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache){ return cache.addAll(APP_FILES); })
      .then(function(){ return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function(event){
  event.waitUntil(
    caches.keys()
      .then(function(keys){
        return Promise.all(keys.filter(function(key){ return key !== CACHE_NAME; })
          .map(function(key){ return caches.delete(key); }));
      })
      .then(function(){ return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function(event){
  var request = event.request;
  if(request.method !== 'GET' || new URL(request.url).origin !== self.location.origin) return;
  if(request.mode === 'navigate'){
    event.respondWith(fetch(request).catch(function(){ return caches.match('./index.html'); }));
    return;
  }
  event.respondWith(fetch(request).then(function(response){
    if(!response.ok) return response;
    var copy = response.clone();
    return caches.open(CACHE_NAME)
      .then(function(cache){ return cache.put(request, copy); })
      .then(function(){ return response; });
  }).catch(function(){ return caches.match(request); }));
});