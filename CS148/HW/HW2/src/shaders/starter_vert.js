export default `#version 300 es
    precision highp float;
    precision highp int;

    in vec4 aVertexPosition;
    in vec4 aVertexNormal;

    uniform mat4 uMeshToWorldMatrix;
    uniform mat4 uMeshToWorldRotMatrix;
    uniform mat4 uWorldToClipSpaceMatrix;
    
    flat out vec4 vNormal;

void main(void) {
  // set vertex normal (to be passed to fragment shader)
  vNormal = uMeshToWorldRotMatrix * aVertexNormal;

  // set world space vertex position
  vec4 vPosition = uMeshToWorldMatrix * aVertexPosition;

  //openGL reads the clipping space coordinates from gl_Position
  gl_Position = uWorldToClipSpaceMatrix * vPosition;
}
`