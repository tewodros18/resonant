<script lang="ts">
	import { browser } from '$app/environment'; 
	import * as THREE from "three"
    import { Reflector} from 'three/examples/jsm/objects/Reflector.js';
	

	if(browser) {
		let camera : THREE.PerspectiveCamera;
		let scene : THREE.Scene;
		let renderer : THREE.WebGLRenderer;


        const images = [
            'judith.jpg'
        ];

        const titles = [
            'Judith'
        ];

        const textureLoader = new THREE.TextureLoader();
        renderer = new THREE.WebGLRenderer();
        renderer.setSize( window.innerWidth, window.innerHeight );
        renderer.setAnimationLoop(animate)
        document.body.appendChild(renderer.domElement);

        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000,);

        let secondCamera = new THREE.PerspectiveCamera( 50, window.innerWidth / window.innerHeight, 0.1, 1000,);
        secondCamera.position.z = 0;

        let currentCam = camera;

        
        const rootNode = new THREE.Object3D();
        scene.add(rootNode);

        let count = 6;
        const SPACE_IN_RADIANS = 2; 

        for (let i = 0; i < count; i++){
            const texture = textureLoader.load(images[0]);
            texture.colorSpace = THREE.SRGBColorSpace; // Ensure the texture is in sRGB color space
            const baseNode = new THREE.Object3D();
            baseNode.rotation.y = i * (SPACE_IN_RADIANS * Math.PI / count);
            rootNode.add(baseNode);

            const border = new THREE.Mesh(
                new THREE.BoxGeometry(3.2, 3.2, 0.09),
                new THREE.MeshStandardMaterial({color: 0x202020})
            );
            border.position.z = -4;
            baseNode.add(border);

            const artwork = new THREE.Mesh(
                new THREE.BoxGeometry(3, 3, 0.1),
                new THREE.MeshStandardMaterial({ map: texture})
            );
            artwork.position.z = -4; 
            baseNode.add(artwork);

        }

        const spotlight = new THREE.SpotLight(0xffffff, 100.0, 10.0, 0.65, 1);
        spotlight.position.set(0,5,0);
        spotlight.target.position.set(0,0.3,-5);
        scene.add(spotlight);
        scene.add(spotlight.target);   

        const mirror = new Reflector(
            new THREE.CircleGeometry(10),
            {
                textureWidth: window.innerWidth,
                textureHeight: window.innerHeight,
                color: 0x303030,
            }
        );
        mirror.position.y = -1.65;
        mirror.rotateX(-Math.PI / 2);
        scene.add(mirror);
        
		function animate (){
            rootNode.rotation.y += 0; // Rotate the root node for continuous rotation
			renderer.render(scene, currentCam);
		}

        window.addEventListener('resize', () => {
            renderer.setSize(window.innerWidth, window.innerHeight);
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix(); 

            mirror.getRenderTarget().setSize(window.innerWidth, window.innerHeight);
        });

        window.addEventListener('keydown', (event) => {
            if (event.key === 'ArrowLeft') {
                rootNode.rotation.y += 0.1; // Rotate left
            } else if (event.key === 'ArrowRight') {
                rootNode.rotation.y -= 0.1; // Rotate right
            } else if (event.key === 'ArrowUp') {
                currentCam = secondCamera;
            } else if (event.key === 'ArrowDown') {
                currentCam = camera;
            }
        });

        /* window.addEventListener('mousemove', (event) => {
            const mouseX = (event.clientX / window.innerWidth) * 2 - 1;
            const mouseY = -(event.clientY / window.innerHeight) * 2 + 1;

            camera.position.x = mouseX * 5; // Adjust the multiplier for sensitivity
            camera.position.y = mouseY * 5; // Adjust the multiplier for sensitivity
            camera.lookAt(scene.position);
        }); */
		
	}
</script>

<svelte:head>
	<title>3D viewer</title>
</svelte:head>


<style>
    :global(body) {
            margin: 0;
            padding: 0;
            height: 100%; /* Ensure html and body take full viewport height */
            width: 100%;  /* Ensure html and body take full viewport width */
            overflow: hidden; /* Prevent any scrollbars on the main page */
        }
</style>