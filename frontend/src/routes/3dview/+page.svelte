<script lang="ts">
	import { browser } from '$app/environment'; 
	import * as THREE from "three"
    import { Reflector} from 'three/examples/jsm/objects/Reflector.js';
    import pkg from 'tween';
    import { onMount } from 'svelte';
    const { Tween, Easing, update } = pkg;
	

    

	if(browser) {
		let camera : THREE.PerspectiveCamera;
		let scene : THREE.Scene;
		let renderer : THREE.WebGLRenderer;
        let arrowsVisible = true;
        let currentIndex = 0;
        let currentChapter = 1; 
        
    
        const images = [
            '437389.jpg',
            '437390.jpg',
            '437391.jpg',
            '437393.jpg',
            '437396.jpg',
            '437406.jpg',
        ];

        const titles = [
            "Bellona",
            "Portrait of a Woman",
            "Portrait of a Young Woman with a Fan",
            "The Toilet of Bathsheba",
            "Hendrickje Stoffels",
            "The Auctioneer"
        ];

        const artist = [
            "Rembrandt (Rembrandt van Rijn)",
            "Rembrandt (Rembrandt van Rijn)",
            "Rembrandt (Rembrandt van Rijn)",
            "Rembrandt (Rembrandt van Rijn)",
            "Rembrandt (Rembrandt van Rijn)",
            "Rembrandt"
        ];
        

        const textureLoader = new THREE.TextureLoader();
        renderer = new THREE.WebGLRenderer();
        renderer.setSize( window.innerWidth, window.innerHeight );
        renderer.setAnimationLoop(animate)
        document.body.appendChild(renderer.domElement);

        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.1, 1000,);

        let currentCam = camera;

        
        const rootNode = new THREE.Object3D();
        scene.add(rootNode);

        let count = 6;
        const SPACE_IN_RADIANS = 2; 

        const leftArrowTexture = textureLoader.load('leftArrow.png');
        const rightArrowTexture = textureLoader.load('rightArrow.png');

        for (let i = 0; i < count; i++){
            
            const texture = textureLoader.load(images[i]);
            texture.colorSpace = THREE.SRGBColorSpace; // Ensure the texture is in sRGB color space
            const baseNode = new THREE.Object3D();
            baseNode.rotation.y = i * (SPACE_IN_RADIANS * Math.PI / count);
            rootNode.add(baseNode);

            let widthBorder = images[i] != '437393.jpg' ? 2.7 : 3.2; // Adjust width for the last artwork 
            let heightBorder = images[i] != '437393.jpg' ? 3.2 : 2.7;
            const border = new THREE.Mesh(
                new THREE.BoxGeometry(widthBorder, heightBorder, 0.09),
                new THREE.MeshStandardMaterial({color: 0x202020})
            );
            border.position.z = -4;
            baseNode.add(border);
            let widthArtwork = images[i] != '437393.jpg' ? 2.5 : 3; // Adjust width for the last artwork 
            let heightArtwork = images[i] != '437393.jpg' ? 3 : 2.5; // Adjust height for the last artwork
            const artwork = new THREE.Mesh(
                new THREE.BoxGeometry(widthArtwork, heightArtwork, 0.1),
                new THREE.MeshStandardMaterial({ map: texture})
            );
            artwork.position.z = -4; 
            baseNode.add(artwork);

            const leftArrow = new THREE.Mesh(
                new THREE.BoxGeometry(0.3, 0.3, 0.01),
                new THREE.MeshStandardMaterial({
                    map: leftArrowTexture, 
                    transparent: true,
                })
            );

            leftArrow.position.set(-1.8, 0, -4);
            leftArrow.name = 'leftArrow';
            //wrap back around to the first image when clicking left on the last image
            leftArrow.userData = {index: (i === count - 1) ? 0:(i + 1)}; // Store the index in userData for reference
            baseNode.add(leftArrow);
            

            const rightArrow = new THREE.Mesh(
                new THREE.BoxGeometry(0.3, 0.3, 0.01),
                new THREE.MeshStandardMaterial({
                    map: rightArrowTexture, 
                    transparent: true,
                })
            );

            rightArrow.position.set(1.8, 0, -4);
            rightArrow.name = 'rightArrow';
            rightArrow.userData = {index: (i === 0) ? count - 1: i - 1};
            baseNode.add(rightArrow);
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
                color: 0x404040,
            }
        );
        mirror.position.y = -1.65;
        mirror.rotateX(-Math.PI / 2);
        scene.add(mirror);
        
		function animate (){
            update();
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
                toggleArrows();
                playAudio(images[currentIndex].slice(0,-4), currentChapter.toString()); // Play audio for the current image
                pan(camera) // Hide arrows when in second camera view 
            } else if (event.key === 'ArrowDown') {
                new Tween(camera)
                .to({fov: 70},3000)
                .easing(Easing.Quadratic.InOut)
                .onUpdate(() => {
                    camera.updateProjectionMatrix();
                })
                .start();
                toggleArrows();
            }
        });

        window.addEventListener('click', (event) => {
            const raycaster = new THREE.Raycaster();
            const mouseNDC = new THREE.Vector2(
                (event.clientX / window.innerWidth) * 2 - 1,
                -(event.clientY / window.innerHeight) * 2 + 1
            );

            raycaster.setFromCamera(mouseNDC, currentCam);
            const intersections = raycaster.intersectObject(rootNode, true);

            if( intersections.length > 0 ){
                const obj = intersections[0].object
                const newIndex = obj.userData.index; // Get the index from userDat
                if(obj.name === 'leftArrow' && arrowsVisible) {
                    rotateGallery(-1, newIndex);
                } else if(obj.name === 'rightArrow' && arrowsVisible) {
                    rotateGallery(1, newIndex);
                }
            }
        })

        /* window.addEventListener('mousemove', (event) => {
            const mouseX = (event.clientX / window.innerWidth) * 2 - 1;
            const mouseY = -(event.clientY / window.innerHeight) * 2 + 1;

            camera.position.x = mouseX * 5; // Adjust the multiplier for sensitivity
            camera.position.y = mouseY * 5; // Adjust the multiplier for sensitivity
            camera.lookAt(scene.position);
        }); */
        
        function toggleArrows(){
                rootNode.children.forEach(baseNode => {
                    baseNode.children.forEach( element=> {
                        if(element.name === 'leftArrow' || element.name === 'rightArrow') {
                            element.visible = !element.visible; // Hide arrows when in second camera view
                        }
                    });
                });
                arrowsVisible = !arrowsVisible; // Toggle visibility state
        }

        function rotateGallery(direction: number, newIndex: number) {
            const deltaY = direction * (SPACE_IN_RADIANS * Math.PI / count);
            currentIndex = newIndex; // Update the current index
            new Tween(rootNode.rotation)
            .to({y: rootNode.rotation.y + deltaY})
            .easing(Easing.Quadratic.InOut)
            .start()
            .onStart(() => {
                document.getElementById('title')!.style.opacity = '0';
                document.getElementById('artist')!.style.opacity = '0';
            })
            .onComplete(
                () => {
                    document.getElementById('title')!.innerText = titles[newIndex];
                    document.getElementById('artist')!.innerText = artist[newIndex];
                    document.getElementById('title')!.style.opacity = '1';
                    document.getElementById('artist')!.style.opacity = '1';
                }
            )
        }
        let audio: HTMLAudioElement | null = null;
        async function playAudio(imageName: string,chapter: string = '1') {
            try {
                let url = `${imageName}`+'-'+`${chapter}`.toString();
                const params = new URLSearchParams({directory: url});
                const response = await fetch(`http://localhost:8000/audio?${params}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const audioBlob = await response.blob();
                const objectUrl = URL.createObjectURL(audioBlob);

                // If audio element already exists, update its source. Otherwise, create new.
                if (!audio) {
                    audio = new Audio(objectUrl);
                } else {
                    audio.src = objectUrl;
                }
                
                audio.play()
                    .then(() => {
                    })
                    .catch(error => {
                        console.error('Error playing audio:', error);
                    });

                // Clean up the object URL after the audio has finished playing
                audio.onended = () => {
                    if (audio) {
                    URL.revokeObjectURL(audio.src);
                    }
                };

                } catch (error: any) {
                    console.error('Fetch or play error:', error);
                }
        }
        function pan(camera: any){
            new Tween(camera)
                .to({fov: 15},3000)
                .easing(Easing.Quadratic.InOut)
                .onUpdate(() => {
                    camera.updateProjectionMatrix();
                })
                .start()
                .onComplete(()=> {
                    new Tween(camera.position)
                    .to({fov: 25, y: 0.8},3000)
                    .easing(Easing.Quadratic.InOut)
                    .onUpdate(() => {
                        camera.updateProjectionMatrix();
                    })
                    .start()
                    .onComplete(()=>{
                        new Tween(camera.position)
                        .to({fov: 25, x: 0.5},3000)
                        .easing(Easing.Quadratic.InOut)
                        .onUpdate(() => {
                            camera.updateProjectionMatrix();
                        })
                        .start().
                        onComplete(() => {
                            new Tween(camera.position)
                            .to({fov: 25, x: -0.5},3000)
                            .easing(Easing.Quadratic.InOut)
                            .onUpdate(() => {
                                camera.updateProjectionMatrix();
                            })
                            .start().
                            onComplete(() => {
                                new Tween(camera.position)
                                .to({fov: 45, x: 0, y:0, z:0},3000)
                                .easing(Easing.Quadratic.InOut)
                                .onUpdate(() => {
                                    camera.updateProjectionMatrix();
                                })
                                .start().
                                onComplete(() => {
                                    new Tween(camera)
                                    .to({fov: 45},3000)
                                    .easing(Easing.Quadratic.InOut)
                                    .onUpdate(() => {
                                        camera.updateProjectionMatrix();
                                    })
                                    .start().
                                    onComplete(() => {
                                        
                                    });
                                });
                            });
                        });
                    });
                });
            
        }

        
        
        (document.getElementsByClassName('snap-button')[0] as HTMLElement)!.addEventListener('click', () => {
            toggleArrows();
            playAudio(images[currentIndex].slice(0,-4), currentChapter.toString()); // Play audio for the current image
            pan(camera);
            (document.getElementsByClassName('ch1-button')[0] as HTMLElement)!.style.visibility = 'visible';
            (document.getElementsByClassName('x-button')[0] as HTMLElement)!.style.visibility = 'visible';
            (document.getElementsByClassName('snap-button')[0] as HTMLElement)!.style.visibility = 'hidden'; // Hide the snap button// Hide the snap button
        });

        (document.getElementsByClassName('ch1-button')[0] as HTMLElement)!.addEventListener('click', () => {
            currentChapter += 1;
            if(currentChapter >= 5 ) {
                currentChapter = 1; // Reset to chapter 1 if it exceeds 3
                (document.getElementsByClassName('ch1-button')[0] as HTMLElement)!.style.visibility = 'hidden';
            }
            playAudio(images[currentIndex].slice(0,-4), currentChapter.toString()); // Play audio for the current image
        });

        (document.getElementsByClassName('x-button')[0] as HTMLElement)!.addEventListener('click', () => {
            currentChapter = 1;
            (document.getElementsByClassName('ch1-button')[0] as HTMLElement)!.style.visibility = 'hidden';
            (document.getElementsByClassName('x-button')[0] as HTMLElement)!.style.visibility = 'hidden';
            (document.getElementsByClassName('snap-button')[0] as HTMLElement)!.style.visibility = 'visible';
            if (audio) {
                audio.pause(); // Pause the audio
                URL.revokeObjectURL(audio.src);
            }
            new Tween(camera)
                .to({fov: 70},3000)
                .easing(Easing.Quadratic.InOut)
                .onUpdate(() => {
                    camera.updateProjectionMatrix();
                })
                .start()
                .onComplete(()=> {
                    new Tween(camera.position)
                    .to({fov: 70, x: 0, y:0, z:0},3000)
                    .easing(Easing.Quadratic.InOut)
                    .onUpdate(() => {
                        camera.updateProjectionMatrix();
                    })
                    .start()
            });
            toggleArrows();
             // Play audio for the current image
        });
        
        document.getElementById('title')!.innerText = titles[0];
        document.getElementById('artist')!.innerText = artist[0];
	}

    
</script>

<svelte:head>
	<title>3D viewer</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" >
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,100&display=swap" rel="stylesheet">
</svelte:head>

<h1 id="title">""</h1>
<h2 id="artist">""</h2>
<button class="snap-button">
    ⚪
</button>

<button class="ch1-button">
    Next
</button>

<button class="x-button">
    X
</button>


<style>
    :global(body) {
        margin: 0;
        padding: 0;
        height: 100%; /* Ensure html and body take full viewport height */
        width: 100%;  /* Ensure html and body take full viewport width */
        overflow: hidden; /* Prevent any scrollbars on the main page */
    }
    h1,
    h2 {
        color: white;
        text-align: center;
        width: 100%;

        font-family: 'Inter';
        font-weight: 100;

        transition: opacity 0.5s ease-in-out;
    }

    #title {
        position: fixed;
        font-size: 3em;
        top: 0.2em;
    }

    #artist {
        position: fixed;
        font-size: 2em;
        color: gray;
        top: 2.5em;
    }

    .snap-button{
        bottom: 2em;
        left: 50%;
    }

    .ch1-button{
        bottom: 2em;
        left: 2%;
        visibility: hidden; /* Hide the button initially */
    }

    .x-button{
        top: 2em;
        right: 2%;
        visibility: hidden; /* Hide the button initially */
    }

    .snap-button, .ch1-button, .x-button {
        /* Basic Button Styling */
        position: fixed;
        
        padding: 10px 10px; /* Adjust padding to your preference */
        cursor: pointer;      /* Changes cursor to a hand on hover */
        font-family: 'Inter'; /* Choose a clear, readable font */
        font-size: 18px;      /* Adjust font size as needed */
        text-align: center;   /* Center the text horizontally */
        text-decoration: none;/* Remove any default underline from links if used on an <a> */

        /* Color Scheme */
        background-color: rgba(24, 100, 171, 0.1);  /* Black background */
        color: #ffffff;         /* White text color */
        border: 1px solid #ffffff; /* 2px solid white border */

        /* Rounded Corners */
        border-radius: 2em; /* Adjust this value for more or less roundness */

        /* Smooth Transitions (Optional but Recommended) */
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
    }

    /* Hover Effect (Optional but Recommended) */
    .snap-button:hover, .ch1-button:hover, .x-button:hover {
        background-color: #333333; /* Slightly lighter black on hover */
        border-color: #dddddd;   /* Slightly off-white border on hover */
    }

    /* Active/Clicked Effect (Optional) */
    .snap-button:active, .ch1-button:active, .x-button:active {
        background-color: #111111; /* Even darker on click */
        border-color: #cccccc;
    }

    /* Focus Effect (Important for Accessibility) */
    .snap-button:focus, .ch1-button:focus, .x-button:focus {
        outline: none; /* Remove default focus outline */
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.5); /* Custom white focus ring */
    }


    
</style>