//define global constants
const IMAGE_PREFIX = "specular"; //you'll change this for each checkpoint 
const MAX_OUT_FRAMES = 9; //set this to 9 to write out images, set back to zero when you're debugging
const OBJ_FILE = "assets/bunny.obj"; //obj file to load
var TIME = 0.0;

//load in shader content
import vsSource from "./shaders/phong_vert.js"; //change this to ./shaders/phong_vert.js for the second part of the homework
import fsSource from "./shaders/phong_frag.js"; //change this to ./shaders/phong_frag.js for the second part of the homework

//run main function
main();

async function main() {
  const canvas = document.querySelector('#glcanvas');
  const gl = canvas.getContext('webgl2');
  if (!gl) {
    alert('Unable to initialize WebGL2. Your browser or machine may not support it.');
    return;
  }

  // Initialize a shader program
  const shaderProgram = initShaderProgram(gl, vsSource, fsSource);

  // Initialize and define all the info needed to use the shader program.
  const programInfo = {
    program: shaderProgram,
    attribLocations: {
      vertexPosition: gl.getAttribLocation(shaderProgram, 'aVertexPosition'),
      vertexNormal: gl.getAttribLocation(shaderProgram, 'aVertexNormal'),
    },
    uniformLocations: {
      ambientColor: gl.getUniformLocation(shaderProgram, 'uAmbientColor'),
      diffuseColor: gl.getUniformLocation(shaderProgram, 'uDiffuseColor'),
      specularColor: gl.getUniformLocation(shaderProgram, 'uSpecularColor'),
      // TODO: do the same for diffuse and specular
      lightPosition: gl.getUniformLocation(shaderProgram, 'uLightPosition'),
      lightColor: gl.getUniformLocation(shaderProgram, 'uLightColor'),
      WorldToClipSpaceMatrix: gl.getUniformLocation(shaderProgram, 'uWorldToClipSpaceMatrix'),
      MeshToWorldMatrix: gl.getUniformLocation(shaderProgram, 'uMeshToWorldMatrix'),
      MeshToWorldRotMatrix: gl.getUniformLocation(shaderProgram, 'uMeshToWorldRotMatrix'),
    },
    uniformValues: {
      ambientColor: [0.2,0.1,0.1,1.0],
      diffuseColor: [0.7,0.5,0.1,1.0],
      specularColor: [0.1,0.4,0.8,1.0],
      lightPosition: [16.0,8.0,4.0],
      lightColor: [1.0,1.0,1.0,1.0],
    }
  };

  // Here's where we call the routine that builds all the
  // objects we'll be drawing.
  const buffers = await loadMeshAndInitBuffers(gl, OBJ_FILE);

  // Draw the scene repeatedly
  var write_frame = 0;
  var prev_t = 0;
  function render(curr_t) {
    curr_t *= 0.001;  // convert to seconds
    const deltaTime = curr_t - prev_t;
    drawScene(gl, programInfo, buffers, deltaTime);
    // If we want to save out images, do it here
    if (write_frame < MAX_OUT_FRAMES && curr_t>write_frame){
      const output_name=`hw2_${IMAGE_PREFIX}_${write_frame}.png`;
      write_frame += 1;
      canvas.toBlob((blob) => {
      saveBlob(blob, output_name);
      });
    }
    prev_t = curr_t;
    requestAnimationFrame(render);
  }
  requestAnimationFrame(render);
}

// Load the mesh and initialize the gl buffers we'll need for the mesh.
async function loadMeshAndInitBuffers(gl, meshPath) {
  const response = await fetch(meshPath);  
  const data = await response.text();
  const mesh = parseOBJ(data);
  const positionBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(mesh.positions), gl.STATIC_DRAW);

  const normalBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, normalBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(mesh.normals), gl.STATIC_DRAW);

  return {
    position: positionBuffer,
    normal: normalBuffer,
    num_gl_vertices: mesh.positions.length,
  };
}

