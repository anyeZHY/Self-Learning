// created by Thorsten Thormaehlen for educational purpose
// See https://www.mathematik.uni-marburg.de/~thormae/lectures/graphics1/code/WebGLShaderLightMat/ShaderLightMat.html

function vec3Dot(a, b) {
  return a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
}

function vec3Cross(a, b, res) {
  res[0] = a[1] * b[2]  -  b[1] * a[2];
  res[1] = a[2] * b[0]  -  b[2] * a[0];
  res[2] = a[0] * b[1]  -  b[0] * a[1];
}

function vec3Normalize(a) {
  var mag = Math.sqrt(a[0] * a[0]  +  a[1] * a[1]  +  a[2] * a[2]);
  a[0] /= mag; a[1] /= mag; a[2] /= mag;
} 

function mat4Identity(a) {
  a.length = 16;
  for (var i = 0; i < 16; ++i) a[i] = 0.0;
  for (var i = 0; i < 4; ++i) a[i + i * 4] = 1.0;
}

function mat4Multiply(res, a, b) {
  for (var i = 0; i < 4; ++i) {
    for (var j = 0; j < 4; ++j) {
      res[j*4 + i] = 0.0;
      for (var k = 0; k < 4; ++k) {
        res[j*4 + i] += a[k*4 + i] * b[j*4 + k];
      }
    }
  }
}

function mat4Perspective(a, fov, aspect, zNear, zFar) {
  var f = 1.0 / Math.tan (fov/2.0 * (Math.PI / 180.0));
  mat4Identity(a);
  a[0] = f / aspect;
  a[1 * 4 + 1] = f;
  a[2 * 4 + 2] = (zFar + zNear)  / (zNear - zFar);
  a[3 * 4 + 2] = (2.0 * zFar * zNear) / (zNear - zFar);
  a[2 * 4 + 3] = -1.0;
  a[3 * 4 + 3] = 0.0;
}

function mat4Translate(mat, vec) {
  mat[12] += vec[0];
  mat[13] += vec[1];
  mat[14] += vec[2];
}

function mat4LookAt(viewMatrix,
    eyeX, eyeY, eyeZ,
    centerX, centerY, centerZ,
    upX, upY, upZ) {

  var dir = new Float32Array(3);
  var right = new Float32Array(3);
  var up = new Float32Array(3);
  var eye = new Float32Array(3);

  up[0]=upX; up[1]=upY; up[2]=upZ;
  eye[0]=eyeX; eye[1]=eyeY; eye[2]=eyeZ;

  dir[0]=centerX-eyeX; dir[1]=centerY-eyeY; dir[2]=centerZ-eyeZ;
  vec3Normalize(dir);
  vec3Cross(dir,up,right);
  vec3Normalize(right);
  vec3Cross(right,dir,up);
  vec3Normalize(up);
  // first row
  viewMatrix[0]  = right[0];
  viewMatrix[4]  = right[1];
  viewMatrix[8]  = right[2];
  viewMatrix[12] = -vec3Dot(right, eye);
  // second row
  viewMatrix[1]  = up[0];
  viewMatrix[5]  = up[1];
  viewMatrix[9]  = up[2];
  viewMatrix[13] = -vec3Dot(up, eye);
  // third row
  viewMatrix[2]  = -dir[0];
  viewMatrix[6]  = -dir[1];
  viewMatrix[10] = -dir[2];
  viewMatrix[14] =  vec3Dot(dir, eye);
  // fourth row
  viewMatrix[3]  = 0.0;
  viewMatrix[7]  = 0.0;
  viewMatrix[11] = 0.0;
  viewMatrix[15] = 1.0;
}

function mat4Print(a) {
  // opengl uses column major order
  var out = "";
  for (var i = 0; i < 4; ++i) {
    for (var j = 0; j < 4; ++j) {
      out += a[j * 4 + i] + " ";
    }
    out += "\n";
  }
  alert(out);
}

function mat4Transpose(transposed, a) {
  var t = 0;
  for (var i = 0; i < 4; ++i) {
    for (var j = 0; j < 4; ++j) {
      transposed[t++] = a[j * 4 + i];
    }
  }
}

