## Answer of Assignment

1. $p_{xy}=\mqty[\sqrt{2}\\-\flatfrac{\sqrt{2}}2\\-\flatfrac{\sqrt{2}}2]$ and $p_{yx}=\mqty[\flatfrac{\sqrt{2}}2\\-\sqrt{2}\\-\flatfrac{\sqrt{2}}2]$. ${t_1}_{\mathrm{cube}}^{\mathrm{world}}=\mqty[3\\1\\2]$ and ${t_2}_{\mathrm{cube}}^{\mathrm{world}}=\mqty[\flatfrac{5\sqrt{2}}{2}\\1\\-\flatfrac{\sqrt2}{2}]$.

## Quiz Question

1. Why are homogeneous coordinates advantageous for computing transformations? What kind of matrix transformations preserve the value of $w$ given homogeneous coordinates $(x, y, z, w)$?
   - Homogenous coordinates allow the nonlinear $\flatfrac{1}{2}$ to be expressed with linear matrix multiplication.
2. Given a single homogeneous matrix transform with both a translation and rotation component, in what order are those two transforms applied? Which ordering of these two transforms is easiest for you to visualize?
3. How is the viewing frustum used to keep objects in the scene in relative perspective for the viewer -- i.e. how does perspective projection work?
4. Why do we use triangles rather than other polygons in rendering? Give at least 2 advantages.
   - Transformations (from last lecture) only need be applied to the triangle vertices. 
   - Complex objects are well approximated (piecewise linear convergence) using enough triangles.
5. What is the benefit of applying “bounding boxes” to triangles for rasterization?
   - Compute efficiently.
6. If we have two adjacent triangles facing the camera with a shared edge between them, what can we say about the 2D normals of this edge for each triangle? How do we use these normal directions to render a shared edge?
7. What are barycentric weights and why are they important?
   - We could get information of world space from a rendered picture (screen space).
8. How does the vertex order of a triangle affect how it’s rendered?
   - The vertex order of a triangle determines whether the triangle face the camera.
9. How do we know whether a 2D point is inside a 2D triangle or not?
10. What is an advantage of using ray tracing instead of scanline rendering?
    - Operating in world space is a huge advantage for the ray tracer when it comes to image quality, as it can thoroughly look around in world space to figure out what’s going on