## Quiz Question

1. What is one use of the surface normal for a bounce in a ray tracing algorithm?

   To calculate $D_{\mathrm{reflection}}$.

2. What natural phenomena require recursive ray tracing to render? Can you describe the process that is used to make sure rays aren’t infinitely generated/traced?

   Reflections and transmissions require recursive ray tracing. We will set a value to max depth to prevent infinite generation.

3. Ray tracing is inherently time-consuming compared to other strategies like scanline rendering. Describe a strategy that is used to make ray tracing quicker.

   Use parallelization on GPUs and CPUs. Or implement Simpler Bounding Volume.

4. How does ray tracer render shadows?

   By finding light's direction $\vec{l}.$

5. What is the difference between ambient and diffuse shading? Describe both algorithmic and visual differences.

   From light: $I_{\mathrm{diffuse}}=k_d(\flatfrac{I}{r^2})\max(\vec{n}\cdot\vec{l})$. From ambient object: $I_{\mathrm{ambient}}=k_{a}k_{d}$.

6. Explain the problem of spurious self-occlusion and how it can be solved.

   $\vec{h}\gets\vec{h}+\epsilon*\vec{n}$.

7. Why can metals reflect the color of surrounding objects and the environment from all viewing angles, but plastics cannot? Think about conductor and dielectrics material.

   The short answer is: Because metals are really absorptive (which comes from the fact that the nearly free electrons in the metal follow the oscillations of the radiation thereby depleting its energy), but some only in part of the visible range.[^1:]

8. Explain Snell’s Law. Under what circumstances will total reflection occur?

   Easy.

[^1]: https://physics.stackexchange.com/questions/213478/why-dont-dielectric-materials-have-coloured-reflections-like-conductors