// Draw the scene.
function drawScene(gl, programInfo, buffers, deltaTime) {
  gl.clearColor(0.0, 0.0, 0.0, 1.0);  // Clear to black, fully opaque
  gl.clearDepth(1.0);                 // Clear everything
  gl.enable(gl.DEPTH_TEST);           // Enable depth testing
  gl.depthFunc(gl.LEQUAL);            // Near things cover up far things
  // Clear the canvas before we start drawing on it.
  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

  // Calculate camera and animated transforms
  const fieldOfView = 45.0;   // in degrees
  const aspect = gl.canvas.clientWidth / gl.canvas.clientHeight;
  const zNear = 0.1;
  const zFar = 100.0;
  // skipping world2cam and using cam2clip as world2cam
  // assumes world2cam is the identity matrix, which
  // implies a camera at the origin looking down the Z axis
  const WorldToClipSpaceMatrix = new Float32Array(16); 
  mat4Perspective(WorldToClipSpaceMatrix,
                   fieldOfView,
                   aspect,
                   zNear,
                   zFar);

 const MeshToWorldMatrix = new Float32Array(16);
  mat4Identity(MeshToWorldMatrix);
  rotationMat(MeshToWorldMatrix,  // destination matrix
              TIME * 20,// amount to rotate in degrees
              1,
              );
  mat4Translate(MeshToWorldMatrix, [-0.0,-2.0,-7.5]);


  const MeshToWorldRotMatrix = new Float32Array(16);
  rotationMat(MeshToWorldRotMatrix,  // destination matrix
              TIME * 20,// amount to rotate in degrees
              1,
              );


  // Tell WebGL how to pull out the positions from the position
  // buffer into the vertexPosition attribute
  {
    const numComponents = 3;
    const type = gl.FLOAT;
    const normalize = false;
    const stride = 0;
    const offset = 0;
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.position);
    gl.vertexAttribPointer(
        programInfo.attribLocations.vertexPosition,
        numComponents,
        type,
        normalize,
        stride,
        offset);
    gl.enableVertexAttribArray(
        programInfo.attribLocations.vertexPosition);
    
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.normal);
    gl.vertexAttribPointer(
        programInfo.attribLocations.vertexNormal,
        numComponents,
        type,
        normalize,
        stride,
        offset);
    gl.enableVertexAttribArray(
        programInfo.attribLocations.vertexNormal);
  }


  // Tell WebGL to use our program when drawing
  gl.useProgram(programInfo.program);

  // Set the values that get passed into the shaders
  gl.uniformMatrix4fv(programInfo.uniformLocations.WorldToClipSpaceMatrix,
      false, WorldToClipSpaceMatrix);
  gl.uniformMatrix4fv(programInfo.uniformLocations.MeshToWorldMatrix,
      false, MeshToWorldMatrix);
  gl.uniformMatrix4fv(programInfo.uniformLocations.MeshToWorldRotMatrix,
      false, MeshToWorldRotMatrix);

  gl.uniform4fv(programInfo.uniformLocations.ambientColor,
      programInfo.uniformValues.ambientColor);
  gl.uniform4fv(programInfo.uniformLocations.diffuseColor,
      programInfo.uniformValues.diffuseColor);
  gl.uniform4fv(programInfo.uniformLocations.specularColor,
      programInfo.uniformValues.specularColor);
  // TODO: do the same for diffuse and specular
  gl.uniform4fv(programInfo.uniformLocations.lightColor,
      programInfo.uniformValues.lightColor);
  gl.uniform3fv(programInfo.uniformLocations.lightPosition,
      programInfo.uniformValues.lightPosition);

  //Draw our vertex buffer data as triangles
  const offset = 0;
  const vertexCount = buffers.num_gl_vertices;
  gl.drawArrays(gl.TRIANGLES, offset, vertexCount / 3);
  
  //Update time
  TIME += deltaTime;
}

// Initialize a shader program, so WebGL knows how to draw our data
function initShaderProgram(gl, vsSource, fsSource) {
  const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vsSource);
  const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, fsSource);

  // Create the shader program
  const shaderProgram = gl.createProgram();
  gl.attachShader(shaderProgram, vertexShader);
  gl.attachShader(shaderProgram, fragmentShader);
  gl.linkProgram(shaderProgram);

  // If creating the shader program failed, alert
  if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
    alert('Unable to initialize the shader program: ' + gl.getProgramInfoLog(shaderProgram));
    return null;
  }
  return shaderProgram;
}


// creates a shader of the given type, uploads the source and compiles it.
function loadShader(gl, type, source) {
  const shader = gl.createShader(type); 
  gl.shaderSource(shader, source); // Send the source to the shader object
  gl.compileShader(shader);        // Compile the shader program
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    alert('An error occurred compiling the shaders: ' + gl.getShaderInfoLog(shader));
    gl.deleteShader(shader);
    return null;
  }
  return shader;
}

// random utility function for saving webGL canvas to an image
const saveBlob = (function() {
    const a = document.createElement('a');
    document.body.appendChild(a);
    a.style.display = 'none';
    return function saveData(blob, fileName) {
       const url = window.URL.createObjectURL(blob);
       a.href = url;
       a.download = fileName;
       a.click();
    };
  }());