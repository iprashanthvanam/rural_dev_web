const fs = require('fs');
const { Canvas } = require('canvas');
const THREE = require('three');

function generate3DModel(villageId, outputPath) {
    const width = 400, height = 400;
    const canvas = Canvas.createCanvas(width, height);
    const context = canvas.getContext('2d');

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas });
    renderer.setSize(width, height);

    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
    camera.position.z = 5;

    renderer.render(scene, camera);
    const buffer = canvas.toBuffer('image/png');
    fs.writeFileSync(outputPath, buffer);
    console.log(`3D model generated for village ${villageId} at ${outputPath}`);
}

// Command-line arguments
const villageId = process.argv[2];
const outputPath = process.argv[3];
if (villageId && outputPath) {
    generate3DModel(villageId, outputPath);
} else {
    console.error('Usage: node generate_3d_model.js <villageId> <outputPath>');
    process.exit(1);
}