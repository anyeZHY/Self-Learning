export default `#version 300 es
    precision highp float;
    precision highp int;
    in vec4 vNormal;
    out vec4 fragColor;

    void main(void) {
        // compute color from interpolated normal
        // vec4 vColor = vec4(normalize(abs(vNormal.xyz)),1.0);
        // fragColor = vColor;
        fragColor = vNormal;
    }
`