const fileInput = document.getElementById('file-input');
const uploadForm = document.getElementById('upload-form');
const emptyCollection = { type: 'FeatureCollection', features: [] };
let selectedGeojson = null;

function filenameFromDisposition(disposition) {
  if (!disposition) return 'centroids.geojson';
  const utfMatch = disposition.match(/filename\*=UTF-8''([^;]+)/i);
  if (utfMatch) return decodeURIComponent(utfMatch[1]);
  const basicMatch = disposition.match(/filename="?([^";]+)"?/i);
  return basicMatch ? basicMatch[1] : 'centroids.geojson';
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function collectCoordinates(coords, output) {
  if (!Array.isArray(coords)) return;
  if (typeof coords[0] === 'number' && typeof coords[1] === 'number') {
    output.push(coords);
    return;
  }
  for (const child of coords) {
    collectCoordinates(child, output);
  }
}

function fitToGeoJSON(geojson) {
  const points = [];
  for (const feature of geojson.features || []) {
    if (feature?.geometry?.coordinates) {
      collectCoordinates(feature.geometry.coordinates, points);
    }
  }
  if (!points.length) return;

  let minLng = Infinity;
  let minLat = Infinity;
  let maxLng = -Infinity;
  let maxLat = -Infinity;

  for (const [lng, lat] of points) {
    if (lng < minLng) minLng = lng;
    if (lat < minLat) minLat = lat;
    if (lng > maxLng) maxLng = lng;
    if (lat > maxLat) maxLat = lat;
  }

  map.fitBounds([[minLng, minLat], [maxLng, maxLat]], {
    padding: 30,
    maxZoom: 10,
    duration: 500
  });
}

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://demotiles.maplibre.org/style.json',
  center: [-98, 39],
  zoom: 3
});

const mapLoaded = new Promise((resolve) => {
  map.once('load', resolve);
});

map.on('load', () => {
  map.addSource('uploaded', { type: 'geojson', data: emptyCollection });
  map.addSource('centroids', { type: 'geojson', data: emptyCollection });

  map.addLayer({
    id: 'uploaded-fill',
    type: 'fill',
    source: 'uploaded',
    paint: { 'fill-color': '#4f46e5', 'fill-opacity': 0.25 }
  });
  map.addLayer({
    id: 'uploaded-line',
    type: 'line',
    source: 'uploaded',
    paint: { 'line-color': '#312e81', 'line-width': 1.5 }
  });
  map.addLayer({
    id: 'centroids',
    type: 'circle',
    source: 'centroids',
    paint: {
      'circle-radius': 6,
      'circle-color': '#f00'
    }
  });
});

fileInput.addEventListener('click', () => {
  fileInput.value = '';
  selectedGeojson = null;
});

fileInput.addEventListener('change', async (e) => {
  const file = e.target.files?.[0];
  if (!file) return;

  await mapLoaded;

  const geojson = JSON.parse(await file.text());
  selectedGeojson = geojson;
  map.getSource('uploaded').setData(geojson);
  map.getSource('centroids').setData(emptyCollection);
  fitToGeoJSON(geojson);
});

uploadForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!selectedGeojson) return;

  await mapLoaded;

  const res = await fetch('/', {
    method: 'POST',
    body: new FormData(uploadForm)
  });
  if (!res.ok) return;

  const filename = filenameFromDisposition(res.headers.get('Content-Disposition'));
  const blob = await res.blob();
  downloadBlob(blob, filename);

  const centroids = JSON.parse(await blob.text());
  map.getSource('centroids').setData(centroids);
});
