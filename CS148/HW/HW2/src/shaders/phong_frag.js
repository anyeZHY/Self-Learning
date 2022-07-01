export default `#version 300 es
    precision highp float;
    precision highp int;

    in vec3 vPosition;
    in vec3 vNormal;

    uniform vec4 uAmbientColor;
    // TODO: pass in diffuse and specular too
    uniform vec4 uLightColor;
    uniform vec3 uLightPosition;

    out vec4 fragColor;

    // Hint: see page 8 (and bottom of page 7) 
    // of https://www.khronos.org/files/webgl20-reference-guide.pdf
    // for functions you can call!

    void main(void) {
      float specularAlpha = 6.0;
      
      fragColor = uAmbientColor;
      // Uncomment these once you've passed in the colors and computed coeffDiffuse and coeffSpecular
      // fragColor += coeffDiffuse * (uDiffuseColor * uLightColor);
      // fragColor += coeffSpecular * (uSpecularColor * uLightColor);
    }
`