function mat4Invert(inverse, m) {
  var inv = new Float32Array(16);
  inv[0] = m[5]*m[10]*m[15]-m[5]*m[11]*m[14]-m[9]*m[6]*m[15]+
           m[9]*m[7]*m[14]+m[13]*m[6]*m[11]-m[13]*m[7]*m[10];
  inv[4] = -m[4]*m[10]*m[15]+m[4]*m[11]*m[14]+m[8]*m[6]*m[15]-
           m[8]*m[7]*m[14]-m[12]*m[6]*m[11]+m[12]*m[7]*m[10];
  inv[8] = m[4]*m[9]*m[15]-m[4]*m[11]*m[13]-m[8]*m[5]*m[15]+
           m[8]*m[7]*m[13]+m[12]*m[5]*m[11]-m[12]*m[7]*m[9];
  inv[12]= -m[4]*m[9]*m[14]+m[4]*m[10]*m[13]+m[8]*m[5]*m[14]-
           m[8]*m[6]*m[13]-m[12]*m[5]*m[10]+m[12]*m[6]*m[9];
  inv[1] = -m[1]*m[10]*m[15]+m[1]*m[11]*m[14]+m[9]*m[2]*m[15]-
           m[9]*m[3]*m[14]-m[13]*m[2]*m[11]+m[13]*m[3]*m[10];
  inv[5] = m[0]*m[10]*m[15]-m[0]*m[11]*m[14]-m[8]*m[2]*m[15]+
           m[8]*m[3]*m[14]+m[12]*m[2]*m[11]-m[12]*m[3]*m[10];
  inv[9] = -m[0]*m[9]*m[15]+m[0]*m[11]*m[13]+m[8]*m[1]*m[15]-
           m[8]*m[3]*m[13]-m[12]*m[1]*m[11]+m[12]*m[3]*m[9];
  inv[13]= m[0]*m[9]*m[14]-m[0]*m[10]*m[13]-m[8]*m[1]*m[14]+
           m[8]*m[2]*m[13]+m[12]*m[1]*m[10]-m[12]*m[2]*m[9];
  inv[2] = m[1]*m[6]*m[15]-m[1]*m[7]*m[14]-m[5]*m[2]*m[15]+
           m[5]*m[3]*m[14]+m[13]*m[2]*m[7]-m[13]*m[3]*m[6];
  inv[6] = -m[0]*m[6]*m[15]+m[0]*m[7]*m[14]+m[4]*m[2]*m[15]-
           m[4]*m[3]*m[14]-m[12]*m[2]*m[7]+m[12]*m[3]*m[6];
  inv[10]= m[0]*m[5]*m[15]-m[0]*m[7]*m[13]-m[4]*m[1]*m[15]+
           m[4]*m[3]*m[13]+m[12]*m[1]*m[7]-m[12]*m[3]*m[5];
  inv[14]= -m[0]*m[5]*m[14]+m[0]*m[6]*m[13]+m[4]*m[1]*m[14]-
           m[4]*m[2]*m[13]-m[12]*m[1]*m[6]+m[12]*m[2]*m[5];
  inv[3] = -m[1]*m[6]*m[11]+m[1]*m[7]*m[10]+m[5]*m[2]*m[11]-
           m[5]*m[3]*m[10]-m[9]*m[2]*m[7]+m[9]*m[3]*m[6];
  inv[7] = m[0]*m[6]*m[11]-m[0]*m[7]*m[10]-m[4]*m[2]*m[11]+
           m[4]*m[3]*m[10]+m[8]*m[2]*m[7]-m[8]*m[3]*m[6];
  inv[11]= -m[0]*m[5]*m[11]+m[0]*m[7]*m[9]+m[4]*m[1]*m[11]-
           m[4]*m[3]*m[9]-m[8]*m[1]*m[7]+m[8]*m[3]*m[5];
  inv[15]= m[0]*m[5]*m[10]-m[0]*m[6]*m[9]-m[4]*m[1]*m[10]+
           m[4]*m[2]*m[9]+m[8]*m[1]*m[6]-m[8]*m[2]*m[5];

  var det = m[0]*inv[0]+m[1]*inv[4]+m[2]*inv[8]+m[3]*inv[12];
  if (det === 0) return false;
  det = 1.0 / det;
  for (var i = 0; i < 16; i++) inverse[i] = inv[i] * det;
  return true;
}

function rotationMat(rot, degree, ax_xyz) {
  mat4Identity(rot);
  var rad = Math.PI / 180.0 * degree;
  var ax1 = (ax_xyz + 1) % 3;
  var ax2 = (ax_xyz + 2) % 3;

  rot[ax1 + 4 *  ax1] = Math.cos(rad);
  rot[ax2 + 4 *  ax1] = Math.sin(rad);
  rot[ax1 + 4 *  ax2] = -Math.sin(rad); 
  rot[ax2 + 4 *  ax2] = Math.cos(rad);   
}

