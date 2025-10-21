const fs = require('fs');
const { render } = require('leaflet-headless'); // Requires leaflet-headless

function generateMap(villageId, outputPath) {
    const L = require('leaflet');
    const map = L.map('map').setView([17.32302, 72.52814], 13); // Example coordinates
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);
    L.marker([17.32302, 72.52814]).addTo(map);

    // Render map to canvas and save as PNG (using leaflet-headless)
    const canvas = render(map);
    const buffer = canvas.toBuffer('image/png');
    fs.writeFileSync(outputPath, buffer);
    console.log(`Map generated for village ${villageId} at ${outputPath}`);
}

// Command-line arguments
const villageId = process.argv[2];
const outputPath = process.argv[3];
if (villageId && outputPath) {
    generateMap(villageId, outputPath);
} else {
    console.error('Usage: node generate_map.js <villageId> <outputPath>');
    process.exit(1);
}