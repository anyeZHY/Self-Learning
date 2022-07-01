export default `#version 300 es
    precision highp float;
    precision highp int;

    in vec4 aVertexPosition;
    in vec4 aVertexNormal;

    uniform mat4 uMeshToWorldMatrix;
    uniform mat4 uMeshToWorldRotMatrix;
    uniform mat4 uWorldToClipSpaceMatrix;

    out vec3 vPosition;
    out vec3 vNormal;

void main(void) {
  vPosition = (uMeshToWorldMatrix * aVertexPosition).xyz;
  vNormal = (uMeshToWorldRotMatrix * aVertexNormal).xyz;
  gl_Position = (uWorldToClipSpaceMatrix * uMeshToWorldMatrix * aVertexPosition);
}
`